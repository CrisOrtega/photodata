# photodata
This script is used to manage a photo folder in your PC.
It basically makes two things

- The first one is to change the name of the files using a date format. In order to have date format names for the files. This is done through Exif data and creation and modification file.
- The second one is to create a small (or several) csv files with some stats taken from exif data 




# how to use it

In order to use the script it is just enough to run it using python. 

C:> python.exe photodata.py

or you can add a shebang line at the beginning of the script: #!/usr/bin/env python3

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



# Name change



# output csv file  