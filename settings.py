import ConfigParser


parser = ConfigParser.SafeConfigParser()
parser.read('config.ini')
SECTION = 'epic_drive_backup_main'

class Settings():
	def __init__(self):
		self.s3_access_key = parser.get(SECTION, 'S3_ACCESS_KEY')
		self.s3_secret_key = parser.get(SECTION, 'S3_SECRET_KEY')
		self.s3_bucket_name = parser.get(SECTION, 's3_bucket_name')
		self.s3_max_file_size = parser.getint(SECTION, 's3_max_file_size')
		self.s3_max_file_part_size = parser.getint(SECTION, 's3_max_file_part_size')