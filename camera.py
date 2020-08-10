from picamera import PiCamera
from pydng.core import RPICAM2DNG
import threading
import argparse
import datetime
import keyboard
import os
import sys
import subprocess
import time

camera = PiCamera()
dng = RPICAM2DNG()

version = "2020.08.10"

# === Argument Handling ========================================================

parser = argparse.ArgumentParser()
parser.add_argument('--action', dest='action', help='Set the command action')
parser.add_argument('--shutter', dest='shutter', help='Set the shutter speed')
parser.add_argument('--iso', dest='iso', help='Set the ISO')
parser.add_argument('--exposure', dest='exposure', help='Set the exposure mode')
parser.add_argument('--ev', dest='ev', help='Set the exposure compensation (+/-25)')
parser.add_argument('--bracket', dest='bracket', help='Set the exposure bracketing value')
parser.add_argument('--awb', dest='awb', help='Set the Auto White Balance (AWB) mode')
parser.add_argument('--outputFolder', dest='outputFolder', help='Set the folder where images will be saved')
parser.add_argument('--raw', dest='raw', help='Set whether DNG files are created in addition to JPEG files')
parser.add_argument('--timer', dest='timer', help='Set self-timer or interval')
parser.add_argument('--previewWidth', dest='previewWidth', help='Set the preview window width')
parser.add_argument('--previewHeight', dest='previewHeight', help='Set the preview window height')
args = parser.parse_args()
	
previewVisible = False
try:
	previewWidth = args.previewWidth or 800
	previewWidth = int(previewWidth)
	previewHeight = args.previewHeight or 600
	previewHeight = int(previewHeight)
except: 
	previewWidth = 800
	previewHeight = 600
	

action = args.action or "capture"
action = action.lower()


shutter = args.shutter or "auto"
shutterLong = 32000
shutterShort = 100


iso = args.iso or "auto"
isoMin = 100
isoMax = 1600


exposure = (args.exposure or "auto").lower()


ev = args.ev or 0
evMin = -25
evMax = 25


bracket = args.bracket or 0
bracketLow = 0
bracketHigh = 0


awb = (args.awb or "auto").lower()


outputFolder = args.outputFolder or "dcim/"
if outputFolder.endswith('/') == False:
	outputFolder = outputFolder+"/"


timer = args.timer or 0
timer = int(timer)


raw = args.raw or True


# === Echo Control =============================================================

def echoOff():
	subprocess.run(['stty', '-echo'], check=True)
def echoOn():
	subprocess.run(['stty', 'echo'], check=True)
def clear():
	subprocess.call('clear' if os.name == 'posix' else 'cls')
clear()


# === Functions ================================================================

def showInstructions(clearFirst = False, wait = 0):
	if clearFirst == True:
		clear()
	else:
		print(" ----------------------------------------------------------------------")

	print("\n Press s+\u25B2 or s+\u25BC to change shutter speed")
	print("\n Press i+\u25B2 or i+\u25BC to change ISO")
	print("\n Press c+\u25B2 or c+\u25BC to change exposure compensation")
	print("\n Press b+\u25B2 or b+\u25BC to change exposure bracketing")
	print("\n Press [p] to toggle the preview window")

	if action == "timelapse":			 		
		print("\n Press the [space] bar to begin a timelapse ")
	else:
		print("\n Press the [space] bar to take photos ")

	print("\n Press \u241B to exit ")
	time.sleep(wait)
	return

# ------------------------------------------------------------------------------

def setShutter(input, wait = 0):
	global shutter
	global shutterLong
	global shutterShort

	if str(input).lower() == "auto" or str(input) == "0":
		shutter = 0
	else:
		shutter = int(float(input))
		if shutter < shutterShort:
			shutter = shutterShort
		elif shutter > shutterLong:
			shutter = shutterLong 
	try:
		camera.shutter_speed = shutter
		# print(str(camera.shutter_speed) + "|" + str(shutter))
		if shutter == 0:
			print(" Shutter Speed: auto")
		else:	
			print(" Shutter Speed: " + str(shutter))
		time.sleep(wait)
		return
	except: 
		print(" WARNING: Invalid Shutter Speed! ")

# ------------------------------------------------------------------------------				

def setISO(input, wait = 0):
	global iso
	global isoMin
	global isoMax
	if str(input).lower() == "auto" or str(input) == "0":
		iso = 0
	else: 
		iso = int(input)
		if iso < isoMin:	
			iso = isoMin
		elif iso > isoMax:
			iso = isoMax	
	try:	
		camera.iso = iso
		# print(str(camera.iso) + "|" + str(iso))
		if iso == 0:
			print(" ISO: auto")
		else:	
			print(" ISO: " + str(iso))
		time.sleep(wait)
		return
	except: 
		print(" WARNING: Invalid ISO Setting! " + iso)

