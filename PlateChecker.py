from openalpr import Alpr
import json
import subprocess
import sys
import requests

def scan():
    #subprocess.call("fswebcam -r 1920x1080 -S 20 --set brightness=50% --no-banner /home/pi/Desktop/BruinLabsParking/license_plate.jpg", shell=True)
    
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data/")
    if not alpr.is_loaded():
        print("Failed to load OpenALPR")
        sys.exit()
    
    plates = alpr.recognize_file("license_plate.jpg")
    
    if len(plates['results']) != 0:
        candidates = [plates['results'][0]['candidates'][i]['plate'] for i in range(0,3)]
        return candidates
    else:
        print("no car found")
    
    alpr.unload()

last_seen = ""
while True:
    potential_plates = scan()
    
    if potential_plates[0] == last_seen:
        continue
    else:
        json_plates = json.dumps(potential_plates)
        x = requests.post(url, json = json_plates
        
scan()
