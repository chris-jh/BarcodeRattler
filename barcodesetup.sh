#!/bin/bash
sudo apt-get install python3-opencv libzbar0 python3-pip
python3 -m pip install evdev
python3 -m pip install pyzbar
python3 -m pip install pexpect
python3 -m pip install RPi.GPIO

echo "Run either"
echo ""
echo "/opt/barcoderattler/enable_barcode_scanner"
echo ""
echo "or"
echo ""
echo "/opt/barcoderattler/enable_camera_barcode_scanner"
echo ""
echo "Depending if you want to run the Barcode Hand Scanner, or Scanning Via the Pi Camera on boot up."
echo ""
echo "See Read Me for more details."
echo ""
