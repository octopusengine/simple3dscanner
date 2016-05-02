#!/usr/bin/python
# Filename : scan.py
#-----------------------------------
## simple 3d scanner - octopusengine.eu
## 2016/04 - I am beginner, but it works ;-)
## 0.21 create xyz point cloud - directly posible import to MeshLab
## 0.33 oeGPIO, scannHelp, filter1
## 0.34 prepare for piCamera/webCamera/mobilCamera
## 0.35 scanSetup, scanInit, filter2
##----------------------------------
import os, sys, math, pygame, time
from datetime import datetime
from time import sleep
#import RPi.GPIO as GPIO # for step motor
from oeGPIO import * #oeSetupGPIO
from scannHelp import *
from scannSetup import *
from scannInit import *
#----------------------------------
pygame.init()

if piCamera:
  import picamera
  cam= picamera.PiCamera() 

if webCamera:
  import pygame.camera
  pygame.camera.init()

  width = 800 #1024 #800
  height = 600 #768 #600
  cam = pygame.camera.Camera("/dev/video0",(width,height),"RGB")


#-----------------------------main---setup
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
try:  
  name=str(sys.argv[1])
  #name="robot" 	#scanning object name
except: 
   help()
   name="noname"
   print ("Default project name: "+ name )
datName=name+datetime.now().strftime("%Y_%m_%d_%H_%M")    

if name=="help":
    help()
    sys.exit()
    #err.stop
else:
     print ("First argument > project name: "+ name )

try:
  print ("Second argument - number scan: %s" % str(sys.argv[2]))
  loop = int(sys.argv[2])+1
except: 
  loop=6 	#testing 10/20/40/100/200/400...
  print ("Default rotation steps: "+ str(loop) ) 

if piCamera:
  sWidth =100 	# width scann
  sTop=430 ##430 #	10 ...11cm #150 // ping 3.6cm ###12cm max 3 cm min --0-500 
  sBott=550

if webCamera:
  sWidth =120
  sTop=100 # height-height/9   
  sBott=200

axisX=width/2-120 #800 ##1200 
endX=axisX-sWidth+50 #50 only right side from axis 
startx=width-axisX-sWidth-20 
nasDef = 1.55  #

rad =height-sTop-sBott+1 #rows

sMat = [[ 0 for i in range(loop+1)] for j in range(rad+1) ] #man data matrix
sVec = [ 0 for j in range(rad+1) ]                                                           #auxiliary vector   
ramdiskPath = "/home/pi/ramdisk/" #temporary data storage

xyzFile = ramdiskPath+datName+'.xyz'
#------------------------------/main-setup
kroky=1
bb=0 #num points 
#------------------------------------
if piCamera:
   if dayLight:
     cam.brightness = 30 ##30ok #25 #35
   else:
     cam.brightness = 60

   if lightObject:
     cam.brightness = 10 #15ok
     cam.contrast=30

   cam.start_preview()
   #cam.annotate_background = cBlu #Color('blue')
   #cam.annotate_foreground = cWhi #Color('yellow')
   cam.annotate_text = "octopusengine 3D scanner"
   sleep(3)
   cam.stop_preview()

#---------------------------------
#oeGPIO.setupGPIO()
oeSetupGPIO()
#---------------------------------

