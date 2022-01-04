import cv2
import pyzbar.pyzbar as pyzbar
from datetime import datetime

import csv
from csv import DictReader
from pexpect import pxssh
import RPi.GPIO as GPIO
import time

MMSIP='192.168.1.100'
MMSPWD='1'
MMSCSV='/opt/barcoderattler/games.csv'
MMSMBC='/media/fat/Scripts/.barcoderattler/mbc'

camera = cv2.VideoCapture(0)

led = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

def readBarcode():
   ret, image = camera.read()
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   barcodes = pyzbar.decode(gray)
   for barcode in barcodes:
      barcodeData = barcode.data.decode()
      barcodeType = barcode.type
      return barcodeData

def mms(rr):
   try:
      s = pxssh.pxssh()
      s.login(MMSIP, 'root', MMSPWD)
      s.sendline('unzip -p '+rr['ZIP']+' '+rr['FILE']+' > '+rr['TMP'])
      s.prompt()
      print(s.before)
      s.sendline(MMSMBC+' load_rom '+rr['CORE']+' '+rr['TMP'])
      s.prompt()
      print(s.before)
      return True
   except pxssh.ExceptionPxssh as e:
      print("pxssh failed on login.")
      print(e)
      return False

def findRow(code):
   with open(MMSCSV, 'r') as read_obj:
      csv_dict_reader = DictReader(read_obj)
      for row in csv_dict_reader:
         if row['BARCODE'] == code:
            return row

try:
   lastData=''
   while True:
      data = readBarcode()
      if data:
         if lastData != data:
            GPIO.output(led, GPIO.HIGH)
            lastData = data
            print(lastData)
            rr=findRow(data)
            if rr:
               print(rr['CORE'], rr['FILE'])
               if mms(rr) == False:
                  lastData=''
            GPIO.output(led, GPIO.LOW)
except KeyboardInterrupt:
   print('interrupted!')
