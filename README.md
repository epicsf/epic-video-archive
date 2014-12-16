## Epic Video Disk Archive Script

Developer: Thomas Knickman

Email: tknickman@gmail.com

##### To Install:
* open terminal
* if the system doesn’t have PIP installed, run: `sudo easy_install pip`
* cd to the directory
* install requirements for the program to run: `sudo pip install -r requirements.txt`
* copy `config.ini.example` file to `config.ini` and set required options
* run with `python app.py`


##### How it works:

* Searches for all external disks with a name starting with "Video" (reports error if none are found)
* Walks the disk, and uploads all files to a new folder with the same directory structure as the local 
* New directory named with the following naming scheme by default: `/Masters/[ISO 8601 datetime]`
