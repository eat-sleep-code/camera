from picamera import PiCamera
import argparse
import datetime
import keyboard
import os
import sys
import subprocess
import time



parser = argparse.ArgumentParser()
parser.add_argument('--action', dest='action', help='Set the command action')
parser.add_argument('--shutter', dest='shutter', help='Set the shutter speed')
parser.add_argument('--iso', dest='iso', help='Set the ISO')
parser.add_argument('--ev', dest='ev', help='Set the exposure compensation (+/- 10)')
parser.add_argument('--awb', dest='awb', help='Set the Auto White Balance (AWB) mode')
parser.add_argument('--exposure', dest='exposure', help='Set the exposure mode')
parser.add_argument('--outputFolder', dest='outputFolder', help='Set the folder where images will be saved')
args = parser.parse_args()

action = args.action or "capture"
action = action.lower()

shutter = args.shutter or "auto"
if str(shutter).lower() == "auto" or str(shutter) == "0":
	shutter = 0
	print(" Shutter Speed: auto")
else:
	shutter = int(float(shutter) * 1000000)
	print(" Shutter Speed: " + str(shutter))


iso = args.iso or "auto"
if str(iso).lower() == "auto" or str(iso) == "0":
	iso = 0
	print(" ISO: auto")
else: 
	iso = int(iso)
	print(" ISO: " + str(iso))


exposure = (args.exposure or "auto").lower()
print(" Exposure Mode: " + exposure)


ev = args.ev or 0
ev = int(ev)
if ev > 0:
	print(" Exposure Compensation: +" + str(ev))
elif ev < 0:
	print(" Exposure Compensation: -" + str(ev))
else:
	print(" Exposure Compensation: +/-" + str(ev)) 


awb = (args.awb or "auto").lower()
print(" White Balance Mode: " + awb)


outputFolder = args.outputFolder or "dcim/"
if outputFolder.endswith('/') == False:
	outputFolder = outputFolder+"/"



def echoOff():
	subprocess.run(['stty', '-echo'], check=True)
def echoOn():
	subprocess.run(['stty', 'echo'], check=True)

try:
	echoOff()

	# === Initialize Camera ===
	camera = PiCamera()

	# === Image Capture Methods ===

	imageCount = 1

	def GetFileName():
		now = datetime.datetime.now()
		datestamp = now.strftime("%Y%m%d")
		return datestamp + "-" + str(imageCount).zfill(6) + ".jpg"


	def GetFilePath():
		try:
			os.makedirs(outputFolder, exist_ok = True)
		except OSError:
			print (" ERROR: Creation of the output folder %s failed." % path)
			echoOn()
			quit()
		else:
			return outputFolder + GetFileName()


	def CaptureImage():
		print("\n Press the [space] bar to take your photo ")
		try:
			camera.shutter_speed = shutter
		except: 
			print(" WARNING: Invalid Shutter Speed! ")

		try:	
			camera.iso = iso
		except: 
			print(" WARNING: Invalid ISO Setting! ")

		try:
			camera.exposure_mode = exposure
		except: 
			print(" WARNING: Invalid Exposure Mode! ")

		try:
			camera.exposure_compensation = ev
		except: 
			print(" WARNING: Invalid Exposure Compensation Setting! ")

		try:
			camera.awb_mode = awb
		except: 
			print(" WARNING: Invalid Auto White Balance Mode! ")
		
		camera.start_preview(fullscreen=False, window = (20, 20, 800, 600))
		
		print("Key Pressed: " + keyboard.read_hotkey())
		while True:
			try:
				if keyboard.is_pressed('ctrl+c') or keyboard.is_pressed('esc'):
					break
				elif keyboard.is_pressed('space'):
					print("\n Capturing image... ")
					camera.capture(outputFolder + GetFileName())
					echoOn()
					break
			except Exception as ex:
				print(ex)
				pass


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


	print(" Action: " + action)
	if action == "capture" or action=="image" or action=="captureimage":
		CaptureImage()


except KeyboardInterrupt:
	echoOn()
	sys.exit(1)
