#!/usr/bin/python3
import argparse
import datetime
import fractions
import os
import signal
import subprocess
import sys
import threading
import time

import cv2
import pygame
from libcamera import ColorSpace
from picamera2 import MappedArray, Picamera2
from picamera2.controls import Controls
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

import globals
from ui import UI

version = '2023.01.24'

camera = Picamera2()
controls = Controls(camera)
camera.CAPTURE_TIMEOUT = 1500
running = False

# === UI Setup ================================================================

# Run without Desktop
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

globals.initialize()
ui = UI()
buttonHandlerThread = threading.Thread(target=ui.buttonHandler)
buttonHandlerThread.start()



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
args = parser.parse_args()
		

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


videoWidth = 1920
videoHeight = 1080
videoFormat = 'h264'
videoFramerate = defaultFramerate
videoModeMax = 1
videoMode = 0


# === Echo Control =============================================================

def echoOff():
	subprocess.run(['stty', '-echo'], check=True)
def echoOn():
	subprocess.run(['stty', 'echo'], check=True)
def clear():
	subprocess.call('clear' if os.name == 'posix' else 'cls')
clear()



# === Create Configurations ====================================================

camera.preview_configuration.main.size = (globals.appWidth, globals.appHeight)
camera.preview_configuration.main.format = 'BGR888'
camera.configure('preview')

# ------------------------------------------------------------------------------


camera.still_configuration.enable_raw()
camera.still_configuration.main.size = camera.sensor_resolution
#camera.still_configuration.buffer_count = 2
camera.still_configuration.colour_space = ColorSpace.Sycc()

# ------------------------------------------------------------------------------

camera.video_configuration.main.size = (videoWidth, videoHeight)
camera.video_configuration.buffer_count = 8
camera.video_configuration.colour_space = ColorSpace.Rec709()


# === Functions ================================================================

def showInstructions(clearFirst = False, wait = 0):
	if clearFirst == True:
		clear()
	else:
		print(' ----------------------------------------------------------------------')

	print('\n Press s+\u21E7 or s+\u2303 to change shutter speed')
	print('\n Press i+\u21E7 or i+\u2303 to change ISO')
	print('\n Press e+\u21E7 or e+\u2303 to change exposure compensation')
	print('\n Press b+\u21E7 or b+\u2303 to change exposure bracketing')
	
	if action == 'timelapse':			 		
		print('\n Press the [space] bar to begin a timelapse ')
	else:
		print('\n Press the [space] bar to take photos ')

	print('\n Press \u241B to exit ')
	time.sleep(wait)
	return


# ------------------------------------------------------------------------------

def setShutter(input, wait = 0):
	global controls
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
		if controls.FrameRate == defaultFramerate and shutter > shutterLongThreshold:
			controls.FrameRate =fractions.Fraction(5, 1000)
		elif controls.FrameRate != defaultFramerate and shutter <= shutterLongThreshold:
			controls.FrameRate = defaultFramerate
	except Exception as ex:
		# print( ' WARNING: Could not set framerate! ')
		pass
	
	try:
		if shutter == 0:
			controls.ExposureTime = 0
			# print(str(controls.ExposureTime) + '|' + str(controls.FrameRate) + '|' + str(shutter))	
			print(' Shutter Speed: auto')
			globals.statusDictionary.update({'message': 'Shutter Speed: auto'})
		else:
			controls.ExposureTime = shutter * 1000
			# print(str(controls.ExposureTime) + '|' + str(controls.FrameRate) + '|' + str(shutter))		
			floatingShutter = float(shutter/1000)
			roundedShutter = '{:.3f}'.format(floatingShutter)
			if shutter > shutterLongThreshold:
				print(' Shutter Speed: ' + str(roundedShutter)  + 's [Long Exposure Mode]')
				globals.statusDictionary.update({'message': ' Shutter Speed: ' + str(roundedShutter)  + 's [Long Exposure Mode]'})
			else:
				print(' Shutter Speed: ' + str(roundedShutter) + 's')
				globals.statusDictionary.update({'message': ' Shutter Speed: ' + str(roundedShutter) + 's'})
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Shutter Speed!' + str(shutter))

# ------------------------------------------------------------------------------				

