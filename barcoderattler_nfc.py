#!/usr/bin/env python

import csv
from csv import DictReader
from pexpect import pxssh
import RPi.GPIO as GPIO
import time
from nfc.clf import RemoteTarget

import nfc

MMSIP='192.168.1.100'
MMSPWD='1'
MMSCSV='/opt/barcoderattler/games.csv'
MMSMBC='/media/fat/Scripts/.barcoderattler/mbc'

# Time in seconds to wait between NFC reads
POLLING_DELAY=1

# Change this to point to your NFC device
# Tested with a PN532 connected via 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
NFC_ID='tty:USB0:pn532'
# Further options are available: https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#open-a-local-device
#NFC_ID='tty:USB0:arygon'
#NFC_ID='tty:AMA0'
#NFC_ID='tty'
#NFC_ID='usb'

# Write a plain text record to your nfc tag with the value set to the barcode
# Tested using https://play.google.com/store/apps/details?id=com.wakdev.wdnfc&hl=en_GB&gl=US

led = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

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

if __name__ == '__main__':

   clf = nfc.ContactlessFrontend()
   connected = clf.open(NFC_ID)
   if connected != True:
      raise Exception("Unable to connect to NFC reader")

   try:
      lastData=''

      print("Listening for NFC tags")
      while True:
         #print('.', end = '', flush=True)
         time.sleep(POLLING_DELAY)

         target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
         if target is None:
            continue

         tag = clf.connect(rdwr={'on-connect': lambda tag: False})
         if tag is None:
            continue

         print("Found tag")
         if tag.ndef is not None:
            if (not hasattr(tag.ndef.records[0], 'text')):
               print('Could not find a text atribute on the first record')
               continue

            data = tag.ndef.records[0].text
            if lastData == data:
               print("That tag has already been seen recently")
               continue

            GPIO.output(led, GPIO.HIGH)
            lastData = data
            print("Barcode:", lastData)
            rr=findRow(data)
            if rr:
               print("DB match:", rr['CORE'], rr['FILE'])
               if mms(rr) == False:
                  lastData=''
            GPIO.output(led, GPIO.LOW)

   except KeyboardInterrupt:
      print('Interrupted!')
   finally:
      clf.close()

   clf.close()
