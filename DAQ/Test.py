import serial  
import numpy   as np
import matplotlib.pyplot as plt
from drawnow import *  
from serial import Serial
from scipy.interpolate import interp1d
import pandas as pd
import datetime

spectreData = serial.Serial("COM23", 115200) 

loop=True

spectreReadings = [0.0,0.0,0.0,0.0,0.0,0.0] 
x = np.linspace(450.00, 650.00, num=6, endpoint=True)
defaultYLimit = 860
xnew = np.linspace(450.00, 650.00, num=6, endpoint=True) 
fig = plt.figure()
plt.ion()     

def getMaximumIntensity(currentReadings):
    maxIntensityIndex = -1
    for num, value in enumerate(currentReadings,start=1):
        if (maxIntensityIndex == -1 or value > currentReadings[maxIntensityIndex]):
                maxIntensityIndex = num
    return maxIntensityIndex
        
def handle_close(evt):
	spectreData.reset_input_buffer()
	plt.ioff()
	plt.close()
	global loop
	loop=False

def plot1():
    plt1 = fig.add_subplot(221)     
    fig.canvas.mpl_connect('close_event', handle_close) # figured out finally how to close the "groundhog" window
    plt1.set_ylim(0,defaultYLimit)                            
    plt1.set_title('Spectral Response')           
    plt1.grid(True)                              
    plt1.set_ylabel('Intensity Count')    
    plt1.set_xlabel('Wavelength (in nm)')                          
    plt1.legend(loc='upper left')
    plt1.plot(x, spectreReadings, 'o', xnew, f(xnew), '-')
    
    plt2 = fig.add_subplot(222)
    plt2.set_title('Max Wavelength vs Time')
    plt2.set_ylim(0,defaultYLimit)
    plt2.grid(False)
    plt2.set_ylabel('Maximum Wavelength')
    plt2.set_xlabel('Time (in seconds)')
    plt2.plot(times, maxReadingsTillNow)

times = []
maxReadingsTillNow = []
startTime =  datetime.datetime.now()
while (loop):            
	while (spectreData.inWaiting()== 0):        
		pass            
	spectreString = spectreData.readline().decode('utf8')
	spectreList = spectreString.split(",")
	if(len(spectreList)==6):
		readingArrivalTime = datetime.datetime.now()
		for num, value in enumerate(spectreList,start=0):
			spectreReadings[num]=float(value)
        
		maxIntensityIndex = getMaximumIntensity(spectreReadings)
		if(maxIntensityIndex != -1 and maxIntensityIndex < len(spectreReadings)):
			print("Maximum intensity is " + str(spectreReadings[maxIntensityIndex]))
			maxReadingsTillNow.append(spectreReadings[maxIntensityIndex])
			times.append((readingArrivalTime - startTime).total_seconds())
		else:
			print("Maximum intensity anamoly detected ")           
        
		defaultYLimit=max(spectreReadings)*1.1 # thus, the cubic spline should remain inside the plotarea
		f=interp1d(x,spectreReadings,kind='cubic')
		drawnow(plot1)
print(".")