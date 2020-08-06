from openalpr import Alpr
import json
import subprocess
import sys
import requests

def scan():
    # change definitions to define parameters of openalpr
    location = "us"
    config_path = "/etc/openalpr/openalpr.conf"
    runtime_path = "/home/pi/openalpr/runtime_data/"
    
    #subprocess.call("fswebcam -r 1920x1080 -S 20 --set brightness=50% --no-banner /home/pi/Desktop/BruinLabsParking/license_plate.jpg", shell=True)
    
    alpr = Alpr(location, config_path, runtime_path)
    if not alpr.is_loaded():
        print("Failed to load OpenALPR")
        sys.exit()
    
    plates = alpr.recognize_file("license_plate.jpg")
    
    # checks if there is car in frame else returns 
    if len(plates['results']) == 0:
        print("no car found")
        return 
    else:
        # return the top 3 candidates
        candidates = [plates['results'][0]['candidates'][i]['plate'] for i in range(0,3)]
        return candidates
    alpr.unload()

def gate(): 
    print("works")
    
last_seen = ""
check_url = "https://parking.wtf/api/check-reservation"
confirm_url = "https://parking.wtf/api/confirm-reservation"

while True:
    potential_plates = scan()
    
    if not potential_plates:
        continue
    else:
        # loops for each potential candidate
        for i in range(len(potential_plates)):
            
            if potential_plates[i] == last_seen:
                continue
            else:
                json_plate = json.dumps({"plateNumber": potential_plates[i]})
                check = requests.post(check_url, data = json_plate)
                # convert response to a python boolean
                x = check.json()
                confirmation = json.load(x)
                
                if confirmation["result"] == True:
                    try:
                        confirm = requests.post(confirm_url, data = json_plate)
                    except:
                        print("error for license plate number: " + potential_plates[i])
                        break
                    gate()
                    last_seen = potential_plates[i]
                    break