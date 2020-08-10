# Camera

This program makes use of a Raspberry Pi HQ camera a little more powerful and user-friendly.   It unleashes easy exposure bracketing, timelapse functionality, etc.   It also adds additional error handling and presets some common settings.

---
## Installation

Installation of the program, any prerequisites, as well as DNG support can be completed with the following install script.

```
wget https://raw.githubusercontent.com/eat-sleep-code/camera/master/install-camera.sh -O ~/install-camera.sh
sudo chmod +x ~/install-camera.sh && ~/install-camera.sh
```

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
+ _--raw_ : Set whether DNG files are created in addition to JPEG files	    *(default: True)*
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
