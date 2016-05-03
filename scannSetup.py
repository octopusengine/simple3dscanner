#!/usr/bin/python
# Filename : scanSetup.py
#-----------------------------------
## simple 3d scanner - octopusengine.eu
## 2016/05 - external setup file
##----------------------------------
global dayLight,lightObject,brownObject,blueObject

#--- camera selection:
piCamera=1    #ok-beta
webCamera=0   #alpha-testing
mobilCamera=0 #no

#--- experimental light and object setup:
dayLight=1    
lightObject=1
brownObject=0
blueObject=0

#--- filters
filter13=1  #ok-beta
filter15=1  #ok-beta
filter29=1  #alpha
## ----------------------------


##hard experiments
if dayLight:
       fR=60 #64 #50
       fG=64
       fB=64
else: 
       fR=90
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

#if lightObject:
#       fR=150 #64
#       fG=64
#       fB=64

#---------------------------------



#---end---