# ------------------------------------------------------------------------------

def setExposure(input, wait = 0):
	global exposure
	exposure = input
	try:	
		camera.exposure_mode = exposure
		print(" Exposure Mode: " + exposure)
		time.sleep(wait)
		return
	except: 
		print(" WARNING: Invalid Exposure Mode! ")
				
# ------------------------------------------------------------------------------

def setEV(input, wait = 0, displayMessage = True):
	global ev 
	global bracket
	ev = input
	ev = int(ev)
	evPrefix = "+/-"
	if ev > 0:
		evPrefix = "+"
	elif ev < 0:
		evPrefix = ""
	try:
		camera.exposure_compensation = ev
		# print(str(camera.exposure_compensation) + "|" + str(ev))
		if displayMessage == True:
			print(" Exposure Compensation: " + evPrefix + str(ev))
		time.sleep(wait)
		return
	except: 
		print(" WARNING: Invalid Exposure Compensation Setting! ")	
		
# ------------------------------------------------------------------------------				

def setBracket(input, wait = 0, displayMessage = True):
	global bracket
	global bracketLow
	global bracketHigh
	global evMax
	global evMin
	bracket = int(input)
	try:
		bracketLow = camera.exposure_compensation - bracket
		if bracketLow < evMin:
			bracketLow = evMin
		bracketHigh = camera.exposure_compensation + bracket
		if bracketHigh > evMax:
			bracketHigh = evMax
		if displayMessage == True:
			print(" Exposure Bracketing: " + str(bracket))
		time.sleep(wait)
		return
	except: 
		print(" WARNING: Invalid Exposure Bracketing Value! ")

# ------------------------------------------------------------------------------

def setAWB(input, wait = 0):
	global awb
	awb = input
	try:	
		camera.awb_mode = awb
		print(" White Balance Mode: " + awb)
		time.sleep(wait)
		return
	except: 
		print(" WARNING: Invalid Auto White Balance Mode! ")

# ------------------------------------------------------------------------------

def GetFileName(timestamped = True):
	now = datetime.datetime.now()
	datestamp = now.strftime("%Y%m%d")
	if timestamped == True:
		timestamp = now.strftime("%H%M")
		return datestamp + "-" + timestamp + "-" + str(imageCount).zfill(3) + ".jpg"
	else:
		return datestamp + "-" + timestamp + "-" + str(imageCount).zfill(8) + ".jpg"

# ------------------------------------------------------------------------------

def GetFilePath(timestamped = True):
	try:
		os.makedirs(outputFolder, exist_ok = True)
	except OSError:
		print (" ERROR: Creation of the output folder %s failed." % path)
		echoOn()
		quit()
	else:
		return outputFolder + GetFileName(timestamped)

# ------------------------------------------------------------------------------

def showPreview(x = 0, y = 0, w = 800, h = 600):
	global previewVisible
	camera.start_preview(fullscreen=False, window = (x, y, w, h))	
	previewVisible = True;
	time.sleep(0.1)
	return
	
# ------------------------------------------------------------------------------

def hidePreview():
	global previewVisible
	camera.stop_preview()
	previewVisible = False;
	time.sleep(0.1)
	return

# ------------------------------------------------------------------------------

def captureImage(filepath, raw = True):
	camera.capture(filepath, quality=100, bayer=raw)
	t = threading.Thread(target=captureImageThreaded, args=(filepath, raw,))
	t.start()

# ------------------------------------------------------------------------------		

def captureImageThreaded(filepath, raw = True):
	if raw == True:
		dng.convert(filepath)

# === Image Capture ============================================================

