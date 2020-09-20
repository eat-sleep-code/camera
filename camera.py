from picamera import PiCamera
from pydng.core import RPICAM2DNG
import threading
import argparse
import datetime
import fractions
import keyboard
import os
import sys
import subprocess
import time


version = '2020.09.20'

camera = PiCamera()
camera.resolution = camera.MAX_RESOLUTION
dng = RPICAM2DNG()


# === Argument Handling ========================================================

parser = argparse.ArgumentParser()
parser.add_argument('--action', dest='action', help='Set the command action')
parser.add_argument('--shutter', dest='shutter', help='Set the shutter speed (milliseconds)')
parser.add_argument('--iso', dest='iso', help='Set the ISO')
parser.add_argument('--exposure', dest='exposure', help='Set the exposure mode')
parser.add_argument('--ev', dest='ev', help='Set the exposure compensation (+/-25)')
parser.add_argument('--bracket', dest='bracket', help='Set the exposure bracketing value')
parser.add_argument('--awb', dest='awb', help='Set the Auto White Balance (AWB) mode')
parser.add_argument('--outputFolder', dest='outputFolder', help='Set the folder where images will be saved')
parser.add_argument('--raw', dest='raw', help='Set whether DNG files are created in addition to JPEG files')
parser.add_argument('--timer', dest='timer', help='Set self-timer or interval (seconds)')
parser.add_argument('--previewWidth', dest='previewWidth', help='Set the preview window width')
parser.add_argument('--previewHeight', dest='previewHeight', help='Set the preview window height')
args = parser.parse_args()
	
previewVisible = False
try:
	previewWidth = args.previewWidth or 800
	previewWidth = int(previewWidth)
	previewHeight = args.previewHeight or 600
	previewHeight = int(previewHeight)
except Exception as ex: 
	previewWidth = 800
	previewHeight = 600
	

action = args.action or 'capture'
action = action.lower()


shutter = args.shutter or 'auto'
shutterLong = 30000
shutterLongThreshold = 1000
shutterShort = 0
defaultFramerate = 30


iso = args.iso or 'auto'
isoMin = 100
isoMax = 1600


exposure = (args.exposure or 'auto').lower()


ev = args.ev or 0
evMin = -25
evMax = 25


bracket = args.bracket or 0
bracketLow = 0
bracketHigh = 0


awb = (args.awb or 'auto').lower()


outputFolder = args.outputFolder or 'dcim/'
if outputFolder.endswith('/') == False:
	outputFolder = outputFolder+'/'


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
		print(' ----------------------------------------------------------------------')

	print('\n Press s+\u25B2 or s+\u25BC to change shutter speed')
	print('\n Press i+\u25B2 or i+\u25BC to change ISO')
	print('\n Press c+\u25B2 or c+\u25BC to change exposure compensation')
	print('\n Press b+\u25B2 or b+\u25BC to change exposure bracketing')
	print('\n Press [p] to toggle the preview window')

	if action == 'timelapse':			 		
		print('\n Press the [space] bar to begin a timelapse ')
	else:
		print('\n Press the [space] bar to take photos ')

	print('\n Press \u241B to exit ')
	time.sleep(wait)
	return

# ------------------------------------------------------------------------------

def setShutter(input, wait = 0):
	global shutter
	global shutterLong
	global shutterLongThreshold
	global shutterShort
	global defaultFramerate
	
	if str(input).lower() == 'auto' or str(input) == '0':
		shutter = 0
	else:
		shutter = int(float(input))
		if shutter < shutterShort:
			shutter = shutterShort
		elif shutter > shutterLong:
			shutter = shutterLong 
	try:
		if camera.framerate == defaultFramerate and shutter > shutterLongThreshold:
			camera.framerate=fractions.Fraction(5, 1000)
		elif camera.framerate != defaultFramerate and shutter <= shutterLongThreshold:
			camera.framerate = defaultFramerate
	
		if shutter == 0:
			camera.shutter_speed = 0
			#print(str(camera.shutter_speed) + '|' + str(camera.framerate) + '|' + str(shutter))	
			print(' Shutter Speed: auto')
		else:
			camera.shutter_speed = shutter * 1000
			#print(str(camera.shutter_speed) + '|' + str(camera.framerate) + '|' + str(shutter))		
			floatingShutter = float(shutter/1000)
			roundedShutter = '{:.3f}'.format(floatingShutter)
			if shutter > shutterLongThreshold:
				print(' Shutter Speed: ' + str(roundedShutter)  + 's [Long Exposure Mode]')
			else:
				print(' Shutter Speed: ' + str(roundedShutter) + 's')
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Shutter Speed!' + str(shutter))

