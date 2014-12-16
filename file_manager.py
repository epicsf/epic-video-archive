import zipfile
import shutil
import time
import os


def get_external_drives():
	external = []
	for drive in os.listdir('/Volumes'):
		if os.path.ismount('/Volumes/%s' % drive):
			external.append('/Volumes/%s' % drive)
	return external

