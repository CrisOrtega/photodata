from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import os
import re



class CameraShot:
    def __init__(self,imagename):
        self.imagename=imagename
        self.dt_creation = '0000:00:00 00:00:00'
        self.dt_modification = '0000:00:00 00:00:00'
        self.datecapture = '9999:99:99 99:99:99'
        self.exifdata={}
        self.exitloaded=False

    def load_exif(self):
        self.exitloaded=True
        # read the image data using PIL
        try:
            # We can control the decompression image bomb warning
            # This is a risk, but I assume we are processing our own images
            #Image.MAX_IMAGE_PIXELS = None
            Image.MAX_IMAGE_PIXELS = 200000000
            image = Image.open(self.imagename)
            # extract EXIF data
            exifdata = image.getexif()
        except IOError as e:
           print('Error loading: {} {} '.format(self.imagename,e))
        # iterating over all EXIF data fields
        ## BETTER TAKE THIS TO A CLASS ...
        for tag_id in exifdata:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                try:
                    data = data.decode()
                except:
                    data = ''
            self.exifdata[tag]=data

    def determine_shotdate(self):
        if not self.exitloaded:
            self.load_exif()
        creation_timestamp = os.path.getctime(self.imagename)
        modification_timestamp = os.path.getmtime(self.imagename)
        self.dt_creation = datetime.fromtimestamp(creation_timestamp).strftime('%Y:%m:%d %H:%M:%S')
        self.dt_modification = datetime.fromtimestamp(modification_timestamp).strftime('%Y:%m:%d %H:%M:%S')
        pattern=r"([1-2]\d{3}:[0-1]\d:[0-3]\d [0-2]\d:[0-6]\d:[0-6]\d)"
        res=re.findall(pattern,self.dt_creation)
        if res != None and res[0] < self.datecapture:
            self.datecapture = res[0]
        res = re.search(pattern, self.dt_modification)
        if res != None and res[0] < self.datecapture:
            self.datecapture = res[0]
        if 'DateTimeOriginal' in self.exifdata.keys():
            res = re.search(pattern, str(self.exifdata['DateTimeOriginal']))
            if res != None and res[0] < self.datecapture:
                self.datecapture = res[0]
        if  'DateTime' in self.exifdata.keys():
            res = re.search(pattern, str(self.exifdata['DateTime']))
            if res != None and res[0] < self.datecapture:
                self.datecapture = res[0]
        if self.datecapture == '9999:99:99 99:99:99':
            return None
        return self.datecapture