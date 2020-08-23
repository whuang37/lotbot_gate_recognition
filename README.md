# LotBot Automated Parking Manager

This code is the license plate recognition system included with the LotBot parking management system created for BruinLabs 2020. Users can drive up to the system and have their license plate recognized and accepted/denied accordinly.

## Installation

- Connect a usb webcam to a computer(tested using a Raspberry Pi 3 with Buster Raspbian)
- Clone the github repository in your local system `git clone https://github.com/whuang37/lotbot_gate_recognition.git`
- Move into the mlab-imaris-analysis repository with `cd lotbot_gate_recognition`
- Install all the libraries mentioned in [requirements.txt](https://github.com/whuang37/biondi_body_client/blob/master/requirements.txt) using `pip install -r requirements.txt`
  - install all of openalpr dependencies as well
- Enter the corresponding GPIO pins and HTTPS links in plate_checker.py
- Run the main python file `python plate_checker.py` 

## Usage

This system reads the license plate and sends the top three candidates in a JSON format to an HTTPS link. It then waits for a return stating whether the car has been accepted or denied before activating a motor/light/etc.

# Authors and Acknowledgement

Development on LotBot by whuang37, solomon-lo, ymhwang1123, and jackxuanliu.

# Marketing Pitch

[Click here to see our marketing pitch](BruinLabsPitch.pptx)