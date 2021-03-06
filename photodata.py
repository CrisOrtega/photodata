import sys
import os
import re
import csv

import config
import various
from debug import Debug
from camerashot import CameraShot
from datetime import datetime

# Function to go over the folder tree in order to look for images
# Supported formats: config.supported_formats
# attributes: path, supported_formats, file(CSV)
def create_report(path, file, dbg=None):


    if not os.path.exists(path):
        raise ValueError("PATH: {} not existing".format(path))
    # open file csv (it will remains open)
    # and declare writer
    filehandle = open(file, 'w', newline='')
    writer = csv.DictWriter(filehandle, fieldnames=config.ExifDict.keys(), delimiter=';')
    writer.writeheader()

    # Create dict for final report and exceptions
    # We are going to make the script to return the exceptions
    final_report = {}
    final_report['ok']={}
    final_report['exception']={}


    for root, dirs, files in os.walk(path):
        # root stores root folder for first iteration
        # dirs stores folders inside the root
        # files stores files inside the root
        path_elements = root.split(os.sep)
        # I use the splat (*) operator to give the route of the folder and the name of folder separately
        dbg.msg('read', 'folder', os.path.join(*path_elements[:-1]), 1, os.path.basename(root))
        for f in files:
            dbg.msg('read', 'file', os.path.basename(root), 1, f)
            extension = r"(^.+)\.(\w+)$"
            result = re.search(extension, f)
            name_file_tuple = (result[1], result[2])
            if len(name_file_tuple) != 2:
                dbg.msg('warning', 'extension', 'not supported', 2, f, 'Not a file?', "lenght:" +
                        str(len(name_file_tuple)))
            elif name_file_tuple[1].lower() not in config.supported_formats:
                dbg.msg('warning', 'extension', 'not supported', 1, f, 'extension not supported:' + name_file_tuple[1])
            else:

                # path to the image or video
                try:
                    imagename = os.path.join(root, f)
                    shot = CameraShot(imagename)
                    shot.load_exif()
                except IOError as e:
                    dbg.msg('ERROR', 'file', 'opening', 3, e, root, f)
                    raise ValueError("Image could not be open")

                # This is the date in which I determine that the shot was taken
                datecapture = shot.determine_shotdate()

                # Now, I build a dictionary for all images
                dict = {}
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
                        # We will output the date in the format given by the configuration
                        # we will use this field.
                        datecapturereport=""
                        # First we convert datecapture to datetime (if the format is correct)
                        pattern = r"([1-2]\d{3}:[0-1]\d:[0-3]\d [0-2]\d:[0-6]\d:[0-6]\d)"
                        res = re.findall(pattern, datecapture)
                        if res != None:
                            date_time_obj = datetime.strptime(datecapture, '%Y:%m:%d %H:%M:%S')
                            # Then we convert it back to datetime with the new format
                            datecapturereport = \
                                date_time_obj.strftime(config.date_format_report)
                        dict[item] = datecapturereport
                        continue
                    # Fill fields and convert
                    default = ''
                    if (item == 'Model' or item == 'Maker'):
                        default = 'Unknown'

                    for exifpointer in config.ExifDict[item]:
                        if exifpointer in shot.exifdata.keys():
                            if str(shot.exifdata[exifpointer]).strip not in ('', None):
                                dict[item] = str(shot.exifdata[exifpointer]).strip()
                                break
                            else:
                                dict[item] = default
                        else:
                            dict[item] = default
                makermodel = "{}::{}".format(dict["Maker"], dict["Model"])
                if dict['FocalLengthIn35mmFilm'] == '' and dict['FocalLength'] != '':
                    if makermodel in config.conversion_to_35mm.keys():
                        try:
                            dict['FocalLengthIn35mmFilm'] = round(float(dict['FocalLength'])
                                                                  * float(config.conversion_to_35mm[makermodel]))
                        except Exception as e:
                            dbg.msg('Warning', 'exif', 'wrong coversion', 2, e, makermodel, dict['FocalLength'])
                        # write in final report
                        final_report['ok'][makermodel] = final_report['ok'].get(makermodel, 0) + 1
                    else:
                        dbg.msg('Warning', 'exif', 'no data coversion', 2, makermodel, dict['FocalLength'])
                        final_report['exception'][makermodel] = final_report['exception'].get(makermodel, 0) + 1


                # file for data is already open. Use 'writer' to write
                # append line
                writer.writerow(dict)

    # close csv file
    filehandle.close()

    return final_report


