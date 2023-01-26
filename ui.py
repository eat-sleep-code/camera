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


		if (len(globals.buttonData) == 0):
			parentList = Data.getControls().parents
		else:
			parentList = globals.buttonData

		tempButtonCollection = []
		if len(parentList) > 0:
			x = collapseButtonWidth
			y = globals.appHeight - buttonHeight - 100
			
			for parent in parentList:

				# Button Group Text
				groupTextStart = x + cellPadding
				groupText = globals.fontDefault.render(parent.title, True, (255, 255, 255))
				globals.displaySurface.blit(groupText, (groupTextStart, y + buttonHeight))
				
				for item in parent.itemList:
					itemX = x
					itemY = y
				
					# Button
					controlRectangle = pygame.draw.rect(globals.displaySurface, globals.chromaKey, [itemX, itemY, buttonWidth, buttonHeight])
					button = Button()
					button.rect = controlRectangle
					button.text = item.tooltip
					button.type = 'launcher'
					button.value = item.id
					button.icon = item.icon

					# Button Icon
					if globals.statusDictionary['action'] == 'recording':
						print('recording')
					
					controlIcon = pygame.image.load(os.path.join(globals.appRoot, button.icon)).convert_alpha()
					controlIcon = pygame.transform.scale(controlIcon, (buttonWidth - (cellPadding * 2), buttonHeight - (cellPadding * 2)))
					controlIcon.set_colorkey(globals.chromaKey)
					
					
					globals.displaySurface.blit(controlIcon, (itemX + cellPadding, itemY + cellPadding))

					
					tempButtonCollection.append(button)
				
					x = itemX + buttonWidth + gutter
					
				
					
			
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