def setISO(input, wait = 0):
	global controls
	global iso
	global isoMin
	global isoMax

	if str(input).lower() == 'auto' or str(input) == '0':
		controls.AeEnable = 1
		iso = 0
	else: 
		controls.AeEnable = 0
		iso = int(input)
		if iso < isoMin:	
			iso = isoMin
		elif iso > isoMax:
			iso = isoMax	
	try:	
		#TODO: camera.iso = iso
		# print(str(camera.iso) + '|' + str(iso))
		if iso == 0:
			print(' ISO: auto')
			globals.statusDictionary.update({'message': ' ISO: auto'})
		else:	
			print(' ISO: ' + str(iso))
			globals.statusDictionary.update({'message': ' ISO: ' + str(iso)})
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid ISO Setting! ' + str(iso))

# ------------------------------------------------------------------------------

def setExposure(input, wait = 0):
	global exposure

	exposure = input
	try:	
		controls.AeExposureMode = exposure
		print(' Exposure Mode: ' + exposure)
		globals.statusDictionary.update({'message': ' Exposure Mode: ' + exposure})
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Exposure Mode! ')
				
# ------------------------------------------------------------------------------

def setEV(input, wait = 0, displayMessage = True):
	global controls
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
		controls.ExposureValue = ev
		# print(str(camera.exposure_compensation) + '|' + str(ev))
		if displayMessage == True:
			print(' Exposure Compensation: ' + evPrefix + str(ev))
			globals.statusDictionary.update({'message': ' Exposure Compensation: ' + evPrefix + str(ev)})
		time.sleep(wait)
		return
	except Exception as ex: 
		print(' WARNING: Invalid Exposure Compensation Setting! ')	
		
# ------------------------------------------------------------------------------				

def setBracket(input, wait = 0, displayMessage = True):
	global controls
	global bracket
	global bracketLow
	global bracketHigh
	global evMax
	global evMin

	bracket = int(input)
	try:
		bracketLow = controls.ExposureValue - bracket
		if bracketLow < evMin:
			bracketLow = evMin
		bracketHigh = controls.ExposureValue + bracket
		if bracketHigh > evMax:
			bracketHigh = evMax
		if displayMessage == True:
			print(' Exposure Bracketing: ' + str(bracket))
			globals.statusDictionary.update({'message': ' Exposure Bracketing: ' + str(bracket)})
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Exposure Bracketing Value! ')

# ------------------------------------------------------------------------------

def setAWB(input, wait = 0):
	global controls
	global awb

	awb = input
	try:	
		controls.AwbMode = awb
		print(' White Balance Mode: ' + awb)
		globals.statusDictionary.update({'message': ' White Balance Mode: ' + awb})
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Auto White Balance Mode! ')

# ------------------------------------------------------------------------------

def setVideoMode(input = 0, wait = 0):
	# --- Video Modes --------------
	# 0 = 1920 x 1080 (30fps) - H264
	# 1 = 1920 x 1080 (24fps) - H264

	global controls
	global videoWidth
	global videoHeight
	global videoFramerate
	global videoFormat
	
	try:
		if input == 1:
			videoWidth = 1920
			videoHeight = 1080
			videoFramerate = 24
			videoFormat = 'h264'
			print(' Video Mode: 1920x1080 24fps (H264)')
			globals.statusDictionary.update({'message': 'Video Mode: 1920x1080 24fps (H264)'})
		else:
			videoWidth = 1920
			videoHeight = 1080
			videoFramerate = 30
			videoFormat = 'h264'
			print(' Video Mode: 1920x1080 30fps (H264)')
			globals.statusDictionary.update({'message': 'Video Mode: 1920x1080 30fps (H264)'})
		time.sleep(wait)
		return
	except Exception as ex:
		print(' WARNING: Invalid Video Mode! ')


# ------------------------------------------------------------------------------

def getFileName(timestamped = True, isVideo = False):
	now = datetime.datetime.now()
	datestamp = now.strftime('%Y%m%d')
	timestamp = now.strftime('%H%M%S')		
			
	if isVideo == True:
		extension = '.h264'
		return datestamp + '-' + timestamp + extension
	else:
		extension = '.jpg'
		if timestamped == True:
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

