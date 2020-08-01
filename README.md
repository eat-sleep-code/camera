# Camera

This program makes use of the Raspberry Pi cameras a little more friendly by adding some error handling and presetting some common settings.

---

## Git and run

```
cd ~
sudo git clone https://github.com/eat-sleep-code/camera
sudo chown -R $USER:$USER camera
cd camera
sudo chmod +x camera.py
```
### Add an alias

```
cd ~
sudo nano .bash_aliases
```

Add the following code to the .bash_aliases.   
```
function camera {
	python ./camera/camera.py $@
}
```
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