# ------------------------------------------------------------------------------				

def setISO(input, wait = 0):
	global iso
	global isoMin
	global isoMax
	if str(input).lower() == 'auto' or str(input) == '0':
		iso = 0
	else: 
		iso = int(input)
		if iso < isoMin:	
			iso = isoMin
		elif iso > isoMax:
			iso = isoMax	
	try:	
		camera.iso = iso
		#print(str(camera.iso) + '|' + str(iso))
		if iso == 0:
			print(' ISO: auto')
		else:	
			print(' ISO: ' + str(iso))
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid ISO Setting! ' + str(iso))

# ------------------------------------------------------------------------------

def setExposure(input, wait = 0):
	global exposure
	exposure = input
	try:	
		camera.exposure_mode = exposure
		print(' Exposure Mode: ' + exposure)
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Exposure Mode! ')
				
# ------------------------------------------------------------------------------

def setEV(input, wait = 0, displayMessage = True):
	global ev 
	global bracket
	ev = input
	ev = int(ev)
	evPrefix = '+/-'
	if ev > 0:
		evPrefix = '+'
	elif ev < 0:
		evPrefix = ''
	try:
		camera.exposure_compensation = ev
		# print(str(camera.exposure_compensation) + '|' + str(ev))
		if displayMessage == True:
			print(' Exposure Compensation: ' + evPrefix + str(ev))
		time.sleep(wait)
		return
	except Exception as ex: 
		print(' WARNING: Invalid Exposure Compensation Setting! ')	
		
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
			print(' Exposure Bracketing: ' + str(bracket))
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Exposure Bracketing Value! ')

# ------------------------------------------------------------------------------

def setAWB(input, wait = 0):
	global awb
	awb = input
	try:	
		camera.awb_mode = awb
		print(' White Balance Mode: ' + awb)
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Auto White Balance Mode! ')

# ------------------------------------------------------------------------------

def getFileName(timestamped = True, isVideo = False):
	now = datetime.datetime.now()
	datestamp = now.strftime('%Y%m%d')
	if isVideo==True:
		extension = '.h264'
	else:
		extension = '.jpg'
	if timestamped == True:
		timestamp = now.strftime('%H%M%S')
		return datestamp + '-' + timestamp + '-' + str(imageCount).zfill(2) + extension
	else:
		return datestamp + '-' + str(imageCount).zfill(8) + extension

# ------------------------------------------------------------------------------

def getFilePath(timestamped = True, isVideo = False):
	try:
		os.makedirs(outputFolder, exist_ok = True)
	except OSError:
		print (' ERROR: Creation of the output folder ' + outputFolder + ' failed! ')
		echoOn()
		quit()
	else:
		return outputFolder + getFileName(timestamped, isVideo)

# ------------------------------------------------------------------------------

def showPreview(x = 0, y = 0, w = 800, h = 600):
	global previewVisible
	camera.start_preview(fullscreen=False, resolution=(w, h), window=(x, y, w, h))	
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
	if raw == True:
		conversionThread = threading.Thread(target=convertBayerDataToDNG, args=(filepath,))
		conversionThread.start()

# ------------------------------------------------------------------------------		

def convertBayerDataToDNG(filepath):
	dng.convert(filepath)

# === Image Capture ============================================================

