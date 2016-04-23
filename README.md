# simple3dscanner
<b>What do you need for program testing?</b><br /> 
Raspberry pi 2, Raspberrypi camera, - it works in Python 2.7 with Pygame module<br /> 
<i>setup ramdisk (temporary files):</i><br />
<code>sudo mkdir /home/pi/ramdisk</code><br /> 
<code>sudo nano /etc/fstab</code><br />
and add the line<br />
<code>tmpfs /home/pi/ramdisk tmpfs defaults,size=100M 0 0</code><br /> 
<br />


<br />
simple starting on your Raspberry pi:<br />
<code>sudo python scan.py [projectName] [numberOfScann] </code><br />

<b>What more do you need for scanner testing?</b><br /> 
red line laser, voltage source 12V + step motor with driver<br /> 
I am using Nema and A4988<br />  
...point cloud to MeshLab

picture of hardware:<br /> 
https://www.instagram.com/p/BEYQFLeR7QY/?taken-by=octopusengine

schematic:<br /> 
http://www.octopusengine.eu/2016gal/scanner-schematic.gif

<hr /> 
simple idea - how to create points cloud:

loop {

  > take a picture 

  > recognize red line

  > transform to xyz
  
  }

 example of processing<br /> 
  https://www.instagram.com/p/BEYRg99R7TE/?taken-by=octopusengine

<hr />
<h3>History:</h3> 

 <b>2016/04</b><br /> 
 0.10 first experiment, it works! I was really surprised ;-)<br /> 
 0.20 my first "open source" post for GitHub<br /> 
 0.30 oeHelp, oeGPIO<br />
 
 
<h3>ToDo:</h3>

 better user input / GUI<br /> 
 light detection / daylight.. color of object..<br /> 
 faster computing / C library or Cython testing<br /> 
 second line laser (FET transistor switching?) <br /> 
 digital filter - RAW data 2D filtering<br /> 
 converting to STL<br /> 
 
  