def captureImage(filepath, raw = True):
	request = camera.switch_mode_and_capture_request('still')
	request.save('main', filepath)
	array = request.make_array('main')
	request.release()
	capturedFrame = pygame.image.frombuffer(array.data, camera.sensor_resolution, 'RGB')
	globals.displaySurface.blit(capturedFrame, (0, 0))
	pygame.display.update()
	if raw == True:
		filepathDNG = filepath.replace('.jpg', '.dng')
		capturedFrame.save_dng(filepathDNG)
	time.sleep(5)
	return

# ------------------------------------------------------------------------------
"""
def detectAreas(detectionType = 'face'):
	global previewVisible

	try:
		itemDetector = cv2.CascadeClassifier('/cv/' + detectionType + '.xml')
		captured = camera.capture_array('lores')
		gray = cv2.cvtColor(captured, cv2.COLOR_BGR2GRAY)
		detections = itemDetector.detectMultiScale(gray, 1.1, 3)
		return detections
	except Exception as ex:
		print( ' WARNING: Could not perform detection! ' + str(ex))
		pass

# ------------------------------------------------------------------------------

def drawDetectedAreas(request):
	(w0, h0) = camera.stream_configuration('main')['size']
	(w1, h1) = camera.stream_configuration('lores')['size']

	with MappedArray(request, 'main') as m:
		for detectedArea in detections:
			(x, y, w, h) = [c * n // d for c, n, d in zip(detectedArea, (w0, h0) * 2, (w1, h1) * 2)] 
			cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
"""
# ------------------------------------------------------------------------------

