import sys
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')
import time
import grovepi
from grove_rgb_lcd import *

# Grove Ultrasonic Ranger connected to digital port 2
ultrasonic_ranger = 2
# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# clear lcd screen before starting main loop
setText("")

while True:
    try:
        # Read distance value from Ultrasonic Ranger
        distance = grovepi.ultrasonicRead(ultrasonic_ranger) 
        # sanitize distance if grovepi returns unexpected values
        if not isinstance(distance, (int, float)) or distance < 0:
            time.sleep(0.18)
            continue
        distance = int(round(distance))

        # Read threshold from potentiometer
        pot_val = grovepi.analogRead(potentiometer) 
    
        MAX_US = 517
        if pot_val < 0:
            pot_val = 0
        if pot_val > 1023:
            pot_val = 1023
        threshold = int(round(pot_val * MAX_US / 1023.0))

        # Format LCD text with fixed positions
        if distance < threshold:
            # Format: "XXX OBJ PRES" (threshold + space + OBJ PRES)
            top_line = "{:3d} OBJ PRES".format(threshold)
            
            # Set background color to RED when object is present
            setRGB(255, 0, 0)  # Red
        else:
            # Format: "XXX           " (threshold + 11 spaces to clear the line)
            top_line = "{:3d}           ".format(threshold)
        
            # Set background color to GREEN when no object
            setRGB(0, 255, 0)  # Green

        bottom_line = "{:4d}cm".format(distance)

        # Use setText_norefresh as required
        setText_norefresh("{}\n{}".format(top_line, bottom_line))

        # small delay to avoid overwhelming sensor/LCD
        time.sleep(0.18)

    except IOError:
        print("Error")