def oneScan(angleStep): #=angle
 global sMat, bb, fw
 filename = "temp"+datName+".jpg"
 print filename
 filepath = ramdiskPath+filename


 if piCamera:
    cam.capture(filepath)

 if webCamera:
    cam.start()
    image = cam.get_image()
    cam.stop()
    pygame.image.save(image, filepath)

 screen=pygame.display.set_mode([screen_width,screen_height])

 obr = pygame.image.load(filepath)
 obrRect = obr.get_rect()
 screen.blit(obr, obrRect)    
 pygame.display.flip()
 
 # x,y points of screen
 #pygame.draw.line(screen,cRed,(1000,sTop),(1000,height-10),2)
 pygame.draw.line(screen,cBlu,(10,sTop),(width-10,sTop),2)
 pygame.draw.line(screen,cBlu,(10,height-sBott),(width-10,height-sBott),2)
 pygame.draw.line(screen,cBlu,(width/2,sTop),(width/2,height-sBott),2)
 pygame.draw.line(screen,cBlu,(width-startx,sTop),(width-startx,height-sBott),2)
 pygame.draw.line(screen,cBlu,(endX,sTop),(endX,height-sBott),2)
 pygame.draw.line(screen,cWhi,(axisX,sTop),(axisX,height-10),2)
 screen.set_at((10,10),cRed) 
 screen.set_at((11,11),cRed)
 pygame.display.flip() 

 rr=0
 x=startx #camera picture X
 y=sTop   #camera picture Y

 #main loop - search between (sBott and sTop) x (startx and endX) - for every angle
 while y<height-sBott: 
   #print screen.get_at((x*10,y*10)) #1 arg
   cR = screen.get_at((width-x,y))[0] # get RGB of one pixel from camera-image 
   cG = screen.get_at((width-x,y))[1]
   cB = screen.get_at((width-x,y))[2]
     
   if cR>fR and cG<fG and  cB<fB: #64/64/64 ##
         cR1 = screen.get_at((width-x-1,y))[0]
         cR2 = screen.get_at((width-x-2,y))[0]
         #cR3 = screen.get_at((width-x-5,y))[0]
         if cR1>cR: 
            x=x-1
            if cR2>cR1:
               x=x-1
         #sensitivity to red color
         rr=rr+1
         #print rr,x,y,cR,cG,cB
         #screen.set_at((width-x,y),cGre) 
         #screen.set_at((width-x-1,y),cGre) 
         xx=width-x-axisX             # = distance from axis > main scann data
         sMat[y-sTop][angleStep]=xx   # matrix RAW data y,a,d (y-sTop,angleStep,xx)
         bb = bb+1     
     
         y=y+kroky
         x=startx
   #else:  
   x=x+1
   if x>width-endX:
         x=startx
         y=y+kroky
         screen.set_at((width-x,y),cBlu) 
     
 #screen.blit(obr, obrRect)    

 
 #---filter1--- 
 if filter1: #doplneni pri 0 predchoyi prvek
    #y=sTop+1   
    y=sTop+2   
    while y<height-sBott-2:   #---filter1---to sVec      
        d = sMat[y-sTop][angleStep]
        #if d == 0:
        #if (sMat[y-sTop-1][angleStep]+sMat[y-sTop+1][angleStep])>0: 
        if (sMat[y-sTop-1][angleStep]>0 and sMat[y-sTop+1][angleStep])>0: 
          #mathematical average of the surrounding pixels
          d = (sMat[y-sTop-1][angleStep]+sMat[y-sTop][angleStep]+sMat[y-sTop+1][angleStep])/3 
          #d = (sMat[y-sTop-2][angleStep]+sMat[y-sTop-1][angleStep]+sMat[y-sTop][angleStep]+sMat[y-sTop+1][angleStep]+sMat[y-sTop+2][angleStep])/5   
          sVec[y-sTop] = d
          #sMat[y-sTop][angleStep]=d #todo
          x=width-axisX-d
          screen.set_at((width-x,y),cGre)
        else:  
          sVec[y-sTop] = sMat[y-sTop][angleStep]
        y=y+kroky 
  
    y=sTop+2   
    while y<height-sBott-2:       
        sMat[y-sTop][angleStep] = sVec[y-sTop]
        y=y+kroky 
  
 pygame.display.flip() 

 #---export xyz--- to filename.xyz 
 y=sTop+1   
 while y<height-sBott:       
    xx = sMat[y-sTop][angleStep]
    if xx!=0 and xx>-200:         
      angle=float(2*pi/(loop-1)*angleStep)
      rx=float(math.sin(angle)*xx*nasDef)
      ry=float(math.cos(angle)*xx*nasDef)
      rz = y
      co = str(rx)+" "+str(ry)+" "+str(rz)
      #cop = str(angle)+" > "+str(xx)+" > "+co
      #print cop
      fp.write(co+"\n") 
    y=y+kroky
 #time.sleep(0.2)    

#======================================== main scan loop =====================================
scanname = ramdiskPath+datName+'.csv'
fp = open(xyzFile,"a")
for st in range (loop-1):
   oneScan(st)
   print "--------------"
   co=name+" "+str(st+1)+"/"+str(loop-1)+" ("+str(bb)+")"
   print co
   if piCamera:
      cam.annotate_text = co
   oeMotCCWs(1600/(loop-1),100)    #1600 na 360 #100:22.5st,16ot #
fp.close()
#======================================== /main scan loop =====================================
#control display data
shift=5
zoom=2

scannRaw = ramdiskPath+datName +'.txt' #RAW scann data
scannImg = ramdiskPath+datName +'.jpg'
fw = open(scannRaw,"a")
screen=pygame.display.set_mode([screen_width,screen_height])
for u in range (loop-1): #angle
  for r in range (rad):  #row
      x=sMat[r][u]
      fw.write(str(x)+",")
      screen.set_at((u*shift+x*zoom,r*zoom),cGre) 
  pygame.display.flip()
  fw.write("\n")
fw.close()

sx =1200 #center 
sy =800
screen.set_at((sx,sy),cGre)
for u in range (0,360):
    x=200
    angle=float(u*2*pi)
    rx=int(float(sx+math.sin(angle)*x))
    ry=int(float(sy+math.cos(angle)*x))
    screen.set_at((rx,ry),cRed) 

pygame.display.flip()
pygame.image.save(screen,scannImg)

oeMotOff()
time.sleep(10)
#---end---
