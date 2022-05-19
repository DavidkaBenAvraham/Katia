import os
import shutil

from ini_files_dir import Ini
import execute_json as json


##https://vivazzi.pro/it/remove-file/
#import os
#import shutil

#def delete_files_from_tree(path, file_name):
#    files = os.listdir(path)
#    for f in files:
#        p = os.path.join(path, f)
#        if os.path.isdir(p):
#            print p
#            if f == file_name:
#                shutil.rmtree(p, True)
#            else:
#                delete_files_from_tree(p, file_name)
#        else:
#            if f == file_name:
#                os.remove(p)


def clear_product_images_folder():
    path  = json.load('filemanager.json')['prestashop']['local_productimages_directory']

    files = os.listdir(path)
    for f in files:
        p = os.path.join(path, f)
        if os.path.isdir(p):
            print(p)
            if f == file_name:
                shutil.rmtree(p, True)
            else:
                delete_files_from_tree(p, file_name)
        else:
            if f == file_name:
                os.remove(p)