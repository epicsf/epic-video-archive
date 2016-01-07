import boto.s3.connection
import settings
import datetime
import logging
import boto
import sys
import os


logging.basicConfig()
settings = settings.Settings()


def connect_to_s3():
    connection = boto.connect_s3(
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        calling_format=boto.s3.connection.OrdinaryCallingFormat()
    )
    return connection


def connect_to_bucket(connection):
    return connection.get_bucket(settings.s3_bucket_name, validate=False)


def _percent_complete(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def upload(connection, bucket, folder):
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
            absolute_source_path = '%s/%s' % (source_dir, filename)
            relative_source_path = absolute_source_path.replace(
                '%s/' % folder, ''
            )
            final_dest_path = os.path.join(dest_dir, relative_source_path)
            sys.stdout.write(relative_source_path)

            filesize = os.path.getsize(absolute_source_path)
            if filesize > settings.s3_max_file_size:
                mp = bucket.initiate_multipart_upload(final_dest_path)
                fp = open(absolute_source_path, 'rb')
                fp_num = 0
                while fp.tell() < filesize:
                    fp_num += 1
                    sys.stdout.write(
                        '\n%s part %i' % (relative_source_path, fp_num)
                    )
                    try:
                        mp.upload_part_from_file(
                            fp, fp_num, cb=_percent_complete, num_cb=10,
                            size=settings.s3_max_file_part_size
                        )
                    except Exception as e:
                        logging.error(e)

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
