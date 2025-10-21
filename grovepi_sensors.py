import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import time
import grovepi
from grove_rgb_lcd import *

# Grove Ultrasonic Ranger connectd to digital port 2
ultrasonic_ranger = 2
# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# clear lcd screen  before starting main loop
setText("")

while True:
  try:
    # TODO:read distance value from Ultrasonic Ranger and print distance on LCD
    distance = grovepi.ultrasonicRead(ultrasonic_ranger) 
    # sanitize distance if grovepi returns unexpected values
    if not isinstance(distance, (int, float)) or distance < 0:
      time.sleep(0.18)
      continue
    distance = int(round(distance))

    # TODO: read threshold from potentiometer
    pot_val = grovepi.analogRead(potentiometer) 
   
    MAX_US = 517
    if pot_val < 0:
      pot_val = 0
    if pot_val > 1023:
      pot_val = 1023
    threshold = int(round(pot_val * MAX_US / 1023.0))

    # TODO: format LCD text according to threshhold
    obj_pres = "OBJ PRES" if distance < threshold else ""
    top_line = f"{threshold:3d} {obj_pres}".strip()
    bottom_line = f"{distance:4d}cm"

    setText(f"{top_line}\n{bottom_line}")

    # small delay to avoid overwhelming sensor/LCD
    time.sleep(0.18)

  except IOError:
    print("Error")
