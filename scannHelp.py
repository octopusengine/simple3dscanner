#!/usr/bin/python
# Filename : scannHelp.py
#-----------------------------------
## simple 3d scanner - octopusengine.eu

def help():
  print("----------------------------------------------------------------")
  print("simple3dscanner 0.35         ---        help       ---          ")
  print("----------------------------------------------------------------")
  print("scannStart.py [projectName] [numberOfScann]") 
  print("Correct input example: scannStart.py test 100") 
  print(">>First argument > "test" => project name" )
  print("  (default: noname)" )
  print("  create file projectName-dateTime.xzy" )
  print(">>Second argument > 100 => number of scann") 
  print("  100 > one step 360/100 degrees") 
  print("  (default: 6, for quick test)")
  print("----------------------------------------------------------------")
  print("(c) https://github.com/octopusengine/simple3dscanner")

#---end---
