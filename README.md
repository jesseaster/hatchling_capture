# Hatchling Capture
Captures a webcam picture every X minutes based on the settings.ini file, uploads to Google Drive

The resolution can be changed by adjusting the image_width and image_height in the INI file.
[Common resolutions](https://en.wikipedia.org/wiki/List_of_common_resolutions)

## Setup Project
This setup process will create a python virtual environment to keep our package requirements contained to this project.

Open a terminal and navigate to the Desktop.

For Windows:
```batch
python3 -m venv hatchling
cd hatching
git clone git@github.com:jesseaster/hatchling_capture.git
Scripts\activate
cd hatchling_capture
pip install -r requirements.txt
python gui.py
```

To create an executable:
```batch
pyinstaller gui.py -F
```
The gui.exe file will get created in the dist folder.


The gui.exe program should then be moved to the G Drive.
