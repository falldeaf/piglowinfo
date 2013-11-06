import xbmc
import xbmcaddon
import os
import sys
import subprocess
import datetime
import _strptime
import time

__settings__   = xbmcaddon.Addon(id="piglowinfo")
#__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' >

picontrolpath = os.path.dirname(os.path.abspath(__file__)) + "/resources/lib/lightcontrol.py "

arm1 = 0
arm2 = 0
arm3 = 0
oldarm1 = 0
oldarm2 = 0
oldarm3 = 0
brightness = 10
percent_divisor = 16.6666666667

xbmc.executebuiltin('Notification(PiGlow Info,information daemon is running,5000,notification.png)')

#percent to Six (p26)
def p26(percent):
    return int(round( int(percent) / percent_divisor ))

def volume():
    volumearr = xbmc.getInfoLabel("Player.Volume")
    volfloat = float(volumearr.split()[0])
    volpercentage = (volfloat+60)/60*100
    volint = p26(volpercentage)
    return volint

def format(x):
    return {
        1: "%S",
        2: "%M:%S",
        3: "%H:%M:%S"
    }[x]

def getSeconds(t):
    total = 0
    if t.second > 0:
        total += t.second
    if t.minute > 0:
        total += t.minute * 60
    if t.hour > 0:
        total += t.hour * 3600
    return int(total)

def playmarker():
    duration = xbmc.getInfoLabel("Player.Duration")
    remaining = xbmc.getInfoLabel("Player.Time")
    if duration != "" and duration != None:

        dformat = format( len(duration.split(':')) )
        rformat = format( len(remaining.split(':')) )

        try:
            dt = datetime.datetime.strptime(duration, dformat)
        except TypeError:
            dt = datetime.datetime(*(time.strptime(duration, dformat)[0:6]))
        try:
            rt = datetime.datetime.strptime(remaining, rformat)
        except TypeError:
            rt = datetime.datetime(*(time.strptime(remaining, rformat)[0:6]))

        print "playmarker: d-" + str(getSeconds(dt))
        print "playmarker: r-" + str(getSeconds(rt))
        #percentage = 100 * (x-a) / (b-a) (a=0 b=durationS x=timeS)
        return p26(100 * getSeconds(rt) / getSeconds(dt))
    return 0

def cache():
    cache = xbmc.getInfoLabel("Player.CacheLevel")
    if cache != "":
        print "cacheF:" + cache
        return p26(float(cache))
    return 0

def temp():
    temperature = float(xbmc.getInfoLabel("System.CPUTemperature")[:-3])
    #temp range (a)120f - (b)185f
    if temperature != "?":
        temppercent = 100 * (temperature-120) / (185-120)
        finalled = p26(temppercent)
        if finalled > 6:
            return 6
        return finalled
    return 0

def space():
    space_percent = xbmc.getInfoLabel("System.UsedSpacePercent")
    #if space_percent == "Unavailable":
        #return p26(space_percent)
    return 0

def mem():
    mem_percent = xbmc.getInfoLabel("System.Memory(used.percent)")
    return p26(mem_percent[:-1])

def battery():
    batt = xbmc.getInfoLabel("System.BatteryLevel")
    if batt != "Busy":
        return p26(batt[:-1])
    return 0

def report():
    print "--------start-----------"
    print "volume:" + str(volume())
    print "playMarker:" + str(playmarker())
    print "cache: " + str(cache())
    print "temp:" + str(temp())
    print "space:" + str(space())
    print "mem:" + str(mem())
    print "battery:" + str(battery())
    print int(float(__settings__.getSetting("brightness")))
    print "-------end--------------\n"

#print xbmc.getInfoLabel("Player.TimeRemaining")


brightness = int(float(__settings__.getSetting("brightness")))

#subprocess.call("sudo python /home/pi/.xbmc/addon/script.piglowinfo/piglowlights.py " + str(arm1) + " " + str(arm2) + " " + str(arm3) + " " + str(brightness) , shell=True)

while (not xbmc.abortRequested):
    #xbmc service loop
    #report()
    arm1 = globals()[ __settings__.getSetting("arm1") ]()
    arm2 = globals()[ __settings__.getSetting("arm2") ]()
    arm3 = globals()[ __settings__.getSetting("arm3") ]()
    #subprocess.call("python " + picontrolpath + str(arm1) + " " + str(arm2) + " " + str(arm3) + " " + str(brightness), shell=True)
    cmd = "sudo python " + picontrolpath + str(arm1) + " " + str(arm2) + " " + str(arm3) + " " + str(brightness)

    if oldarm1 != arm1 or oldarm2 != arm2 or oldarm3 != arm3:
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    oldarm1 = arm1
    oldarm2 = arm2
    oldarm3 = arm3

    time.sleep(1)
    # wait for the process to terminate
    #out, err = process.communicate()
    #errcode = process.returncode

    #print err
                                                          
