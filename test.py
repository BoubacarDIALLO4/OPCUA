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
    myrootdir = '/mnt/d/AIVI_FCM/MSA4/'
    seen = []


    for dir,_,filenames in os.walk(myrootdir):
        for filename in filenames:
            if filename.endswith('.json'):
               files.extend(glob(os.path.join(dir,filename)))

    for file in files:
        barcode = os.path.basename(file).split("_")[1]
        if barcode not in seen:
            seen.append(barcode)
            #print(f' barcode first : {barcode}')

    return seen

ap = get_barcode_from_fake_images()
print(ap)
print(len(ap))