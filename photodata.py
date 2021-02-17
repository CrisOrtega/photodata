import config
import os
from debug import Debug

# Function to go over the folder tree in order to look for images
# Supported formats: config.supported_formats
# attributes: path, supported_formats, file(CSV)
def walk_photo_folder(path,formats,file,dbg=None):
    for root, dirs, files in os.walk(path):
        # root stores root folder for first iteration
        # dirs stores folders inside the root
        # files stores files inside the root
        path_elements = root.split(os.sep)
        # I use the splat (*) operator to give the route of the folder and the name of folder separately
        dbg.msg('read','folder',os.path.join(*path_elements[:-1]),os.path.basename(root))
        for f in files:
            dbg.msg('read', 'file', os.path.basename(root),f)
            # type =
            # type in suported formats
            ## do my thing
            ## Read the attributes
            ## is the name correct? autocorrect name? then correct name
            ## Prepare record and append in the file
            # not in suported formats
            ## report



# Function to read the metadata of a specific file
# Fields reads: config.metadata_fields
# attributes: file_path
# return image_class

# We define the debuger
dbg = Debug(os.path.basename(__file__))
dbg.msg('config','path','all_photos',config.PATH)

# output csv
output_csv = os.path.join(config.PATH, 'photo_ddbb.csv')
dbg.msg('config','file','output_csv',output_csv)

walk_photo_folder(config.PATH,config.supported_formats,output_csv,dbg)