def name_correction(path, dbg=None):
    if not os.path.exists(path):
        raise ValueError("PATH: {} not existing".format(path))

    for root, dirs, files in os.walk(path):
        # root stores root folder for first iteration
        # dirs stores folders inside the root
        # files stores files inside the root
        path_elements = root.split(os.sep)
        # I use the splat (*) operator to give the route of the folder and the name of folder separately
        dbg.msg('read', 'folder', os.path.join(*path_elements[:-1]), 1, os.path.basename(root))
        for f in files:
            dbg.msg('read', 'file', os.path.basename(root), 1, f)
            extension = r"(^.+)\.(\w+)$"
            result = re.search(extension, f)
            name_file_tuple = (result[1], result[2])
            if len(name_file_tuple) != 2:
                dbg.msg('warning', 'extension', 'not supported', 2, f, 'Not a file?', "lenght:" +
                        str(len(name_file_tuple)))
            elif name_file_tuple[1].lower() not in config.supported_formats:
                dbg.msg('warning', 'extension', 'not supported', 1, f,
                        'Not the right extension:' + name_file_tuple[1])
            else:

                # path to the image or video
                try:
                    imagename = os.path.join(root, f)
                    shot = CameraShot(imagename)
                    shot.load_exif()
                except IOError as e:
                    dbg.msg('ERROR', 'file', 'opening', 3, e, root, f)
                    raise ValueError("Image could not be open")

                datecapture = ''
                # In case we are going to correct the file and the file has an incorrect name

                # START renaming routine
                if config.correct_name == True and re.search(config.name_pattern, name_file_tuple[0]) == None:
                    datecapture = shot.determine_shotdate()
                    if (datecapture != None):
                        # We will change the name from f to name_target
                        name_target = "{}{}{}_{}{}{}.{}".format(datecapture[0:4], datecapture[5:7],
                                                                datecapture[8:10],
                                                                datecapture[11:13], datecapture[14:16],
                                                                datecapture[17:19],
                                                                name_file_tuple[1])
                        i = 1
                        while (os.path.exists(os.path.join(root, name_target))):
                            i += 1
                            name_target = "{}{}{}_{}{}{}_{}.{}".format(datecapture[0:4], datecapture[5:7],
                                                                       datecapture[8:10],
                                                                       datecapture[11:13], datecapture[14:16],
                                                                       datecapture[17:19], str(i),
                                                                       name_file_tuple[1])
                        if (os.path.exists(os.path.join(root, f)) and
                                not os.path.exists(os.path.join(root, name_target))):
                            dbg.msg('write', 'file', 'renaming', 2, root, f, name_target)
                            try:
                                os.rename(os.path.join(root, f), os.path.join(root, name_target))
                            except IOError as e:
                                dbg.msg('ERROR', 'file', 'renaming', 3, e, root, f, name_target)
                                raise ValueError("Rename failed")
                        else:
                            dbg.msg('ERROR', 'file', 'renaming process error', 3, root, f, name_target)
                            raise ValueError("Renaming process error")

                    else:
                        dbg.msg('warning', 'file', 'no valid date', 2, root, f)
                # END renaming routine
    return True


def other_tables(path):
    if not os.path.exists(path):
        raise ValueError("PATH: {} not existing".format(path))
    # File with models
    # open file csv (it will remains open)
    # and declare writer
    file = os.path.join(path, 'camera_conversion.csv')
    filehead = {'Model', 'ConversionRatio'}
    filehandle = open(file, 'w', newline='')
    writer = csv.DictWriter(filehandle, fieldnames=filehead, delimiter=';')
    writer.writeheader()
    values = []
    for model, value in config.conversion_to_35mm.items():
        values.append({'Model': model, 'ConversionRatio': value})
    writer.writerows(values)
    # close csv file
    filehandle.close()


def draw_report(report,path):
    print()
    print("***************************************")
    print("Printing results for: {}".format(path))
    print("***************************************")
    # sorting the results of the ok - stats
    # sorting the results of the exceptions
    print("Folder stats:")
    print("------------------------------------")
    stats_report={k: v for k, v in sorted(report['ok'].items(), key=lambda item: item[1],reverse=True)}
    for key,value in stats_report.items():
        print("{:>40}{:>10}".format(key, value))
    print("Exceptions:")
    print("------------------------------------")
    stats_report = {k: v for k, v in sorted(report['exception'].items(), key=lambda item: item[1],reverse=True)}
    if len(stats_report)>0:
        for key, value in stats_report.items():
            print("{:>40}{:>10}".format(key, value))
    else:
        print("No Exceptions")


def main():
    # We define the debuger
    dbg = Debug(os.path.basename(__file__), level=2)
    dbg.msg('Version', 'sys.version', 'sys.version', 1, sys.version)

    dbg.msg('config', 'path', 'all_photos', 1, config.PATH)

    if os.path.exists(config.PATH):
        other_tables(config.PATH)
        if config.correct_name:
            name_correction(config.PATH, dbg)
        for report in config.reports:
            file_report = os.path.join(config.PATH, report['file'])
            subpath = os.path.join(config.PATH, report['subpath'])
            dbg.msg('report', 'file', 'output_csv', 1, subpath, file_report)
            assert os.path.exists(subpath), "{} doesn't exist".format(subpath)
            quickresult = create_report(subpath, file_report, dbg)
            draw_report(quickresult,subpath)
    else:
        dbg.msg('config', 'path', 'all_photos', 3, config.PATH)
        raise ValueError("A correct folder needs to be specified")


if __name__ == "__main__":
    main()
