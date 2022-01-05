# Barcode Rattler
A Raspberry Pi Powered Barcode Reader to load a game on the Mister FPGA using MBC

This is a work in progress and a bit hackery 😅

There are limitations on the MBC side. Some of the computer cores don't work in loading games up. Such as the commodore computers as the cores have changed the menu layout is slightly different.

Currently i have only implemented getting games from out of zip files. You can do direct loading of a rom, just not implemented in my python script to do this.

The CSV file, spaces and other special characters need backslash \ or sometimes double backslash \\\ not got around to sorting this out.

---

Versions
========

0.2 04/01/2022 | Initial commit

---

Raspberry Pi OS
===============

I used the Raspberry Pi OS Lite Release date: October 30th 2021 

Installation of files
=====================

Files need to be installed in to a folder called /opt/barcoderattler

```sudo mkdir /opt/barcoderattler```

```sudo chown pi /opt/barcoderattler```

```cd /opt/barcoderattler```

You can either get the zip file

```wget https://github.com/chris-jh/BarcodeRattler/archive/refs/tags/barcoderattler_v0.2.zip```

```unzip -j ./barcoderattler_v0.2.zip```

or the tar.tgz file

```wget https://github.com/chris-jh/BarcodeRattler/archive/refs/tags/barcoderattler_v0.2.tar.gz```

```tar -zxf ./barcoderattler_v0.2.tar.gz --strip-components=1```

or if you have git installed, you can clone the latest

```git clone https://github.com/chris-jh/BarcodeRattler.git ./```

all the above methods assume you are inside the /opt/barcoderattler folder before running

Installing MBC on Mister
========================

Get the Mister IP Address

Enable SSH on the Mister

Copy the mmsmbc.sh file to Mister in the Fat folder

default password is 1

```scp /opt/barcoderattler/mmsmbc.sh root@IP:/media/fat```

ssh into Mister and run the mmsmbc.sh file to install mbc

```ssh root@IP```

```cd /media/fat```

```./mmsmbc.sh```

Running this file will download MBC from the Fork at https://github.com/mrchrisster/MiSTer_Batch_Control

It will be installed on your SD Card at ```/media/fat/Scripts/.barcoderattler```

The main MBC Project is located at

https://github.com/pocomane/MiSTer_Batch_Control


Configuring the PI Camera
=========================

Make sure to enable the Camera and SSH on the Pi

You may need to tweak the focus on the Camera, so it can read close up objects, like a barcode.

I had to adjust mine anticlockwise about 1 full turn


Intalling PYTHON LIBS
======================

make sure to 

```sudo apt-get update```

and then run the file barcodesetup.sh (do not sudo, it will ask for password) on the pi, this should install the python libraries that is required

KEYBOARD USB Permissions
========================

A udev rule is required so that the pi user can have access to the USB events for the keyboard

create a file called (you will have to sudo nano)

```/etc/udev/rules.d/99-hidraw-permissions.rules```

and this should be inside it

```KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"```

The barcode scanner will need to be in USB Keyboard mode, it also needs to be the first usb keyboard device to be plugged in, or the only usb keyboard device plugged.

The barcode device i bought was this one from amazon.

https://www.amazon.co.uk/gp/product/B00Y83TXOE

CSV File
========

The file is made up of the headers

```BARCODE,CORE,ZIP,FILE,TMP```

BARCODE=The Barcode
CORE=Is the Core name, like GENESIS
ZIP=This zip file, this version expects the games to be inside a zip file, if not then changes need to be made to the python script
FILE=The file including the path inside the zip file of the game
TMP=a temperory filename to extract the zipfile to, can be for example /tmp/game.md for the genesis 

any special characters in the file path including spaces needs the backslash \
some need double backslash such as the [ ] 


Running
=======

There are two python script files

1. barcoderattler.py

This one uses the Barcode Hand Scanner, make sure to scan factory reset code in the book and then scan the USB Keyboard.

2. barcoderattler_camera.py

This is for using the Pi Camera on a Pi 3


In each of the python scripts there is an area at the top to Specify your Mister IP Address and to change the password is different from the default 1.
You can also change the location of the CSV file to read and also if you put the mbc in a different directory also.

---

If you are going to use the Hand Scanner, this needs to be the first keyboard device. Remove any keyboards, and then plug in the barcode hand scanner.

You should do any interaction with the Pi via SSH

---

To run each version, only one should be run, from the command line type either

1. ```/opt/barcoderattler/startrattler```

   To start the Barcode Hand Scanner version

2. ```/opt/barcoderattler/startrattler_camera```

   To start the Barcode scanning via the Pi Camera

---

If you want to enable the barcode rattler on start up, run either of the following

1. ```/opt/barcoderattler/enable_barcode_scanner```

   To enable the Barcode Hand Scanner on boot up

2. ```/opt/barcoderattler/enable_camera_barcode_scanner```

   To enable the Barcode Scanning via the Pi Camer on boot up

---

To start and stop the service

1. ```sudo service start barcoderattler```

   To Start the Barcode Hand Scanner

2. ```sudo service stop barcoderattler```

   To Stop the Barcode Hand Scanner

3. ```sudo service start barcoderattler```

   To Start the Barcode Camera Scanner

4. ```sudo service stop barcoderattler```

   To Stop the Barcode Camera Scanner


---

To Stop the services for starting at boot up

Run

```sudo systemctl disable barcoderattler_camera.service```

```sudo systemctl disable barcoderattler.service```
