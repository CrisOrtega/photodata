import config
import sys
import os
import re
import csv
import various

from debug import Debug
from camerashot import CameraShot


# Function to go over the folder tree in order to look for images
# Supported formats: config.supported_formats
# attributes: path, supported_formats, file(CSV)
def walk_photo_folder(path,file,dbg=None):

    #open file csv (it will remains open)
    # and declare writer
    filehandle=open(file,'w',newline='')
    writer = csv.DictWriter(filehandle, fieldnames=config.ExifDict.keys(),delimiter=';')
    writer.writeheader()

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
            result=re.search(extension,f)
            name_file_tuple=(result[1],result[2])
            if len(name_file_tuple) != 2:
                dbg.msg('warning', 'extension', 'not supported',2, f,'Not a file?',"lenght:"+
                        str(len(name_file_tuple)))
            elif name_file_tuple[1].lower() not in config.supported_formats:
                dbg.msg('warning', 'extension', 'not supported', 2, f,'Not the right extension:'+name_file_tuple[1])
            else:

                # path to the image or video
                try:
                    imagename = os.path.join(root,f)
                    shot = CameraShot(imagename)
                    shot.load_exif()
                except IOError as e:
                    dbg.msg('ERROR', 'file', 'opening', 3, e, root, f, name_target)

                datecapture=''
                # In case we are going to correct the file and the file has an incorrect name
                # START renaming routine
                if config.correct_name == True and re.search(config.name_pattern, name_file_tuple[0]) == None:
                    datecapture=shot.determine_shotdate()
                    if (datecapture != None):
                        # We will change the name from f to name_target
                        name_target="{}{}{}_{}{}{}.{}".format(datecapture[0:4],datecapture[5:7],datecapture[8:10],
                                                          datecapture[11:13],datecapture[14:16],datecapture[17:19],
                                                          name_file_tuple[1])
                        i=1
                        while (os.path.exists(os.path.join(root,name_target))):
                            i+=1
                            name_target = "{}{}{}_{}{}{}_{}.{}".format(datecapture[0:4], datecapture[5:7],
                                                                    datecapture[8:10],
                                                                    datecapture[11:13], datecapture[14:16],
                                                                    datecapture[17:19],str(i),
                                                                    name_file_tuple[1])
                        if (os.path.exists(os.path.join(root,f)) and
                                not os.path.exists(os.path.join(root,name_target))):
                            dbg.msg('write', 'file', 'renaming', 2, root, f,name_target)
                            try:
                                os.rename(os.path.join(root,f),os.path.join(root,name_target))
                            except IOError as e:
                                dbg.msg('ERROR', 'file', 'renaming', 3, e, root, f, name_target)
                                sys.exit(1)
                        else:
                            dbg.msg('ERROR', 'file', 'renaming process error', 3, root, f,name_target)
                            sys.exit(1)

                    else:
                        dbg.msg('warning', 'file', 'no valid date', 2, root,f)
                # END renaming routine


                # Now, I build a dictionary for all images
                dict={}
                # Create dict

                for item in config.ExifDict.keys():
                    if item == 'Path':
                        dict[item] = various.latin1_to_ascii(root)
                        continue
                    if item == 'Name':
                        dict[item] = f
                        continue
                    # Write date
                    if item == 'DateTime':
                        dict[item] = datecapture
                        continue
                    # Fill fields and convert
                    for exifpointer in config.ExifDict[item]:
                        if exifpointer in shot.exifdata.keys():
                            if str(shot.exifdata[exifpointer]).strip not in ('',None):
                                dict[item]=str(shot.exifdata[exifpointer]).strip()
                                break
                            else:
                                dict[item]='NA'
                        else:
                            dict[item] = 'NA'

                # file for data is already open. Use 'writer' to write
                #append line
                writer.writerow(dict)


    #close csv file
    filehandle.close()




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




