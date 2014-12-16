## Epic Production Drive Backup Script

Developer: Thomas Knickman

Email: tknickman@gmail.com

##### TO INSTALL:
* open terminal
* if the system doesn’t have PIP installed, run: “sudo easy_install pip”
* cd to the directory
* install requirements for the program to run: “sudo pip install -r requirements.txt”
* set config options in config.ini file =
* run with “python app.py”


##### How it works:

* Searches for all external drives (reports error if none are found)
* Walks the drive, and uploads all files to a new folder with the same directory structure as the local 
* New directory named with the following naming scheme by default: “/epic_prod_drives-year-month-day-hour:minute:second