def createUI():
	global running
	running = True
	ui.render(running)
	
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
		global videoWidth
		global videoHeight
		global videoFramerate
		global videoFormat
		global videoMode
		global videoModeMax
		global imageCount
		global isRecording

		camera.start()
		# print(str(camera.resolution))
		#camera.sensor_mode = 3

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
		
		while True:
			try:
				key = pygame.key.get_pressed()
				if (key[pygame.K_q] or key[pygame.K_ESCAPE]) or (globals.buttonStateDictionary['exit'] == True):
					# clear()
					echoOn()
					sys.exit(1)
					
				# Help
				elif (key[pygame.K_QUESTION]):
					showInstructions(True, 0.5)	

				# Capture
				elif (key[pygame.K_SPACE]) or (globals.buttonStateDictionary['capture'] == True):
					
					if mode == 'persistent':
						# Normal photo
						filepath = getFilePath(True)
						print(' Starting capture...', globals.buttonStateDictionary['capture'])
	
						print(' Capturing image: ' + filepath + '\n')
						captureImage(filepath, raw)
						print('did I come back here?')
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
							
					else:
						# Single photo and then exit
						filepath = getFilePath(True)
						print(' Capturing single image: ' + filepath + '\n')
						captureImage(filepath, raw)
						echoOn()
						break

					print('Updating button')
					globals.buttonStateDictionary.update({'capture': False})
					print('Button is now ', globals.buttonStateDictionary['capture'])
				elif (globals.buttonStateDictionary['captureVideo'] == True):

					# Video
					if isRecording == False:
						isRecording = True
						globals.statusDictionary.update({'action': 'recording'})
						filepath = getFilePath(True, True)
						print(' Capturing video: ' + filepath + '\n')
						globals.statusDictionary.update({'message': ' Recording: Started '})
						globals.buttonStateDictionary.update({'captureVideo': False})
						encoder = H264Encoder(10000000)
						encoder.output = FileOutput(filepath)
						#controls.FrameRate = videoFramerate
						camera.configure('video')
						camera.start_encoder(encoder)
					else:
						isRecording = False
						globals.statusDictionary.update({'action': ''})
						camera.stop_encoder()
						camera.configure('preview')
						print(' Capture complete \n')
						globals.statusDictionary.update({'message': ' Recording: Stopped '})
						globals.buttonStateDictionary.update({'captureVideo': False})
					
					time.sleep(1)

				# Shutter Speed	
				elif (key[pygame.K_s] and (pygame.key.get_mods() & pygame.KMOD_SHIFT)) or (globals.buttonStateDictionary['shutterSpeedUp'] == True):
					if shutter == 0:
						shutter = shutterShort
					elif shutter > shutterShort and shutter <= shutterLong:					
						shutter = int(shutter / 1.5)
					setShutter(shutter, 0.25)
					globals.buttonStateDictionary.update({'shutterSpeedUp': False})
				elif (key[pygame.K_s] and (pygame.key.get_mods() & pygame.KMOD_CTRL)) or (globals.buttonStateDictionary['shutterSpeedDown'] == True):
					if shutter == 0:						
						shutter = shutterLong
					elif shutter < shutterLong and shutter >= shutterShort:					
						shutter = int(shutter * 1.5)
					elif shutter == shutterShort:
						shutter = 0
					setShutter(shutter, 0.25)
					globals.buttonStateDictionary.update({'shutterSpeedDown': False})

				# ISO
				elif (key[pygame.K_i] and (pygame.key.get_mods() & pygame.KMOD_SHIFT)) or (globals.buttonStateDictionary['isoUp'] == True):
					if iso == 0:
						iso = isoMin
					elif iso >= isoMin and iso < isoMax:					
						iso = int(iso * 2)
					setISO(iso, 0.25)
					globals.buttonStateDictionary.update({'isoUp': False})
				elif (key[pygame.K_i] and (pygame.key.get_mods() & pygame.KMOD_CTRL)) or (globals.buttonStateDictionary['isoDown'] == True):
					if iso == 0:
						iso = isoMax
					elif iso <= isoMax and iso > isoMin:					
						iso = int(iso / 2)
					elif iso == isoMin:
						iso = 0
					setISO(iso, 0.25)
					globals.buttonStateDictionary.update({'isoDown': False})

				# Exposure Compensation
				elif (key[pygame.K_e] and (pygame.key.get_mods() & pygame.KMOD_SHIFT)) or (globals.buttonStateDictionary['evUp'] == True):
					if ev >= evMin and ev < evMax:					
						ev = int(ev + 1)
						setEV(ev, 0.25)
						globals.buttonStateDictionary.update({'evUp': False})
				elif (key[pygame.K_e] and (pygame.key.get_mods() & pygame.KMOD_CTRL)) or (globals.buttonStateDictionary['evDown'] == True):
					if ev <= evMax and ev > evMin:					
						ev = int(ev - 1)
						setEV(ev, 0.25)
						globals.buttonStateDictionary.update({'evDown': False})

				# Exposure Bracketing
				elif (key[pygame.K_b] and (pygame.key.get_mods() & pygame.KMOD_SHIFT)) or (globals.buttonStateDictionary['bracketUp'] == True):
					if bracket < evMax:
						bracket = int(bracket + 1)
						setBracket(bracket, 0.25)
						globals.buttonStateDictionary.update({'bracketUp': False})
				elif (key[pygame.K_b] and (pygame.key.get_mods() & pygame.KMOD_CTRL)) or (globals.buttonStateDictionary['bracketDown'] == True):
					if bracket > 0:					
						bracket = int(bracket - 1)
						setBracket(bracket, 0.25)
						globals.buttonStateDictionary.update({'bracketDown': False})

				# Video Mode
				elif (globals.buttonStateDictionary['videoMode'] == True):
					if videoMode < videoModeMax:
						videoMode = int(videoMode + 1)
					else: 
						videoMode = 0
					setVideoMode(videoMode, 0.25)
					globals.buttonStateDictionary.update({'videoMode': False})
			
				# Show Preview Frame
				array = camera.capture_array()
				previewFrame = pygame.image.frombuffer(array.data, (globals.appWidth, globals.appHeight), 'RGB')
				globals.displaySurface.blit(previewFrame, (0, 0))
				createUI()
				pygame.display.update()
				#uiThread = threading.Thread(target=createUI)
				#uiThread.start()

			except SystemExit:
				time.sleep(5)				
				os.kill(os.getpid(), signal.SIGSTOP)
				sys.exit(0)
			except Exception as ex:
				print(str(ex))
				pass



	# print(' Action: ' + action)
	if action == 'capturesingle' or action == 'single':
		Capture('single')
	elif action == 'timelapse':
		Capture('timelapse')
	elif action == 'video':
		Capture('video')
	else:
		Capture()

except KeyboardInterrupt:
	camera.stop()
	echoOn()
	sys.exit(1)
