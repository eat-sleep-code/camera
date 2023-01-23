#!/usr/bin/python3
import os
import sys
import time
import globals


	
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

		

		# --- Control Rendering -------------------------------------------------
		# Status
		statusVariable = tk.StringVar() 
		statusLabel = ttk.Label(root, compound=tk.CENTER, textvariable=statusVariable)
		statusLabel['style'] = 'default.TLabel'
		statusLabel.configure(anchor='center')
		statusVariable.set(statusDictionary['message'])		
		statusLabel.place(x=0,y=buttonHeight+labelHeight,width=globals.appWidth,height=labelHeight)
				
				
		# Exit
		# image = pygame.image.load(os.path.join(currentDirectory, 'images/exit.png'))
		# exitImage = ImageTk.PhotoImage(image)
		# exitButton = ttk.Button(root, compound=tk.CENTER, image=exitImage, command=lambda: Buttons.handler(buttonDictionary, 'exit'))
		# exitButton['style'] = 'default.TButton'
		# exitButton.place(x=borderLeft,y=0,width=buttonWidth,height=buttonHeight)

		# exitLabel = ttk.Label(root, compound=tk.CENTER, text='Exit')
		# exitLabel['style'] = 'warning.TLabel'
		# exitLabel.configure(anchor='center')
		# exitLabel.place(x=borderLeft,y=buttonHeight,width=buttonWidth,height=labelHeight)


		# Capture Video
		captureVideoImage = pygame.image.load(os.path.join(currentDirectory, 'images/capture-video.png'))
		captureVideoButton = ttk.Button(root, compound=tk.CENTER, image=captureVideoImage, command=lambda: Buttons.handler(buttonDictionary, 'captureVideo'))
		captureVideoButton['style'] = 'primary.TButton'
		captureVideoButton.place(x=borderLeft,y=0,width=buttonWidth,height=buttonHeight)

		captureVideoLabel = ttk.Label(root, compound=tk.CENTER, text='Record')
		captureVideoLabel['style'] = 'primary.TLabel'
		captureVideoLabel.configure(anchor='center')
		captureVideoLabel.place(x=borderLeft,y=buttonHeight,width=buttonWidth,height=labelHeight)

		# Video Mode
		videoModeImage = pygame.image.load(os.path.join(currentDirectory, 'images/video-mode.png'))
		videoModeButton = ttk.Button(root, compound=tk.CENTER, image=videoModeImage, command=lambda: Buttons.handler(buttonDictionary, 'videoMode'))
		videoModeButton['style'] = 'default.TButton'
		videoModeButton.place(x=borderLeft+buttonWidth,y=0,width=buttonWidth,height=buttonHeight)

		videoModeLabel = ttk.Label(root, compound=tk.CENTER, text='Mode')
		videoModeLabel['style'] = 'default.TLabel'
		videoModeLabel.configure(anchor='center')
		videoModeLabel.place(x=borderLeft+buttonWidth,y=buttonHeight,width=buttonWidth,height=labelHeight)


		# Shutter Speed 
		shutterUpImage = pygame.image.load(os.path.join(currentDirectory, 'images/shutter-speed-up.png'))
		shutterUpButton = ttk.Button(root, compound=tk.CENTER, image=shutterUpImage, command=lambda: Buttons.handler(buttonDictionary, 'shutterUp'))
		shutterUpButton['style'] = 'default.TButton'
		shutterUpButton.place(x=borderLeft+(buttonWidth*2),y=0,width=buttonWidth,height=buttonHeight)

		shutterDownImage = pygame.image.load(os.path.join(currentDirectory, 'images/shutter-speed-down.png'))
		shutterDownButton = ttk.Button(root, compound=tk.CENTER, image=shutterDownImage, command=lambda: Buttons.handler(buttonDictionary, 'shutterDown'))
		shutterDownButton['style'] = 'default.TButton'
		shutterDownButton.place(x=borderLeft+(buttonWidth*3),y=0,width=buttonWidth,height=buttonHeight)

		shutterLabel = ttk.Label(root, compound=tk.CENTER, text='Shutter Speed')
		shutterLabel['style'] = 'default.TLabel'
		shutterLabel.configure(anchor='center')
		shutterLabel.place(x=borderLeft+(buttonWidth*2),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


		#ISO
		isoUpImage = pygame.image.load(os.path.join(currentDirectory, 'images/iso-up.png'))
		isoUpButton = ttk.Button(root, compound=tk.CENTER, image=isoUpImage, command=lambda: Buttons.handler(buttonDictionary, 'isoUp'))
		isoUpButton['style'] = 'default.TButton'
		isoUpButton.place(x=borderLeft+(buttonWidth*4),y=0,width=buttonWidth,height=buttonHeight)

		isoDownImage = pygame.image.load(os.path.join(currentDirectory, 'images/iso-down.png'))
		isoDownButton = ttk.Button(root, compound=tk.CENTER, image=isoDownImage, command=lambda: Buttons.handler(buttonDictionary, 'isoDown'))
		isoDownButton['style'] = 'default.TButton'
		isoDownButton.place(x=borderLeft+(buttonWidth*5),y=0,width=buttonWidth,height=buttonHeight)

		isoLabel = ttk.Label(root, compound=tk.CENTER, text='ISO')
		isoLabel['style'] = 'default.TLabel'
		isoLabel.configure(anchor='center')
		isoLabel.place(x=borderLeft+(buttonWidth*4),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


		# Exposure Compensation
		evUpImage = pygame.image.load(os.path.join(currentDirectory, 'images/exposure-compensation-up.png'))
		evUpButton = ttk.Button(root, compound=tk.CENTER, image=evUpImage, command=lambda: Buttons.handler(buttonDictionary, 'evUp'))
		evUpButton['style'] = 'default.TButton'
		evUpButton.place(x=borderLeft+(buttonWidth*6),y=0,width=buttonWidth,height=buttonHeight)

		evDownImage = pygame.image.load(os.path.join(currentDirectory, 'images/exposure-compensation-down.png'))
		evDownButton = ttk.Button(root, compound=tk.CENTER, image=evDownImage, command=lambda: Buttons.handler(buttonDictionary, 'evDown'))
		evDownButton['style'] = 'default.TButton'
		evDownButton.place(x=borderLeft+(buttonWidth*7),y=0,width=buttonWidth,height=buttonHeight)

		evLabel = ttk.Label(root, compound=tk.CENTER, text='Compensation')
		evLabel['style'] = 'default.TLabel'
		evLabel.configure(anchor='center')
		evLabel.place(x=borderLeft+(buttonWidth*6),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


		# Exposure Bracketing
		bracketUpImage = pygame.image.load(os.path.join(currentDirectory, 'images/exposure-bracketing-up.png'))
		bracketUpButton = ttk.Button(root, compound=tk.CENTER, image=bracketUpImage, command=lambda: Buttons.handler(buttonDictionary, 'bracketUp'))
		bracketUpButton['style'] = 'default.TButton'
		bracketUpButton.place(x=borderLeft+(buttonWidth*8),y=0,width=buttonWidth,height=buttonHeight)

		bracketDownImage = pygame.image.load(os.path.join(currentDirectory, 'images/exposure-bracketing-down.png'))
		bracketDownButton = ttk.Button(root, compound=tk.CENTER, image=bracketDownImage, command=lambda: Buttons.handler(buttonDictionary, 'bracketDown'))
		bracketDownButton['style'] = 'default.TButton'
		bracketDownButton.place(x=borderLeft+(buttonWidth*9),y=0,width=buttonWidth,height=buttonHeight)

		bracketLabel = ttk.Label(root, compound=tk.CENTER, text='Bracketing')
		bracketLabel['style'] = 'default.TLabel'
		bracketLabel.configure(anchor='center')
		bracketLabel.place(x=borderLeft+(buttonWidth*8),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


		# Capture
		captureImage = pygame.image.load(os.path.join(currentDirectory, 'images/capture-photo.png'))
		captureButton = ttk.Button(root, compound=tk.CENTER, image=captureImage, command=lambda: Buttons.handler(buttonDictionary, 'capture'))
		captureButton['style'] = 'primary.TButton'
		captureButton.place(x=borderLeft+(buttonWidth*10),y=0,width=buttonWidth,height=buttonHeight)

		captureLabel = ttk.Label(root, compound=tk.CENTER, text='Capture')
		captureLabel['style'] = 'primary.TLabel'
		captureLabel.configure(anchor='center')
		captureLabel.place(x=borderLeft+(buttonWidth*10),y=buttonHeight,width=buttonWidth,height=labelHeight)
		

		def updateStatus():
			statusVariable.set(statusDictionary['message'])
			if statusDictionary['action'] == 'recording' and captureVideoLabel['style'] == 'primary.TLabel':
				captureVideoLabel['style'] = 'warning.TLabel'
			elif statusDictionary['action'] == 'recording' and captureVideoLabel['style'] == 'warning.TLabel':
				captureVideoLabel['style'] = 'primary.TLabel'
			else:
				captureVideoLabel['style'] = 'primary.TLabel'
			if running == False:
				root.destroy()
				sys.exit(0)


		

