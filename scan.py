#!/usr/bin/python
# Filename : scan.py
#-----------------------------------
## simple 3d scanner - octopusengine.eu
## 2016/04 - I am beginner, but it works ;-)
## 0.21 create xyz point cloud - directly posible import to MeshLab
## 0.33 oeGPIO, oeHelp
##----------------------------------
import os, sys, math, pygame, time
from datetime import datetime
from time import sleep
#import RPi.GPIO as GPIO # for step motor
import picamera

from oeGPIO import * #oeSetupGPIO
from oeHelp import *

width = 1600 #1024 #800
height = 1200 #768 #600
screen_width=width
screen_height=height

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

#---------------------------------
dayLight=1
lightObject=0
brownObject=0
blueObject=0

filter1=1


sWidth =100 	# width scann
sTop=430 ##430 #	10 liska 11cm #150 vetsi / 300 ping 3.6cm ###12cm max 3 cm min --0-500 
sBott=550

axisX=width/2-120 #800 ##1200 
endX=axisX-sWidth+50 #50 nejde vubec za osu  
startx=width-axisX-sWidth-20 
nasDef = 1.6  #

rad =height-sTop-sBott+1 #rows

sMat = [[ 0 for i in range(loop+1)] for j in range(rad+1) ] #man data matrix
sVec = [ 0 for j in range(rad+1) ]                                                           #auxiliary vector   
ramdiskPath = "/home/pi/ramdisk/" #temporary data storage

xyzFile = ramdiskPath+datName+'.xyz'
#------------------------------/main-setup
#print "0,0", sMat[0][0]
#print math.sin(0)
pi=math.pi

#define colors for painting
cRed=(255,0,0)
cGre=(0,255,0)
cBlu=(0,0,255)
cYel=(255,255,0)
cWhi=(255,255,255)

kroky=1
bb=0 #num points 

#------------------------------------
pygame.init()
#cam = pygame.camera.Camera("/dev/video0",(width,height),"RGB")
cam= picamera.PiCamera()
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
##hard experiments
if dayLight:
       fR=60 #64 #50
       fG=64
       fB=64
else: 
       fR=80
       fG=50
       fB=50 

if brownObject:
       fR=70 #64
       fG=50
       fB=64 

if blueObject:
       fR=16 #64
       fG=160
       fB=160
#---------------------------------

def oneScan(angleStep): #=angle
 global sMat, bb, fw
 filename = "temp"+datName+".jpg"
 print filename
 filepath = ramdiskPath+filename
 cam.capture(filepath)
 screen=pygame.display.set_mode([screen_width,screen_height])

 obr = pygame.image.load(filepath)
 obrRect = obr.get_rect()
 screen.blit(obr, obrRect)    
 pygame.display.flip()
 
 # x,y points of screen
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
   cR = screen.get_at((width-x,y))[0]
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
        if (sMat[y-sTop-1][angleStep]+sMat[y-sTop+1][angleStep])>0: 
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
