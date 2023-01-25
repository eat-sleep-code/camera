#!/usr/bin/python3
import os
import sys
import time

import pygame

import globals
from data import Data
from models import Button



class UI():

	# === Create UI =======================================================

	def render(self, running):

		collapseButtonWidth = 16
		buttonCount = 11
		buttonWidth = (globals.appWidth - collapseButtonWidth) / buttonCount
		buttonWidth = int(buttonWidth)
		buttonHeight = buttonWidth
		labelHeight = 32
		cellPadding = 10
		gutter = 0
		

		# --- Control Rendering -------------------------------------------------
		# Status
		try:
			statusText = globals.fontDefault.render(str(globals.statusDictionary['message']), True, (255, 255, 255))
			globals.displaySurface.blit(statusText, (collapseButtonWidth, globals.appHeight - 50))
		except:
			print('Warning: Could not update on-screen status')
			pass

		# Hide / Collapse Button
		# TODO: Write logic to show/collapse controls

		groupList = Data.getCameraControls().cameraControls
		tempButtonCollection = []
		if len(groupList) > 0:
			x = collapseButtonWidth
			y = globals.appHeight - buttonHeight - 100
			for group in groupList:
				itemX = x
				itemY = y
				
				for control in group:
					# Button
					controlRectangle = pygame.draw.rect(globals.displaySurface, (255, 0, 255), [itemX, itemY, buttonWidth, buttonHeight])
					button = Button()
					button.rect = controlRectangle
					button.text = control.tooltip
					button.type = 'launcher'
					button.value = control.id
					button.icon = control.icon

					# Button Icon

					if globals.statusDictionary['action'] == 'recording':
						print('recording')
					
					controlIcon = pygame.image.load(os.path.join(globals.appRoot, button.icon)).convert_alpha()
					controlIcon = pygame.transform.scale(controlIcon, (buttonWidth, buttonHeight))
					globals.displaySurface.blit(controlIcon, (itemX, itemY))

					# Button Text
					buttonTextStart = itemX + buttonWidth + cellPadding + gutter
					buttonText = globals.fontDefault.render(button.text, True, (255, 255, 255))
					globals.displaySurface.blit(buttonText, (buttonTextStart, itemY))

					tempButtonCollection.append(button)
					
					x = itemX + buttonWidth + gutter
					#print('X:', x, 'Y:', y)
				
			globals.buttonCollection.clear()
			globals.buttonCollection = tempButtonCollection
			return



# === Button Click Event Handler ============================================

	def buttonHandler(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
					for button in globals.buttonCollection:
						rect = button.rect
						if rect.collidepoint(event.pos):
							globals.buttonStateDictionary.update({button.value: True})
							time.sleep(0.2)
