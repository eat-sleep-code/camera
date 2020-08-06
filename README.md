# Camera

This program makes use of a Raspberry Pi camera a little more powerful and user-friendly.   It unleashes easy exposure bracketing, timelapse functionality, etc.   It also adds additional error handling and presets some common settings.

---
## Installation

### Prerequisites

To install the required prerequisites, execute the following from the Terminal window:
```
sudo apt-get update
sudo apt-get install python3 python3-pip python3-picamera
sudo pip3 install keyboard
```

### Download the code

To download the code and set the required permissions, execute the following from the Terminal window:
```
cd ~
sudo git clone https://github.com/eat-sleep-code/camera
sudo chown -R $USER:$USER camera
cd camera
sudo chmod +x camera.py
```
### Add an alias

To make launching the program more efficient you will want to create an alias to the program.   To do this, execute the following from the Terminal window:
```
cd ~
sudo nano .bash_aliases
```
... and then add the following code to the .bash_aliases file.   NOTE: The usage of `sudo` in the alias is a prerequisite of the Python keyboard library.      
```
function camera {
	sudo python3 ~/camera/camera.py $@
}
```
Save the file, exit nano.
Restart your computer to allow the alias to take effect.

---

## Usage
```
camera <options>
```

### Options

+ _--action_ : Set the camera action     *(default: capture)*
+ _--shutter_ : Set the shutter speed     *(default: auto)*
+ _--iso_ : Set the ISO     *(default: auto)*
+ _--exposure_ : Set the exposure mode     *(default: auto)*
+ _--ev_ : Set the exposure compensation (+/-10)     *(default: 0)*
+ _--bracket_ : Set the exposure bracketing value     *(default: 0)*
+ _--awb_ : Set the Auto White Balance (AWB) mode      *(default: auto)*
+ _--outputFolder_ : Set the folder where images will be saved     *(default: dcim/)* 
+ _--timer_ : Set the interval for timelapse mode     *(default: 0)* 
+ _--previewWidth_ : Set the preview window width     *(default: 800)*
+ _--previewHeight_ : Set the preview window height    *(default: 600)*

### Keyboard Controls
+ Press s+&#x25B2; or s+&#x25BC; to change shutter speed
+ Press i+&#x25B2; or i+&#x25B2; to change ISO
+ Press c+&#x25B2; or c+&#x25B2; to change exposure compensation
+ Press b+&#x25B2; or b+&#x25B2; to change exposure bracketing
+ Press [p] to toggle the preview window
+ Press the [space] bar to take photos or begin a timelapse
+ Press &#x241B; to exit
