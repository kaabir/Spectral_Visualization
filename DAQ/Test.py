import pyfirmata
import serial
import numpy   as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from drawnow import *  
from serial import Serial
from scipy.interpolate import interp1d
import pandas as pd
import datetime

class MaxIntensity:
    intensity = 0.0
    wavelength = 0.0
    time = 0
    
    def __init__(self,intensity, wavelength, time):
        self.intensity = intensity
        self.wavelength = wavelength
        self.time = time
        
        
spectreData = serial.Serial("COM23", 115200) 
#spectreData =[0.0,0.0,0.0,0.0,0.0,0.0] 

loop=True
allReadings = []
spectreReadings = [0.0,0.0,0.0,0.0,0.0,0.0] 
x = np.linspace(450.00, 650.00, num=6, endpoint=True)
defaultYLimit = 1024
defaultWavelengthLimit = 750.00
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
    fig.canvas.mpl_connect('close_event', handle_close)
    ax1 = fig.add_subplot(311, )      
    ax1.set_ylim(0,defaultYLimit)                            
    ax1.set_title('Spectral Response')           
    ax1.grid(True)                              
    ax1.set_ylabel('Intensity Count')    
    ax1.set_xlabel('Wavelength (in nm)')                          
    ax1.legend(loc='upper left')
    #ax1.xaxis.set_minor_locator(MultipleLocator(15))
    #ax1.xaxis.set_minor_formatter(FormatStrFormatter("%d"))
    ax1.plot(x, spectreReadings, 'o', xnew, f(xnew), '-')
    
    intensities = list(map(lambda x: x.intensity, maxIntensities))
    times =list(map(lambda x: x.time, maxIntensities))
    wavelengths = list(map(lambda x: x.wavelength, maxIntensities))
    
    ax2 = fig.add_subplot(312, autoscaley_on = True)
    ax2.set_title('Max Intensity vs Time')
    ax2.set_ylim(0,defaultYLimit)
    ax2.grid(True)
    ax2.set_ylabel('Maximum Intensity')
    ax2.set_xlabel('Time (in seconds)')
    ax2.plot(times, intensities, 'g')
    plt.tight_layout()
    
    
    ax3 = fig.add_subplot(313)
    ax3.set_title('Max Wavelength vs Time')
    ax3.set_ylim(0,defaultWavelengthLimit)
    ax3.grid(True)
    ax3.set_ylabel('Maximum Wavelength (in nm)')
    ax3.set_xlabel('Time (in seconds)')
    ax3.plot(times, wavelengths, 'b')
    plt.tight_layout()

#times = []
#maxIntensitiesTillNow = []
maxIntensities = []
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
			#maxIntensitiesTillNow.append(spectreReadings[maxIntensityIndex])
			allReadings.append(spectreReadings)
			time = (readingArrivalTime - startTime).total_seconds()
			intensity = MaxIntensity(spectreReadings[maxIntensityIndex], x[maxIntensityIndex], time)
			maxIntensities.append(intensity)
		else:
			print("Maximum intensity anamoly detected ")           
        
		defaultYLimit=max(spectreReadings)*1.3
		f=interp1d(x,spectreReadings,kind='cubic')
		drawnow(plot1)
"""
data = {'Wavelength':[x],'Intensity':[spectreReadings],'Time':[time]}        
df = pd.DataFrame(data, columns= ['Wavelength', 'Intensity', 'Time'])
df1 = df.transpose()
"""

wavelength450 = list(map(lambda x: x[0], allReadings))
wavelength490 = list(map(lambda x: x[1], allReadings))
wavelength530 = list(map(lambda x: x[2], allReadings))
wavelength570 = list(map(lambda x: x[3], allReadings))
wavelength610 = list(map(lambda x: x[4], allReadings))
wavelength650 = list(map(lambda x: x[5], allReadings))
data = {'450':wavelength450, 
        '490':wavelength490, 
        '530':wavelength530,
        '570':wavelength570,
        '610':wavelength610, 
        '650':wavelength650, 
        'Time':[time]}        
df = pd.DataFrame(data, columns= ['450', '490', '530', '570', '610', '650', 'Time'])
export_csv = df.to_csv (r'C:\Users\debacle\Documents\Plot\DAQ\export_dataframe.csv', index = True, header=True)        
print(".")