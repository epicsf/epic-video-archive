import boto.s3.connection
import settings
import datetime
import boto
import sys
import os


settings = settings.Settings()

def connect_to_s3():
	connection = boto.connect_s3(
				aws_access_key_id = settings.s3_access_key,
	        	aws_secret_access_key = settings.s3_secret_key,
	        	calling_format = boto.s3.connection.OrdinaryCallingFormat())
	return connection

def connect_to_bucket(connection):
	return connection.get_bucket(settings.s3_bucket_name, validate=False)

def _percent_complete(complete, total):
	    sys.stdout.write('.')
	    sys.stdout.flush()

def upload(connection, bucket, folder):
	dest_dir = '/Masters/%s'%datetime.datetime.now().isoformat()
	upload_file_names = {}
	for (source_dir, dir_name, filename) in os.walk(folder):
		upload_file_names.setdefault(source_dir, []).extend(filename)
 
	for source_dir in upload_file_names:
		for filename in upload_file_names[source_dir]:
			absolute_source_path = '%s/%s'%(source_dir, filename)
			relative_source_path = absolute_source_path.replace("%s/" % folder, '')
			final_dest_path = os.path.join(dest_dir, relative_source_path)
			sys.stdout.write('Uploading %s to Amazon S3 bucket %s' % (final_dest_path, bucket.name))
	 
			filesize = os.path.getsize(absolute_source_path)
			if filesize > settings.s3_max_file_size:
				mp = bucket.initiate_multipart_upload(final_dest_path)
				fp = open(absolute_source_path, 'rb')
				fp_num = 0
				while (fp.tell() < filesize):
					fp_num += 1
					sys.stdout.write("\nUploading part %i" % fp_num)
					mp.upload_part_from_file(fp, fp_num, cb=_percent_complete, num_cb=10, size=settings.s3_max_file_part_size)

				mp.complete_upload()
		 
			else:
				k = boto.s3.key.Key(bucket)
				k.key = final_dest_path
				k.set_contents_from_filename(absolute_source_path, cb=_percent_complete, num_cb=10)
				print
	print 

