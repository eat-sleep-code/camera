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
	appRoot = os.getcwd() + '/'
	os.chdir(appRoot)

	global displayInfo
	displayInfo = pygame.display.Info()
	
	global appWidth 
	appWidth = displayInfo.current_w
	
	global appHeight
	appHeight = displayInfo.current_h
	
	global displaySurface
	displaySurface = pygame.display.set_mode((appWidth, appHeight), pygame.HWSURFACE | pygame.DOUBLEBUF)

	global fontDefault
	fontDefault = pygame.font.SysFont('Helvetica', 20, bold=False)

	global title
	title = 'Camera'
	pygame.display.set_caption(title)

	global iconDefault 
	iconDefault = os.path.join(appRoot, 'images/capture-photo.png')
	pygame.display.set_icon(iconDefault)

	global status
	status = ''

	global buttonCollection
	buttonCollection = []

	

def restart():
	os.execv(sys.executable, ['python'] + sys.argv)