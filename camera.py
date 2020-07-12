import os
import argparse
import time
import datetime

parser = argparse.ArgumentParser()
parser.addArgument('--exposure', dest='exposure', help='Set the exposure mode')
parser.addArgument('--iso', dest='iso', help='Set the ISO')
parser.addArgument('--ev', dest='ev', help='Set the exposure compensation (+/- 10)')
parser.addArgument('--awb', dest='awb', help='Set the Auto White Balance (AWB) mode')
parser.add_argument('--outputFolder', dest='outputFolder', help='Folder where images will be saved')
args = parser.parse_args

exposure = args.exposure or "auto"
iso = args.iso or 100
ev = args.ev = 0
awb = args.awb or "auto"
outputFolder = outputFolder or "dcim/"

imageCount = 1

def GetFileName():
    now = datetime.datetime.now()
    datestamp = now.strftime("%Y%m%d")
    return datestamp + "-" + str(imageCount).zfill(6) + ".jpg"

def CaptureImage():
    os.system("raspistill --thumb none --iso " + iso + " --exposure " + exposure + " --ev " + ev + " --awb " + awb + " -o " + GetFileName())

def UploadImage():
    print("Not yet implemented")

def CreateTimelapse(interval = 5000):
    while True: 
        CaptureImage()
        imageCount += 1
        time.sleep(interval)

def CaptureAndUploadImage():
    CaptureImage()
    time.sleep(1000)
    UploadImage()

