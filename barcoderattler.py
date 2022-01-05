#Version: 0.2
#Author: Chrissy
#Date: 04/01/2022

import evdev
from evdev import InputDevice, categorize, ecodes
import csv
from csv import DictReader
from pexpect import pxssh
import RPi.GPIO as GPIO
import time

MMSIP='192.168.1.100'
MMSPWD='1'
MMSCSV='/opt/barcoderattler/games.csv'
MMSMBC='/media/fat/Scripts/.barcoderattler/mbc'

dev = InputDevice('/dev/input/event0')

led = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}

def readBarcode():
   x = ''
   caps = False
   dev.grab()

   for event in dev.read_loop():
      if event.type == ecodes.EV_KEY:
         data = categorize(event)
         if data.scancode == 42:
            if data.keystate == 1:
               caps = True
            if data.keystate == 0:
               caps = False
         if data.keystate == 1:
            if caps:
               key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)
            else:
               key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)
            if (data.scancode != 42) and (data.scancode != 28) :
               x += key_lookup
            if(data.scancode == 28):
               dev.ungrab()
               return x

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
