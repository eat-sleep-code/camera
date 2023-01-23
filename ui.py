#!/usr/bin/python3
import os
import sys
import time

import pygame

import globals
from data import Data
from models import Button


class Buttons():
	
	# === Button Click Event Handler ============================================

	def handler(buttonDictionary, e):
		
		# print(' DEBUG: ' + e + ' was clicked ')

		if e == 'shutterUp':
			buttonDictionary.update({'shutterUp': True})
		elif e == 'shutterDown':
			buttonDictionary.update({'shutterDown': True})
		elif e == 'isoUp':
			buttonDictionary.update({'isoUp': True})
		elif e == 'isoDown':
			buttonDictionary.update({'isoDown': True})
		elif e == 'evUp':
			buttonDictionary.update({'evUp': True})
		elif e == 'evDown':
			buttonDictionary.update({'evDown': True})
		elif e == 'bracketUp':
			buttonDictionary.update({'bracketUp': True})
		elif e == 'bracketDown':
			buttonDictionary.update({'bracketDown': True})
		elif e == 'videoMode':
			buttonDictionary.update({'videoMode': True})
		elif e == 'capture':
			buttonDictionary.update({'capture': True})
		elif e == 'captureVideo':
			buttonDictionary.update({'captureVideo': True})
		elif e == 'exit':
			buttonDictionary.update({'exit': True})			
		
		time.sleep(0.2)

		return buttonDictionary



class OnScreenUI():

	# === Create UI =======================================================

	def create(self, running, statusDictionary, buttonDictionary):
		
		currentDirectory = os.getcwd() + '/'
		
		
		collapseButtonWidth = 16
		buttonCount = 8
		buttonWidth = (globals.appWidth - collapseButtonWidth) / buttonCount
		buttonHeight = buttonWidth
		labelHeight = 32
		cellPadding = 10
		gutter = 0
		

		# --- Control Rendering -------------------------------------------------
		# Status
		statusText = globals.fontDefault.render(str(globals.status), True, (255, 255, 255))
		globals.displaySurface.blit(statusText, (0, 0))
		
		# Hide / Collapse Button
		# TODO: Write logic to show/collapse controls

		menuItems = Data.getControls.controls
		tempButtonCollection = []
		if len(menuItems) > 0:
			x = collapseButtonWidth,
			y = globals.appHeight - buttonHeight
			for item in menuItems:
				itemX = x
				itemY = y
				
				# Button
				controlRectangle = pygame.draw.rect(globals.displaySurface, (1, 30, 64), [itemX, itemY, buttonWidth, buttonHeight])
				button = Button()
				button.rect = controlRectangle
				button.text = item.title
				button.type = 'launcher'
				button.value = item.id
				button.icon = item.icon

				# Button Icon
				controlIcon = pygame.image.load(os.path.join(globals.appRoot, button.icon)).convert_alpha()
				controlIcon = pygame.transform.scale(controlIcon, (buttonWidth, buttonHeight))
				globals.displaySurface.blit(controlIcon, (itemX, itemY))

				# Button Text
				textStart = itemX + buttonWidth + cellPadding + gutter
				gameTitleText = globals.fontDefault.render(button.text, True, (255, 255, 255))
				globals.displaySurface.blit(gameTitleText, (textStart, itemX, itemY))

				tempButtonCollection.append(button)
				
				x = itemX + buttonWidth + gutter
				#print('X:', x, 'Y:', y)
				
			globals.buttonCollection.clear()
			globals.buttonCollection = tempButtonCollection
			pygame.display.flip()


		
		def updateStatus():
			statusText.set(statusDictionary['message'])
			if statusDictionary['action'] == 'recording':
				print('recording')
			else:
				...
			if running == False:
				sys.exit(0)


	def buttonHandler():
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					for button in globals.buttonCollection:
						rect = button.rect
						if rect.collidepoint(event.pos):
							globals.buttonDictionary[button.value] == True
								