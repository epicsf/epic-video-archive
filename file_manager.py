import os


def get_video_volumes():
    video_volumes = []
    for drive in os.listdir('/Volumes'):
        normalized_drive = drive.lower()
        if os.path.ismount('/Volumes/%s' % drive) and \
                normalized_drive.startswith('video'):
            video_volumes.append('/Volumes/%s' % drive)
    return video_volumes
