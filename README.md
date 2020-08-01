# Camera

This program makes use of a Raspberry Pi camera a little more friendly by adding some error handling and presetting common settings.

---
## Installation

### Prerequisites

To install the required prerequisites, execute the following from the Terminal window:
```
sudo apt-get update
sudo apt-get install python3 python3-pip python3-picamera
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
... and then add the following code to the .bash_aliases file:   
```
function camera {
	python3 ./camera/camera.py $@
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
+ _--ev_' : Set the exposure compensation (+/-10)     *(default: 0)*
+ _--awb_' : Set the Auto White Balance (AWB) mode      *(default: auto)*
+ _--exposure_ : Set the exposure mode     *(default: auto)*
+ _--outputFolder_ : Set the folder where images will be saved     *(default: dcim/)* 
