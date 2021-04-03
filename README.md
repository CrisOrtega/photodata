# photodata


This script is used to manage a <b>photo folder</b> in your PC.
It basically makes two things

- It changes the name of the files using a date format (YYYYMMDD_hhmmss). This allow an intuitive sorting of files. It uses Exif data and file dates.
- It creates a small (or several) csv files with some stats taken from exif data. This can be easily explored with Tableau or PowerBI 



# how to use it

In order to use the script 

- Configure all aspects using config.py 
- Run it with Python: <b>C:> python.exe photodata.py</b>

Alternatively, you can add a shebang line at the beginning of the script: #!/usr/bin/env python3

The way to control how the script works is through the config file: config.py
See the Config File section to see how it can be configured.

# Dependencies

The main dependencies to be included in Python are:

import sys 	# For error management
import os 	# For OS calls and file operation 
import re	# For regex and name matching
import csv	# To produce the csv files

from datetime import datetime	# To work with time for the images
from PIL import Image			# In order to read de image
from PIL.ExifTags import TAGS	# To read the Exif data


# Config File

The config is available as variables in the script, as long as config is imported with "import config"

General config
-------------------

PATH = r'C:\complete_path'
> Path of the folder with the files. The example is in windows. It is important to modify this
> It can include spaces and does not need to include / or \ at the end

supported_formats = ('jpg','jpeg')
> This is to identify the image format supported_formats

tags=('DateTimeOriginal','ProcessingSoftware','MaxApertureValue','Fnumber','MeteringMode','Flash','FocalLength',
      'ExifImageWidth','ExifImageHeight','Saturation','Make','Model','ISOSpeedRatings','FocalLengthIn35mmFilm',
      'ExposureTime','ExposureBiasValue','Orientation','DateTime')
> These are the tags to be read
> If we need these new tags to be included in csv file they need to be included here and also in ExifDict
> The rest of Exif tags are ignored

Rename config
-------------------
correct_name = True
> This indicates if the name of the files is going to be changed. 
> Set to False if you don't want to change the names and you want only to extract a report 

name_pattern='[1-2]\d{3}[0-1]\d[0-3]\d_[0-2]\d[0-6]\d[0-6]\d_*.*'
> This is the pattern to look in the files. 
> Note: This is to be improved. This is static and must not be changed.
> In the future I expect the name of the files to be configurable

Report config
-------------------
reports=[
    {'file':'all_photos.csv', 'subpath':'ALBUM FINAL'},
    {'file':'instagram.csv', 'subpath':'_instagram\IG_done'}
]
> These are the reports to produce.
> file: it is the file to be produced at the root level of PATH variables
> subpath: it is the subfolder that will be analyzed 
> So, the script read all images in subpath and store the info of them in the file specified in file

date_format_report='%Y-%m-%d %H:%M:%S'
> This is the output format of the dates in the report.
> I strongly recommend to format it in a way it can be easily usable by a third party
> In the example, the date is in a PowerBI format 

ExifDict
> This variable is a mapping between the report fields to produce and the Exif data
> 'Path':[],'Name':[],'DateTime':[]    must be always present
> I recommend not to modify them if possible

Extra config
-------------------

conversion_to_35mm
> This is a dictionary with the convertion ratio for all models 
> It will be also be exported as csv to PATH/camera_conversion.csv


# Name change

The name change functionality works just by configuring the option in the config.py file

> correct_name = True

Once the correct_name option is specified, the script will automatically rename all files with formats specified in config.py:

> supported_formats = ('jpg','jpeg')

under the following path defined in config.py:

> PATH = r'C:\complete_path'

The files not matching the following regex will be renamed to: YYYYMMDD_hhmmss.ext or YYYYMMDD_hhmmss_N.ext
This way the name will be in a
> name_pattern='[1-2]\d{3}[0-1]\d[0-3]\d_[0-2]\d[0-6]\d[0-6]\d_*.*'

Any file named as YYYYMMDD_hhmmss_FreeText.ext won't be renamed

# output csv file  


# warning report