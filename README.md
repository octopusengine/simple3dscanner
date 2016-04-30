# simple3dscanner

<img src="https://raw.githubusercontent.com/octopusengine/simple3dscanner/master/images/fig5-ball-schematic.jpg" alt="fig5-ball-schematic.jpg" width="600">

It is only the first step - my first project here.<br /> 
I would be very happy to see people "testing" or forking this and creating bigger and better versions ;-)<br /> 
I'm also grateful for any advice, error correction or recommendations how to proceed...<br />
Also look at pictures in a directory <b>images</b> - it was a hard job to explain how easy principle I use ;-)<br /> 

<b>What do you need for program testing?</b><br />
For imperfect testing you can use only Raspberry pi 2 and free webcam, without step motor.<br />
set only:<br />
<code>piCamera=0</code><br />
<code>webCamera=1</code><br />

But I recommend faster Raspberry pi 3 and <b>Raspberrypi camera (full HD)</b><br />
<code>piCamera=1</code> is deafult setting<br />


Program <b>scan.py</b> works in Python 2.7 with Pygame module<br />
<br />
<i>How setup ramdisk (temporary files)?</i><br />
<code>sudo mkdir /home/pi/ramdisk</code><br /> 
<code>sudo nano /etc/fstab</code><br />
and add the line<br />
<code>tmpfs /home/pi/ramdisk tmpfs defaults,size=100M 0 0</code><br /> 
<br />

<br />
simple starting on your Raspberry pi:<br />
<code>sudo python scan.py [projectName] [numberOfScann] </code><br />
<i>numberOfScann = rotation steps</i><br />

<b>What more do you need for scanner testing?</b><br /> 
red line laser, voltage source 12V + step motor with driver<br /> 
I am using Nema and A4988<br />  

picture of hardware - first alpha edition (with one laser):<br /> 
<img src="https://raw.githubusercontent.com/octopusengine/simple3dscanner/master/images/scanner-hardware1.jpg" alt="scanner-hardware1.jpg" width="600">

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

Point cloud file xyz is simple "txt" format:<br />
<i>x1 y1 z1<br />
x2 y2 z2<br />
...<br />
xn yn zn<br />
<br />
for exaple 5 points:<br />
-14.7657331345 -8.525 177<br />
-10.7387150069 -6.2 178<br />
-1.34233937587 -0.775 179<br />
32.2161450208 18.6 288<br />
41.6125206518 24.025 311<br />
49.666556907 28.675 318 <br />
<br />
</i>





<hr />
Import point cloud (file.xyz) to <a href=http://meshlab.sourceforge.net/>MeshLab:</a><br /> 
File / Import mesh...<br /> 
<br /> 

<hr />
<h3>History:</h3> 

 <b>2016/04</b><br /> 
 0.10 first experiment, it works! I was really surprised ;-)<br /> 
 0.20 my first "open source" post for GitHub<br /> 
 0.30 oeHelp, oeGPIO<br />
 0.33 filter1 - digital filter <i>Xn=aver(Xn-1,Xn,Xn+1)</i><br />
 
<h3>ToDo:</h3>

 better user input / GUI<br /> 
 light detection / daylight.. color of object..<br /> 
 faster computing / C library or Cython testing<br /> 
 second line laser (FET transistor switching?) <br /> 
 digital filter - RAW data 2D filtering<br /> 
 converting to STL<br /> 
 
<h3>Licence:</h3>
MIT<br /> 
<i>Copyright (c) 2016 Octopusengine.eu</i><hr /> 
