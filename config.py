
# This file is to store the config variables used in the script


# General config
#--------------------------------------
# Path of the folder with images to be renamed
PATH = r'C:\Users\Cristóbal Ortega\Desktop\fotos'

# Suported_formats by the script
supported_formats = ('jpg','jpeg')

# Tags readed. Rest of tags are ignored
# https://exiftool.org/TagNames/EXIF.html
tags=('DateTimeOriginal','ProcessingSoftware','MaxApertureValue','Fnumber','MeteringMode','Flash','FocalLength',
      'ExifImageWidth','ExifImageHeight','Saturation','Make','Model','ISOSpeedRatings','FocalLengthIn35mmFilm',
      'ExposureTime','ExposureBiasValue','Orientation','DateTime')


# Rename config
#--------------------------------------
# RENAMING IMAGES PARAMETERS
# This fiels indicates if the name must me changed
# IMPORTANT. If set to True it will modify the file names to match the format
correct_name = True

# Date/file name pattern expected.
name_pattern='[1-2]\d{3}[0-1]\d[0-3]\d_[0-2]\d[0-6]\d[0-6]\d_*.*'

# Reports config
#--------------------------------------

# Reports to produce
reports=[
    {'file':'all_photos.csv', 'subpath':'ALBUM FINAL'},
    {'file':'instagram.csv', 'subpath':'_instagram\IG_done'}
]


# Tags map for the csv file. Path, Name and DateTime are automatically taken
# The rest of the tags are taken from map.
# In case more than one tag is specified, the first existing one will be taken
# https://exiftool.org/TagNames/EXIF.html
ExifDict={'Path':[],'Name':[],'DateTime':[],
          'Maker':['Make'],
          'Model':['Model'],
          'FocalLength':['FocalLength'],
          'FocalLengthIn35mmFilm':['FocalLengthIn35mmFilm'],
          'Aperture':['FNumber','MaxApertureValue'],
          'ExposureTime':['ExposureTime'],
          'ExposureBiasValue':['ExposureBiasValue'],
          'ISO': ['ISOSpeedRatings'],
          'Orientation':['Orientation'],
          'Flash':['Flash'],
          'MeteringMode':['MeteringMode'],
          'ExifImageWidth':['ExifImageWidth'],
          'ExifImageHeight':['ExifImageHeight']}


# Extra config
#--------------------------------------

# Conversion to 35mm
# ratio of conversion to 35mm, fill with your used models
conversion_to_35mm={
    'OLYMPUS IMAGING CORP.::E-500':2,
    'OLYMPUS IMAGING CORP.::E-620':2,
    'FUJIFILM::FinePix F30':3,
    'OLYMPUS IMAGING CORP.::E-410':2,
    'RICOH::Caplio GX100': 4.71,
    'NIKON::E4300':4.75,
    'Panasonic::DMC-FX10':6,
    'FUJIFILM::FinePix S6500fd': 6.5,
    'NIKON::COOLPIX S220': 5.56,
    'Canon::Canon PowerShot A400' : 7.63,
    'Canon::Canon EOS DIGITAL REBEL': 1.6,
    'NIKON::E3200':6.55,
    'FUJIFILM::FinePix F460': 6.03,
    'Canon::Canon EOS 5D': 1,
    'OLYMPUS IMAGING CORP.::E-PL1':2,
    'OLYMPUS IMAGING CORP.::E-P1': 2,
    'FUJIFILM::FinePix X100' : 1.5,
    'Canon::Canon PowerShot S90':4.67
}