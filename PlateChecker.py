from openalpr import Alpr
import json
import subprocess
import sys
import requests
import RPi.GPIO as GPIO
from time import sleep

location = "us"
config_path = "/etc/openalpr/openalpr.conf"
runtime_path = "/home/pi/openalpr/runtime_data/"

in1 = 24
in2 = 23
en = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)



def scan():
    # change definitions to define parameters of openalpr
    
    subprocess.call("fswebcam -r 1920x1080 -S 20 --set brightness=50% --no-banner /home/pi/Desktop/BruinLabsParking/license_plate.jpg", shell=True)
    
    alpr = Alpr(location, config_path, runtime_path)
    if not alpr.is_loaded():
        print("Failed to load OpenALPR")
        sys.exit()
    
    plates = alpr.recognize_file("license_plate.jpg")
    
    # checks if there is car in frame else returns 
    if len(plates['results']) == 0:
        return 
    else:
        # return the top 3 candidates
        candidates = [plates['results'][0]['candidates'][i]['plate'] for i in range(0,3)]
        return candidates
    alpr.unload()

def gate():
    for i in range(3): 
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(.5)
        GPIO.output(in1, GPIO.LOW)
        sleep(.5)
    
last_seen = ""
check_url = "https://parking.wtf/api/check-reservation"
confirm_url = "https://parking.wtf/api/confirm-reservation"

while True:
    potential_plates = scan()
    
    if not potential_plates:
        print("no car found")
        continue
    else:
        # loops for each potential candidate
        for i in range(len(potential_plates)):
            
            if potential_plates[i] == last_seen:
                break
            else:
                print(potential_plates[i])
                plate = {"plateNumber": potential_plates[i]}
                check = requests.post(check_url, json = plate)
                # convert response to a python boolean
                confirmation = check.json()
                if confirmation["result"] == True:
                    # catch errors in confirmation post
                    try:
                        confirm = requests.post(confirm_url, json = plate)
                    except Exception as e:
                        print("error for license plate number: " + potential_plates[i])
                        print(e)
                        break
                    gate()
                    last_seen = potential_plates[i]
                    print(potential_plates[i] + " has entered")
                    break
                else: 
                    print(potential_plates[i] + " has been denied")
    
    x = str(input())
    if x == exit:
        sys.exit()
        GPIO.cleanup()
                