def createControls(borderLeft, buttonHeight, buttonWidth, labelHeight):

    # Exit
    image = Image.open(os.path.join(currentDirectory, 'images/exit.png'))
    exitImage = ImageTk.PhotoImage(image)
    exitButton = ttk.Button(controls, compound=tk.CENTER, image=exitImage, command=lambda: handleOnScreenButtonClick('exitButton'))
    exitButton['style'] = 'default.TButton'
    exitButton.place(x=borderLeft,y=0,width=buttonWidth,height=buttonHeight)

    exitLabel = ttk.Label(controls, compound=tk.CENTER, text='Exit')
    exitLabel['style'] = 'warning.TLabel'
    exitLabel.configure(anchor='center')
    exitLabel.place(x=borderLeft,y=buttonHeight,width=buttonWidth,height=labelHeight)

    # Shutter Speed 
    image = Image.open(os.path.join(currentDirectory, 'images/shutter-speed-up.png'))
    shutterSpeedUpImage = ImageTk.PhotoImage(image)
    shutterSpeedUpButton = ttk.Button(controls, compound=tk.CENTER, image=shutterSpeedUpImage, command=lambda: handleOnScreenButtonClick('shutterSpeedUpButton'))
    shutterSpeedUpButton['style'] = 'default.TButton'
    shutterSpeedUpButton.place(x=borderLeft+(buttonWidth),y=0,width=buttonWidth,height=buttonHeight)

    image = Image.open(os.path.join(currentDirectory, 'images/shutter-speed-down.png'))
    shutterSpeedDownImage = ImageTk.PhotoImage(image)
    shutterSpeedDownButton = ttk.Button(controls, compound=tk.CENTER, image=shutterSpeedDownImage, command=lambda: handleOnScreenButtonClick('shutterSpeedDownButton'))
    shutterSpeedDownButton['style'] = 'default.TButton'
    shutterSpeedDownButton.place(x=borderLeft+(buttonWidth*2),y=0,width=buttonWidth,height=buttonHeight)

    shutterSpeedLabel = ttk.Label(controls, compound=tk.CENTER, text='Shutter Speed')
    shutterSpeedLabel['style'] = 'default.TLabel'
    shutterSpeedLabel.configure(anchor='center')
    shutterSpeedLabel.place(x=borderLeft+(buttonWidth),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


    #ISO
    image = Image.open(os.path.join(currentDirectory, 'images/iso-up.png'))
    isoUpImage = ImageTk.PhotoImage(image)
    isoUpButton = ttk.Button(controls, compound=tk.CENTER, image=isoUpImage, command=lambda: handleOnScreenButtonClick('isoUpButton'))
    isoUpButton['style'] = 'default.TButton'
    isoUpButton.place(x=borderLeft+(buttonWidth*3),y=0,width=buttonWidth,height=buttonHeight)

    image = Image.open(os.path.join(currentDirectory, 'images/iso-down.png'))
    isoDownImage = ImageTk.PhotoImage(image)
    isoDownButton = ttk.Button(controls, compound=tk.CENTER, image=isoDownImage, command=lambda: handleOnScreenButtonClick('isoDownButton'))
    isoDownButton['style'] = 'default.TButton'
    isoDownButton.place(x=borderLeft+(buttonWidth*4),y=0,width=buttonWidth,height=buttonHeight)

    isoLabel = ttk.Label(controls, compound=tk.CENTER, text='ISO')
    isoLabel['style'] = 'default.TLabel'
    isoLabel.configure(anchor='center')
    isoLabel.place(x=borderLeft+(buttonWidth*3),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


    # Exposure Compensation
    image = Image.open(os.path.join(currentDirectory, 'images/exposure-compensation-up.png'))
    exposureCompensationUpImage = ImageTk.PhotoImage(image)
    exposureCompensationUpButton = ttk.Button(controls, compound=tk.CENTER, image=exposureCompensationUpImage, command=lambda: handleOnScreenButtonClick('exposureCompensationUpButton'))
    exposureCompensationUpButton['style'] = 'default.TButton'
    exposureCompensationUpButton.place(x=borderLeft+(buttonWidth*5),y=0,width=buttonWidth,height=buttonHeight)

    image = Image.open(os.path.join(currentDirectory, 'images/exposure-compensation-down.png'))
    exposureCompensationDownImage = ImageTk.PhotoImage(image)
    exposureCompensationDownButton = ttk.Button(controls, compound=tk.CENTER, image=exposureCompensationDownImage, command=lambda: handleOnScreenButtonClick('exposureCompensationDownButton'))
    exposureCompensationDownButton['style'] = 'default.TButton'
    exposureCompensationDownButton.place(x=borderLeft+(buttonWidth*6),y=0,width=buttonWidth,height=buttonHeight)

    exposureCompensationLabel = ttk.Label(controls, compound=tk.CENTER, text='Compensation')
    exposureCompensationLabel['style'] = 'default.TLabel'
    exposureCompensationLabel.configure(anchor='center')
    exposureCompensationLabel.place(x=borderLeft+(buttonWidth*5),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


    # Exposure Bracketing
    image = Image.open(os.path.join(currentDirectory, 'images/exposure-bracketing-up.png'))
    exposureBracketingUpImage = ImageTk.PhotoImage(image)
    exposureBracketingUpButton = ttk.Button(controls, compound=tk.CENTER, image=exposureBracketingUpImage, command=lambda: handleOnScreenButtonClick('exposureBracketingUpButton'))
    exposureBracketingUpButton['style'] = 'default.TButton'
    exposureBracketingUpButton.place(x=borderLeft+(buttonWidth*7),y=0,width=buttonWidth,height=buttonHeight)

    image = Image.open(os.path.join(currentDirectory, 'images/exposure-bracketing-down.png'))
    exposureBracketingDownImage = ImageTk.PhotoImage(image)
    exposureBracketingDownButton = ttk.Button(controls, compound=tk.CENTER, image=exposureBracketingDownImage, command=lambda: handleOnScreenButtonClick('exposureBracketingDownButton'))
    exposureBracketingDownButton['style'] = 'default.TButton'
    exposureBracketingDownButton.place(x=borderLeft+(buttonWidth*8),y=0,width=buttonWidth,height=buttonHeight)

    exposureBracketingLabel = ttk.Label(controls, compound=tk.CENTER, text='Bracketing')
    exposureBracketingLabel['style'] = 'default.TLabel'
    exposureBracketingLabel.configure(anchor='center')
    exposureBracketingLabel.place(x=borderLeft+(buttonWidth*7),y=buttonHeight,width=buttonWidth*2,height=labelHeight)


    # Capture
    image = Image.open(os.path.join(currentDirectory, 'images/capture.png'))
    captureImage = ImageTk.PhotoImage(image)
    captureButton = ttk.Button(controls, compound=tk.CENTER, image=captureImage, command=lambda: handleOnScreenButtonClick('captureButton'))
    captureButton['style'] = 'default.TButton'
    captureButton.place(x=borderLeft+(buttonWidth*9),y=0,width=buttonWidth,height=buttonHeight)

    captureLabel = ttk.Label(controls, compound=tk.CENTER, text='Capture')
    captureLabel['style'] = 'primary.TLabel'
    captureLabel.configure(anchor='center')
    captureLabel.place(x=borderLeft+(buttonWidth*9),y=buttonHeight,width=buttonWidth,height=labelHeight)
