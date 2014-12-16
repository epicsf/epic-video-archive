import zipfile
import shutil
import time
import os


def get_video_volumes():
	video_volumes = []
	for drive in os.listdir('/Volumes'):
		if os.path.ismount('/Volumes/%s' % drive) and drive.startswith('Video'):
			video_volumes.append('/Volumes/%s' % drive)
	return video_volumes
