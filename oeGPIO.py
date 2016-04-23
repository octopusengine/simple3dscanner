#!/usr/bin/python
# Filename : oeGPIO.py

#-----------------------------------
## simple 3d scanner 
##----------------------------------
import time
from time import sleep
import RPi.GPIO as GPIO # for step motor

EN2 = 22
DIR2 = 27
STEP2 = 17
dStep=0.00001

#---------------------------------

def oeSetupGPIO():
  global EN2,DIR2,STEP2
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  #GPIO.setup(END2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(EN2, GPIO.OUT)
  GPIO.setup(DIR2, GPIO.OUT)
  GPIO.setup(STEP2, GPIO.OUT)

#---------------------------------

def oeMotCCWs(steps,speed):
   global EN2,DIR2,STEP2, dStep
   #step motor - coun clock wise   
   nas=2 #1600/ot #8=400 #16=200 for 360
   GPIO.output(EN2, False)
   GPIO.output(DIR2, False)
   for tx in range(steps*nas): 
     time.sleep(dStep*speed)  
     GPIO.output(STEP2, True)
     time.sleep(dStep*speed) 
     GPIO.output(STEP2, False)
   GPIO.output(EN2, True)  #aret.

#---------------------------------

def oeMotOff():  
   GPIO.output(EN2, True) #motor switch off 

#---end---
