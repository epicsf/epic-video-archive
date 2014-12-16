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
	destDir = '/Masters/%s'%datetime.datetime.now().isoformat()
	uploadFileNames = {}
	for (sourceDir, dirname, filename) in os.walk(folder):
		uploadFileNames.setdefault(sourceDir, []).extend(filename)
 
	for sourceDir in uploadFileNames:
		for filename in uploadFileNames[sourceDir]:
			sourcepath = '%s/%s'%(sourceDir, filename)
			#build the dest path
			path_parts = sourceDir.split('/')
			path_prefix = '/'.join(path_parts[2:])
			destpath = os.path.join(path_prefix, filename)
			final_dest_path = os.path.join(destDir, destpath)
			sys.stdout.write('Uploading %s to Amazon S3 bucket %s' % (filename, bucket.name))
	 
			filesize = os.path.getsize(sourcepath)
			if filesize > settings.s3_max_file_size:
				mp = bucket.initiate_multipart_upload(final_dest_path)
				fp = open(sourcepath,'rb')
				fp_num = 0
				while (fp.tell() < filesize):
					fp_num += 1
					sys.stdout.write("\nUploading part %i" % fp_num)
					mp.upload_part_from_file(fp, fp_num, cb=_percent_complete, num_cb=10, size=settings.s3_max_file_part_size)

				mp.complete_upload()
		 
			else:
				k = boto.s3.key.Key(bucket)
				k.key = final_dest_path
				k.set_contents_from_filename(sourcepath, cb=_percent_complete, num_cb=10)
				print
	print 