try:
	echoOff()
	imageCount = 1
	
	def Capture(mode = "persistent", timer = 0):
		# print(str(camera.resolution))
		camera.resolution = (4056, 3040)
	
		global previewVisible
		global previewWidth
		global previewHeight
		global shutter
		global shutterLong
		global shutterShort
		global iso
		global isoMin
		global isoMax
		global exposure
		global ev
		global evMin
		global evMax
		global bracket
		global awb
		global raw
		global imageCount

		print("\n Camera " + version )
		print("\n ----------------------------------------------------------------------")
		
		setShutter(shutter, 0)		
		setISO(iso, 0)
		setExposure(exposure, 0)
		setEV(ev, 0)
		setBracket(bracket, 0)
		setAWB(awb, 0)
		
		showInstructions(False, 0)
		showPreview(0, 0, previewWidth, previewHeight)
		
		
		# print("Key Pressed: " + keyboard.read_hotkey())
		while True:
			try:
				if keyboard.is_pressed('ctrl+c') or keyboard.is_pressed('esc'):
					# clear()
					echoOn()
					break

				# Help
				elif keyboard.is_pressed('/') or keyboard.is_pressed('shift+/'):
					showInstructions(True, 0.5)	

				# Capture
				elif keyboard.is_pressed('space'):
					
					if mode == "persistent":
						# Normal photo
						filepath = GetFilePath(True)
						print(" Capturing image: " + filepath + "\n")
						captureImage(filepath, raw)
						imageCount += 1
				
						if (bracket != 0):
							baseEV = ev
							# Take underexposed photo
							setEV(baseEV + bracketLow, 0, False)
							filepath = GetFilePath(True)
							print(" Capturing image: " + filepath + "  [" + str(bracketLow) + "]\n")
							captureImage(filepath, raw)
							imageCount += 1

							# Take overexposed photo
							setEV(baseEV + bracketHigh, 0, False)
							filepath = GetFilePath(True)
							print(" Capturing image: " + filepath + "  [" + str(bracketHigh) + "]\n")
							captureImage(filepath, raw)
							imageCount += 1						
							
							# Reset EV to base photo's value
							setEV(baseEV, 0, False)
							
					elif mode == "timelapse":
						# Timelapse photo series
						if timer < 0:
							timer = 1
						while True:
							filepath = GetFilePath(True)
							print(" Capturing timelapse image: " + filepath + "\n")
							captureImage(filepath, raw)
							imageCount += 1
							time.sleep(timer) 					
					else:
						# Single photo and then exit
						filepath = GetFilePath(True)
						print(" Capturing single image: " + filepath + "\n")
						captureImage(filepath, raw)
						echoOn()
						break

				# Preview Toggle				
				elif keyboard.is_pressed('p'):
					if previewVisible == True:
						hidePreview()
					else:
						showPreview(0, 0, previewWidth, previewHeight)

				# Shutter				
				elif keyboard.is_pressed('s+up'):
					if shutter == 0:
						shutter = shutterShort
					if shutter > shutterShort and shutter <= shutterLong:					
						shutter = int(shutter / 2)
					setShutter(shutter, 0.25)
				elif keyboard.is_pressed('s+down'):
					if shutter == 0:						
						shutter = shutterLong
					elif shutter < shutterLong and shutter >= shutterShort:					
						shutter = int(shutter * 2)
					elif shutter == shutterShort:
						shutter = 0
					setShutter(shutter, 0.25)

				# ISO
				elif keyboard.is_pressed('i+up'):
					if iso == 0:
						iso = isoMin
					if iso >= isoMin and iso < isoMax:					
						iso = int(iso * 2)
					setISO(iso, 0.25)
				elif keyboard.is_pressed('i+down'):
					if iso == 0:
						iso = isoMax
					elif iso <= isoMax and iso > isoMin:					
						iso = int(iso / 2)
					elif iso == isoMin:
						iso = 0
					setISO(iso, 0.25)

				# Exposure Compensation
				elif keyboard.is_pressed('c+up'):
					if ev >= evMin and ev < evMax:					
						ev = int(ev + 1)
						setEV(ev, 0.25)
				elif keyboard.is_pressed('c+down'):
					if ev <= evMax and ev > evMin:					
						ev = int(ev - 1)
						setEV(ev, 0.25)

				# Exposure Bracketing
				elif keyboard.is_pressed('b+up'):
					if bracket < evMax:
						bracket = int(bracket + 1)
						setBracket(bracket, 0.25)
				elif keyboard.is_pressed('b+down'):
					if bracket > 0:					
						bracket = int(bracket - 1)
						setBracket(bracket, 0.25)

			except Exception as ex:
				print(ex)
				pass


	def UploadImage():
		print(" INFO: Not yet implemented")


	def CaptureAndUploadImage():
		Capture()
		time.sleep(1000)
		UploadImage()


	# print(" Action: " + action)
	if action == "capture" or action == "image" or action == "photo":
		Capture()
	elif action == "capturesingle" or action == "single":
		Capture("single")
	elif action == "timelapse":
		Capture("timelapse", timer)


except KeyboardInterrupt:
	echoOn()
	sys.exit(1)
