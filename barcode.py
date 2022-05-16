import os
from glob import glob
from collections import defaultdict
import re
import shutil


def get_barcode_from_fake_images() -> list:

    #fake_images_path = os.getenv('FAKE_IMAGES_DIR')
    #print(os.environ.get['FAKE_IMAGES_DIR'])
    files = []
    #myrootdir = os.getcwd()
    myrootdir = '/mnt/d/AIVI_FCM/MSA3/'
    seen = []


    for dir,_,filenames in os.walk(myrootdir):
        for filename in filenames:
            if filename.endswith('.jpeg'):
               files.extend(glob(os.path.join(dir,filename)))

    for file in files:
        barcode = os.path.basename(file).split("_")[1]
        if barcode not in seen:
            seen.append(barcode)
            #print(f' barcode first : {barcode}')

    return seen

ap = get_barcode_from_fake_images()
print(type(ap))

# count = 0
# for i in ap:
#     print(i)
#     count = count + 1
#     #print(count)
myroot = '/mnt/d/AIVI_FCM/MSA3/'
bouba = '/mnt/d/AIVI_FCM/'
regex = '218399105J201218083809'


for root, dirs, filles in os.walk(myroot):
    for fil in filles:
        #print(fil)
        filname = os.path.basename(fil[0])
        split_file = os.path.basename(fil).split("_")
        
        if regex in split_file:
            print(fil)
            shutil.copyfile(fil, bouba + fil)
            #shutil.copyfile(fil[0], os.path.join(bouba, filname))

