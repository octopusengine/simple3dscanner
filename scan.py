#!/usr/bin/python
# Filename : scan.py

#-----------------------------------
## simple 3d scanner 
## 2016/04 - I am beginner, but it works ;-)
## 0.2 create xyz point cloud - directly posible import to MeshLab
##----------------------------------
import os, math, pygame, time
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO # for step motor
import picamera

width = 1600 #1024 #800
height = 1200 #768 #600
screen_width=width
screen_height=height
#-----------------------------main---setup
dayLight=1
lightObject=0
brownObject=0
blueObject=1

loop=600 	#testing 10/20/40/100/200/400...
name="robot" 	#scanning object name

sWidth =100 	# width scann
sTop=430 #	10 liska 11cm #150 vetsi / 300 ping 3.6cm ###12cm max 3 cm min --0-500 
sBott=550

axisX=width/2-120 #800 ##1200 
endX=axisX-sWidth+50 #50 nejde vubec za osu  
startx=width-axisX-sWidth-20 
nasDef = 1.9 

rad =height-sTop-sBott+1 #rows
#------------------------------/main-setup
sMat = [[ 0 for i in range(loop+1)] for j in range(rad+1) ]

ramdiskPath = "/home/pi/ramdisk/" #temporary data storage
#print "0,0", sMat[0][0]
#print math.sin(0)
pi=math.pi

#define colors for painting
cRed=(255,0,0)
cGre=(0,255,0)
cBlu=(0,0,255)
cWhi=(255,255,255)

kroky=1
bb=0 #num points 

#------------------------------------
pygame.init()

datName=name+datetime.now().strftime("%Y_%m_%d_%H_%M") 
xyzFile = ramdiskPath+datName+'.xyz'

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
EN2 = 22
DIR2 = 27
STEP2 = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO.setup(END2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(EN2, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
#---------------------------------

dStep=0.00001
def motCCWs(steps,slow): #down - modif old slow = step.Tilt / new mot2
   nas=2 #1600/ot #8=400 #16=200 for 360
   GPIO.output(EN2, False)
   GPIO.output(DIR2, False)
   for tx in range(steps*nas): 
     time.sleep(dStep*slow)  
     GPIO.output(STEP2, True)
     time.sleep(dStep*slow) 
     GPIO.output(STEP2, False)
   GPIO.output(EN2, True)  #aretace

def oneScan(angleStep): #=angle
 global sMat, bb
 global fw
 filename = "temp"+datName+".jpg"
 print filename
 filepath = ramdiskPath+filename
 cam.capture(filepath)

 screen=pygame.display.set_mode([screen_width,screen_height])

 obr = pygame.image.load(filepath)
 obrRect = obr.get_rect()
 screen.blit(obr, obrRect)    
 pygame.display.flip()

 rr=0
 x=startx
 y=sTop 
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

 while y<height-sBott:
   #print screen.get_at((x*10,y*10)) #1 arg
   cR = screen.get_at((width-x,y))[0]
   cG = screen.get_at((width-x,y))[1]
   cB = screen.get_at((width-x,y))[2]
     
   if cR>fR and cG<fG and  cB<fB: #64/64/64 ##
         #citlivost na RED: pro R 64 na svetle malo
         rr=rr+1
         #print rr,x,y,cR,cG,cB
         screen.set_at((width-x,y),cGre) 
         screen.set_at((width-x-1,y),cGre) 
         xx=width-x-axisX
         sMat[y-sTop][angleStep]=xx
         bb = bb+1
         
         if xx!=0 and xx>-200:         
          angle=float(2*pi/(loop-1)*angleAll)
          rx=float(math.sin(angle)*xx*nasDef)
          ry=float(math.cos(angle)*xx*nasDef)
          rz = y
          co = str(rx)+" "+str(ry)+" "+str(rz)
          cop = str(angle)+" > "+str(xx)+" > "+co
          #print cop
          fp.write(co+"\n")
     
         y=y+kroky
         x=startx
   #else:  
   x=x+1
   if x>width-endX:
         x=startx
         y=y+kroky
         screen.set_at((width-x,y),cBlu) 
     

 #screen.blit(obr, obrRect)    
 pygame.display.flip()
 time.sleep(2)

#=============================================================================
scanname = ramdiskPath+datName+'.csv'
fp = open(xyzFile,"a")
for st in range (loop-1):
   oneScan(st)
   print "--------------"
   co=str(st+1)+"/"+str(loop-1)+" ("+str(bb)+")"
   print co
   cam.annotate_text = co
   motCCWs(1600/(loop-1),500) #1600 na 360 #100:22.5st,16ot #
fp.close()
#----------------------------------------
#control display data
posun=6

scanname = ramdiskPath+datName +'.txt'
scannami = ramdiskPath+datName +'.jpg'
fw = open(scanname,"a")
screen=pygame.display.set_mode([screen_width,screen_height])
for u in range (loop-1):
  for r in range (rad):
      x=sMat[r][u]
      fw.write(str(x)+",")
      screen.set_at((u*posun+x,r),cGre) 
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

GPIO.output(EN2, True) #motor switch off 
#---end---
