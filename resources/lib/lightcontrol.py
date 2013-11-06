import sys
from pyglow import PyGlow

pyglow = PyGlow()

arm1 = int(sys.argv[1])
arm2 = int(sys.argv[2])
arm3 = int(sys.argv[3])
brightness = int(sys.argv[4])

entire_led_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
sub_led_array = []

pyglow.set_leds(entire_led_array,0)

for x in range(0, arm1):
	sub_led_array.append(x+1)
for y in range(6, 6 + arm2):
	sub_led_array.append(y+1)
for z in range(12, 12 + arm3):
	sub_led_array.append(z+1)

#print str(sub_led_array)
pyglow.set_leds(sub_led_array,brightness)

pyglow.update_leds()
