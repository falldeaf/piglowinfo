#Piglow Info addon for XBMC

##Installation

First, you need to install the GPIO python lib for Rasperry Pi (https://code.google.com/p/raspberry-gpio-python/)

1. wget http://raspberry-gpio-python.googlecode.com/files/python-rpi.gpio_0.3.1a-1_armhf.deb
2. sudo dpkg -i python-rpi.gpio_0.3.1a-1_armhf.deb

Next, download the xbmc Addon and install

1. Download the zip from falldeaf.com (http://falldeaf.com/wp-content/uploads/2013/11/service.piglowinfo-0.0.1.zip)
2. Settings
3. Add-ons
4. Install from zip file
4. Enter the path to the downloaded file and select OK
5. Open the add-on settings dialog and choose which conditions to monitor (or leave the default of volume, playmarker and mem)

You're done! You should be seeing the Piglow lights change depending on your conditions.

##Features

You can currently track:
- Volume (current system volume)
- Playmarker (How much time is left in the show or song)
- Cache (How much local cache is used)
- Temp (How hot is your Pi)
- Space (How much HD space is left)
- MEM (How much memory is being used)
- battery (How much battery is left)

##Known Issues

The Battery and Space conditions are untested.
