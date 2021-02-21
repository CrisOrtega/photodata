
# This file is to store the config variables used in the script

PATH = r'C:\Users\Cristóbal Ortega\Desktop\phototest'
supported_formats = ('jpg','jpeg')
metadata_fields = ()
# Date min, not uset so far
min_date = '1900:00:00 00:00:00'
# Indicates if the name must me changed
correct_name = True
name_pattern='[1-2]\d{3}[0-1]\d[0-3]\d_[0-2]\d[0-6]\d[0-6]\d_*.*'

tags=('DateTimeOriginal','ProcessingSoftware','MaxApertureValue','Fnumber','MeteringMode','Flash','FocalLength',
      'ExifImageWidth','ExifImageHeight','Saturation','Make','Model','ISOSpeedRatings','FocalLengthIn35mmFilm',
      'ExposureTime','ExposureBiasValue','Orientation','DateTime')
# https://exiftool.org/TagNames/EXIF.html
ExifDict={'Path':[],'Name':[],
          'DateTime':[],
          'Maker':['Make'],
          'Model':['Model'],
          'FocalLength':['FocalLength'],
          'FocalLengthIn35mmFilm':['FocalLengthIn35mmFilm'],
          'Aperture':['Fnumber','MaxApertureValue'],
          'ExposureTime':['ExposureTime'],
          'ExposureBiasValue':['ExposureBiasValue'],
          'ISO': ['ISOSpeedRatings'],
          'Orientation':['Orientation'],
          'Flash':['Flash'],
          'MeteringMode':['MeteringMode'],
          'ExifImageWidth':['ExifImageWidth'],
          'ExifImageHeight':['ExifImageHeight']}