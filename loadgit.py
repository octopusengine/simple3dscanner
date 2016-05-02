import random, sys, os, time
from time import sleep

import urllib2 
import zipfile
import shutil

import subprocess
import string

#----------------------------------
ramdiskPath = "/home/pi/ramdisk/"
updaPathDw = r"/home/pi/github/"
urlUpdate='https://raw.githubusercontent.com/octopusengine/simple3dscanner/master/'
#https://github.com/octopusengine/simple3dscanner/blob/master/scan.py
#https://raw.githubusercontent.com/octopusengine/simple3dscanner/master/scan.py


numUpdaOk=0
numUpda=0

#----------------------------------
def doNetUpdate(upath,ufile):
   global numUpda, numUpdaOk
   print ufile   
   #hh.neXtxt2("d0",ufile)
   try:
     ufileNet=ufile
     #ufileNet=ufile.lower()
     urlr = urllib2.urlopen(urlUpdate+ufileNet)
     utemp = urlr.read()
     urlr.close() 

     fwu = open(ramdiskPath+ufile,"w")
     fwu.write(utemp)
     fwu.close()
     #hh.neXtxt2("p2",ramdiskPath+ufile) 
       
     shutil.copy(ramdiskPath+ufile,upath+ufile)
     hh.iSRAdd("net[<span class=red>ok</span>] >> "+ufile)
     numUpdaOk=numUpdaOk+1     
     print "file update OK:  "+str(numUpdaOk)
     time.sleep(0.5)     
 
   except:
     numUpda=numUpda+1
     #hh.infoRC(".....",tr2,"WHI") 
     #hh.iSRAdd("net[ &nbsp; ] .. "+ufile)
     #hh.neXtxt2("p2","file update OK:  "+str(numUpdaOk)) 
     #hh.neXtxt2("p3","no update... "+str(numUpda))

   proc = (numUpda+numUpdaOk)*10
   #hh.neXcmd("page print")
   #hh.neXval("j0",str(int(proc)))
   #hh.neXtxt2("pp",str(int(proc))+"%")


print "load scan.py > github"

doNetUpdate(updaPathDw,'scannStart.py')     
doNetUpdate(updaPathDw,'oeGPIO.py')
doNetUpdate(updaPathDw,'scannHelp.py')
doNetUpdate(updaPathDw,'scannInit.py')
doNetUpdate(updaPathDw,'scannConfig.py')

