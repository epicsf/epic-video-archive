import file_manager
import s3_manager
import settings
import sys


settings = settings.Settings()

def main():
	# get all the drive contents
	drive_list = file_manager.get_video_volumes()
	if not drive_list:
		print "No video disks detected"
		sys.exit()

	# connect to s3
	connection = s3_manager.connect_to_s3()
	bucket = s3_manager.connect_to_bucket(connection)
	if not bucket: 
		print "Bucket does not exist on S3!"
		sys.exit()

	# upload to s3
	for drive in drive_list:
		s3_manager.upload(connection, bucket, drive)	






main()