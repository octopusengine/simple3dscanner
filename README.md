# simple3dscanner
<b>What do you need for program testing?</b><br /> 
Raspberry pi 2, Raspberrypi camera, - it works in Python with Pygame module
<i>setup /ramdisk</i>

<b>What more do you need for scanner testing?</b><br /> 
red line laser, voltage source 12V + step motor with driver<br /> 
I am using NEMO and A4988 ...point cloud to MeshLab

picture of hardware:<br /> 
https://www.instagram.com/p/BEYQFLeR7QY/?taken-by=octopusengine

schematic:<br /> 
http://www.octopusengine.eu/2016gal/scanner-schematic.gif


simple idea - how to create points cloud:

loop {

  > take a picture 

  > recognize red line

  > transform to xyz
  
  }

 example of processing<br /> 
  https://www.instagram.com/p/BEYRg99R7TE/?taken-by=octopusengine

<hr />
<h3>HISTORY:</h3> 

 2016/04/18 - 0.1 first experiment, it works! I was really surprised ;-)<br /> 
 2016/04/21 - 0.2 my first "open source" pos on GitHub - simple starting on your Raspberry pi: sudo python scan.py<br /> 
 
<h3>TODO:</h3>

 better user input / GUI<br /> 
 light detection / daylight.. color of object..<br /> 
 faster computing / C library or Cython testing<br /> 
 digital filter - RAW data filtering<br /> 
 converting to STL<br /> 
 
  
