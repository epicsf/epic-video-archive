Developer: Thomas Knickman
Email: tknickman@gmail.com

TO INSTALL:
1. open terminal
2. if the system doesn’t have PIP installed, run: “sudo easy_install pip”
3. cd to the directory
4. install requirements for the program to run: “sudo pip install -r requirements.txt”
5. set config options in config.ini file =
6. run with “python app.py”


How it works:

1. Searches for all external drives (reports error if none are found)
2. Walks the drive, and uploads all files to a new folder with the same directory structure as the local 
3. New directory named with the following naming scheme by default: “/epic_prod_drives-year-month-day-hour:minute:second