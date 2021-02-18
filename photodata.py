import config
import sys
import os
import re
from PIL import Image
from PIL.ExifTags import TAGS
from debug import Debug
from datetime import datetime

# Function to go over the folder tree in order to look for images
# Supported formats: config.supported_formats
# attributes: path, supported_formats, file(CSV)
def walk_photo_folder(path,file,dbg=None):
    for root, dirs, files in os.walk(path):
        # root stores root folder for first iteration
        # dirs stores folders inside the root
        # files stores files inside the root
        path_elements = root.split(os.sep)
        # I use the splat (*) operator to give the route of the folder and the name of folder separately
        dbg.msg('read','folder',os.path.join(*path_elements[:-1]),1,os.path.basename(root))
        for f in files:
            dbg.msg('read', 'file', os.path.basename(root),1,f)
            extension=r"(^.+)\.(\w+)$"
            result=re.findall(extension,f)
            name_file_tuple=result[0]
            if len(name_file_tuple) != 2:
                dbg.msg('warning', 'extension', 'not supported',2, f,'Not a file?',"lenght:"+
                        str(len(name_file_tuple)))
            elif name_file_tuple[1].lower() not in config.supported_formats:
                dbg.msg('warning', 'extension', 'not supported', 2, f,'Not the right extension:'+name_file_tuple[1])
            else:

                # path to the image or video
                imagename = os.path.join(root,f)
                print(imagename)

                creation_timestamp = os.path.getctime(imagename)
                modification_timestamp = os.path.getmtime(imagename)
                dt_creation = datetime.fromtimestamp(creation_timestamp).strftime('%Y:%m:%d %H:%M:%S')
                dt_modification = datetime.fromtimestamp(modification_timestamp).strftime('%Y:%m:%d %H:%M:%S')
                print("dt_creation =", dt_creation)
                print("dt_modification =", dt_modification)

                # read the image data using PIL
                image = Image.open(imagename)
                # extract EXIF data
                exifdata = image.getexif()
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
                            data=''
                    print(f"{tag:25}: {data}")
                ## is the name correct? autocorrect name? then correct name
                ## Prepare record and append in the file



# Function to read the metadata of a specific file
# Fields reads: config.metadata_fields
# attributes: file_path
# return image_class

# We define the debuger
dbg = Debug(os.path.basename(__file__),level=2)
dbg.msg('Version','sys.version','sys.version',1,sys.version)
dbg.msg('config','path','all_photos',1,config.PATH)

# output csv
output_csv = os.path.join(config.PATH, 'photo_ddbb.csv')
dbg.msg('config','file','output_csv',1,output_csv)

walk_photo_folder(config.PATH,output_csv,dbg)




