from settings import Settings
import boto.s3.connection
import datetime
import logging
import time
import boto
import math
import sys
import os


logging.basicConfig()


def connect_to_s3():
    connection = boto.connect_s3(
        aws_access_key_id=Settings.s3_access_key,
        aws_secret_access_key=Settings.s3_secret_key,
        calling_format=boto.s3.connection.OrdinaryCallingFormat()
    )
    return connection


def connect_to_bucket(connection):
    return connection.get_bucket(Settings.s3_bucket_name, validate=False)


def _percent_complete(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def upload(connection, bucket, folder):
    os.system('clear')
    dest_dir = '/Masters/%s' % datetime.datetime.now().isoformat()

    print 'Starting upload to Amazon S3 bucket %s' % bucket.name
    print 'Source:      %s' % folder
    print 'Destination: %s' % dest_dir

    upload_file_names = {}
    for (source_dir, dir_name, filename) in os.walk(folder):
        # strip out hidden files and directories
        filename = [f for f in filename if not f[0] == '.']
        dir_name[:] = [d for d in dir_name if not d[0] == '.']
        upload_file_names.setdefault(source_dir, []).extend(filename)

    for source_dir in upload_file_names:
        for filename in upload_file_names[source_dir]:
            all_upload_times = []
            part_time = 0
            absolute_source_path = '%s/%s' % (source_dir, filename)
            relative_source_path = absolute_source_path.replace(
                '%s/' % folder, ''
            )
            final_dest_path = os.path.join(dest_dir, relative_source_path)

            filesize = os.path.getsize(absolute_source_path)
            if filesize > Settings.s3_max_file_size:
                mp = bucket.initiate_multipart_upload(final_dest_path)
                fp = open(absolute_source_path, 'rb')
                fp_num = 0
                while fp.tell() < filesize:
                    fp_num += 1
                    print '\n%s part            : %i' % (
                        relative_source_path, fp_num
                    )
                    print '____________________________'
                    if fp_num == 1:
                        print 'Percent complete            : N/A'
                        print 'Previous part upload time   : N/A'
                        print 'Average part upload time    : N/A'
                        print 'Estimated time of completion: calculating...'
                    else:
                        num_parts = math.ceil(
                            float(filesize) / float(
                                Settings.s3_max_file_part_size
                            )
                        )
                        avg_part_time = sum(
                            all_upload_times) / float(len(all_upload_times))
                        print 'Percent Complete            : %0.6f' % (
                            ((Settings.s3_max_file_part_size * fp_num) /
                             float(filesize)) * 100.0
                        )
                        print 'Previous Part Upload Time   : %0.6f sec' % \
                              part_time
                        print 'Average Part Upload Time    : %0.6f sec' % \
                              avg_part_time
                        if fp_num > 4:
                            print 'Estimated Time To Completion: %0.2f min' % \
                                  ((num_parts - fp_num) * avg_part_time / 60.0)
                        else:
                            print 'Estimated Time Of Completion: calculating...'

                    print '____________________________'

                    try:
                        upload_start = time.time()
                        mp.upload_part_from_file(
                            fp, fp_num, cb=_percent_complete, num_cb=10,
                            size=Settings.s3_max_file_part_size
                        )
                        part_time = time.time() - upload_start

                    except Exception as e:
                        logging.error(e)
                        part_time = 0.0

                    os.system('clear')
                    all_upload_times.append(part_time)

                mp.complete_upload()

            else:
                try:
                    k = boto.s3.key.Key(bucket)
                    k.key = final_dest_path
                    k.set_contents_from_filename(
                        absolute_source_path, cb=_percent_complete, num_cb=10
                    )
                except Exception as e:
                    logging.error(e)
                print
    print
