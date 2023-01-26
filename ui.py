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
		collapseButtonWidth = 42
		collapseButtonHeight = 128
		buttonCount = 11
		buttonWidth = (globals.appWidth - collapseButtonWidth - 5) / buttonCount
		buttonWidth = int(buttonWidth)
		buttonHeight = buttonWidth
		labelHeight = 30
		cellPadding = 10
		gutter = 1
		tempButtonCollection = []
		x = collapseButtonWidth
		y = globals.appHeight - buttonHeight - 100
			

		# --- Control Rendering -------------------------------------------------
		# Status
		try:
			statusText = globals.fontDefault.render(str(globals.statusDictionary['message']), True, (255, 255, 255))
			globals.displaySurface.blit(statusText, (collapseButtonWidth, 42))
		except:
			print('Warning: Could not update on-screen status')
			pass

		# Hide / Collapse Button
		expandIcon = pygame.image.load(os.path.join(globals.appRoot, 'images/menu-expand.png')).convert_alpha()	
		collapseIcon = pygame.image.load(os.path.join(globals.appRoot, 'images/menu-collapse.png')).convert_alpha()
		globals.menuToggleRectangle = pygame.Rect(5, y, collapseButtonWidth, collapseButtonHeight)
		if globals.menuCollapsed == True:
			menuToggleIcon = pygame.transform.scale(expandIcon, (collapseButtonWidth - (cellPadding * 2), collapseButtonHeight - (cellPadding * 2)))
			globals.displaySurface.blit(menuToggleIcon, (5, y))
		else: 
			menuToggleIcon = pygame.transform.scale(collapseIcon, (collapseButtonWidth - (cellPadding * 2), collapseButtonHeight - (cellPadding * 2)))
			globals.displaySurface.blit(menuToggleIcon, (5, y))
	

			if (len(globals.buttonData) == 0):
				parentList = Data.getControls().parents
			else:
				parentList = globals.buttonData

			
			if len(parentList) > 0:
				for parent in parentList:
					groupTextX = x
					groupTextY = y + buttonHeight
					
					itemCount = 0
					for item in parent.itemList:
						itemX = x
						itemY = y
						itemCount = itemCount + 1
					
						# Button
						controlRectangle = pygame.Rect(itemX, itemY, buttonWidth, buttonHeight)
						button = Button()
						button.rect = controlRectangle
						button.text = item.tooltip
						button.type = 'launcher'
						button.value = item.id
						button.icon = item.icon

						# Button Icon
						if globals.statusDictionary['action'] == 'recording' and button.value == 'captureVideo':
							controlIcon = pygame.image.load(os.path.join(globals.appRoot, button.icon.replace('.png', '-active.png'))).convert_alpha()
						else:
							controlIcon = pygame.image.load(os.path.join(globals.appRoot, button.icon)).convert_alpha()
						controlIcon = pygame.transform.scale(controlIcon, (buttonWidth - (cellPadding * 2), buttonHeight - (cellPadding * 2)))
						
						globals.displaySurface.blit(controlIcon, (itemX + cellPadding, itemY + cellPadding))

						
						tempButtonCollection.append(button)
					
						x = itemX + buttonWidth + gutter
						
					# Button Group Text
					groupTextRectangleWidth = (itemCount * (buttonWidth + gutter)) - gutter
					groupTextRectangle = pygame.Rect(groupTextX, groupTextY, groupTextRectangleWidth, labelHeight)

					groupText = globals.fontDefault.render(parent.title, True, (255, 255, 255))
					globals.displaySurface.blit(groupText, groupText.get_rect(center = groupTextRectangle.center))
					
						
				
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
					
					if globals.menuToggleRectangle.collidepoint(event.pos):
						if globals.menuCollapsed == True:
							globals.menuCollapsed = False
						else:
							globals.menuCollapsed = True
