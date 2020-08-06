import json
import requests

add_reservation = "https://parking.wtf/api/add-reservation"
add = requests.post(add_reservation, json = {"phoneNumber": "9499107797", "plateNumber": "6RUX251"})