try:
	echoOff()
	imageCount = 1
	isRecording = False

	try:
		os.chdir('/home/pi') 
	except:
		pass
	
	def Capture(mode = 'persistent'):
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
		global timer
		global raw
		global imageCount
		global isRecording

		# print(str(camera.resolution))
		camera.sensor_mode = 3

		print('\n Camera ' + version )
		print('\n ----------------------------------------------------------------------')
		time.sleep(2)

		
		setShutter(shutter, 0)		
		setISO(iso, 0)
		setExposure(exposure, 0)
		setEV(ev, 0)
		setBracket(bracket, 0)
		setAWB(awb, 0)
		
		showInstructions(False, 0)
		showPreview(0, 0, previewWidth, previewHeight)
		
		# print('Key Pressed: ' + keyboard.read_hotkey())
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
					
					if mode == 'persistent':
						# Normal photo
						filepath = getFilePath(True)
						print(' Capturing image: ' + filepath + '\n')
						captureImage(filepath, raw)
						
						imageCount += 1
				
						if (bracket != 0):
							baseEV = ev
							# Take underexposed photo
							setEV(baseEV + bracketLow, 0, False)
							filepath = getFilePath(True)
							print(' Capturing image: ' + filepath + '  [' + str(bracketLow) + ']\n')
							captureImage(filepath, raw)
							imageCount += 1

							# Take overexposed photo
							setEV(baseEV + bracketHigh, 0, False)
							filepath = getFilePath(True)
							print(' Capturing image: ' + filepath + '  [' + str(bracketHigh) + ']\n')
							captureImage(filepath, raw)
							imageCount += 1						
							
							# Reset EV to base photo's value
							setEV(baseEV, 0, False)
							
					elif mode == 'timelapse':
						# Timelapse photo series
						if timer < 0:
							timer = 1
						while True:
							filepath = getFilePath(False)
							print(' Capturing timelapse image: ' + filepath + '\n')
							captureImage(filepath, raw)
							imageCount += 1
							time.sleep(timer) 	

					elif mode == 'video':
						camera.sensor_mode = 0
						if isRecording == True:
							camera.stop_recording()			
							camera.video_stabilization = False							
							camera.resolution = camera.MAX_RESOLUTION
							isRecording = False
							time.sleep(1)
						else:
							filepath = getFilePath(True, True)
							print(' Capturing video: ' + filepath + '\n')
							isRecording = True							
							camera.resolution = (1920, 1080)
							camera.video_stabilization = True
							camera.start_recording(filepath)
							if timer > 0:
								sleep(timer)
								camera.stop_recording()
							
					else:
						# Single photo and then exit
						filepath = getFilePath(True)
						print(' Capturing single image: ' + filepath + '\n')
						captureImage(filepath, raw)
						echoOn()
						break

				# Preview Toggle				
				elif keyboard.is_pressed('p'):
					if previewVisible == True:
						hidePreview()
					else:
						showPreview(0, 0, previewWidth, previewHeight)

				# Shutter Speed	
				elif keyboard.is_pressed('s+up'):
					if shutter == 0:
						shutter = shutterShort
					if shutter > shutterShort and shutter <= shutterLong:					
						shutter = int(shutter / 1.5)
					setShutter(shutter, 0.25)
				elif keyboard.is_pressed('s+down'):
					if shutter == 0:						
						shutter = shutterLong
					elif shutter < shutterLong and shutter >= shutterShort:					
						shutter = int(shutter * 1.5)
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
				print(str(ex))
				pass

	def CaptureAndUploadImage():
		Capture()
		time.sleep(1000)
		# Not yet implemented

	# print(' Action: ' + action)
	if action == 'capture' or action == 'image' or action == 'photo':
		Capture()
	elif action == 'capturesingle' or action == 'single':
		Capture('single')
	elif action == 'timelapse':
		Capture('timelapse')
	elif action == 'video':
		Capture('video')
	else:
		echoOn()
		sys.exit(0)

except KeyboardInterrupt:
	echoOn()
	sys.exit(1)
