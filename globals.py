#!/usr/bin/python3
import os
import sys

import pygame


def initialize():
	pygame.init()
	pygame.mixer.init()

	global clock
	clock = pygame.time.Clock()

	global appRoot
	#appRoot = os.getcwd() + '/'
	appRoot = '/home/pi/camera/'
	os.chdir(appRoot)

	global displayInfo
	displayInfo = pygame.display.Info()
	
	global appWidth 
	appWidth = displayInfo.current_w
	
	global appHeight
	appHeight = displayInfo.current_h
	
	global displaySurface
	displaySurface = pygame.display.set_mode((appWidth, appHeight), pygame.HWSURFACE | pygame.DOUBLEBUF)   # pygame.FULLSCREEN | 

	global fontDefault
	fontDefault = pygame.font.SysFont('Helvetica', 20, bold=False)

	global title
	title = 'Camera'
	pygame.display.set_caption(title)

	global iconDefault 
	iconDefault = pygame.image.load(os.path.join(appRoot, 'images/capture-photo.png')).convert_alpha()
	pygame.display.set_icon(iconDefault)

	global buttonCollection
	buttonCollection = []
	
	global buttonStateDictionary
	buttonStateDictionary = {'exit': False, 'shutterUp': False, 'shutterDown': False, 'isoUp': False, 'isoDown': False, 'evUp': False, 'evDown': False, 'bracketUp': False, 'bracketDown': False, 'videoMode': False, 'capture': False, 'captureVideo': False}

	global statusDictionary
	statusDictionary = {'message': '', 'action': ''}

	global detections
	detections = []



def restart():
	os.execv(sys.executable, ['python'] + sys.argv)