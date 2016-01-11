import ConfigParser
import os


parser = ConfigParser.SafeConfigParser()
# read config with absolute path
parser.readfp(open(os.path.join(os.path.abspath('%s/%s' % (
    os.path.dirname(__file__),
    'config.ini')))))

SECTION = 'epic_drive_backup_main'


class Settings(object):
    s3_access_key = parser.get(
        SECTION,
        'S3_ACCESS_KEY'
    )

    s3_secret_key = parser.get(
        SECTION,
        'S3_SECRET_KEY'
    )

    s3_bucket_name = parser.get(
        SECTION,
        's3_bucket_name'
    )

    s3_max_file_size = parser.getint(
        SECTION,
        's3_max_file_size'
    )

    s3_max_file_part_size = parser.getint(
        SECTION,
        's3_max_file_part_size'
    )
