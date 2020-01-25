import serial
import numpy   as np
import matplotlib.pyplot as plt
from drawnow import *  
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

loop=True
allReadings = []
spectreReadings = [0.0,0.0,0.0,0.0,0.0,0.0] 
x = np.linspace(450.00, 650.00, num=6, endpoint=True)
defaultYLimit = 1024
defaultWavelengthMaxLimit = 700.00
defaultWavelengthMinLimit = 400.00
maxIntensityMaxLimit = 22000
maxIntensityMinLimit = 0
xnew = np.linspace(450.00, 650.00, num=6, endpoint=True) 
fig = plt.figure()
plt.ion()     

def getMaximumIntensity(currentReadings):
    maxIntensityIndex = -1
    for num, value in enumerate(currentReadings,start=0):
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
    ax2.set_ylim(maxIntensityMinLimit,maxIntensityMaxLimit)
    ax2.grid(True)
    ax2.set_ylabel('Maximum Intensity')
    ax2.set_xlabel('Time (in seconds)')
    ax2.plot(times, intensities, 'g')
    plt.tight_layout()
    
    
    ax3 = fig.add_subplot(313)
    ax3.set_title('Max Wavelength vs Time')
    ax3.set_ylim(defaultWavelengthMinLimit,defaultWavelengthMaxLimit)
    ax3.grid(True)
    ax3.set_ylabel('Maximum Wavelength (in nm)')
    ax3.set_xlabel('Time (in seconds)')
    ax3.plot(times, wavelengths, 'b')
    plt.tight_layout()

times = []
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
			allReadings.append(spectreReadings[:])
			time = (readingArrivalTime - startTime).total_seconds()
			intensity = MaxIntensity(spectreReadings[maxIntensityIndex], x[maxIntensityIndex], time)
			maxIntensities.append(intensity)
			times.append(time)
		else:
			print("Maximum intensity anamoly detected ")           
        
		defaultYLimit=max(spectreReadings)*1.3
		f=interp1d(x,spectreReadings,kind='cubic')
		drawnow(plot1)

wavelength450 = list(map(lambda x: x[0], allReadings))
wavelength500 = list(map(lambda x: x[1], allReadings))
wavelength550 = list(map(lambda x: x[2], allReadings))
wavelength570 = list(map(lambda x: x[3], allReadings))
wavelength600 = list(map(lambda x: x[4], allReadings))
wavelength650 = list(map(lambda x: x[5], allReadings))
data = {'450':wavelength450, 
        '500':wavelength500, 
        '550':wavelength550,
        '570':wavelength570,
        '600':wavelength600, 
        '650':wavelength650, 
        'Time':times}        
df = pd.DataFrame(data, columns= ['450', '500', '550', '570', '600', '650', 'Time'])
export_csv = df.to_csv (r'C:\Users\debacle\Documents\Plot\DAQ\export_dataframe1.csv', index = True, header=True)        
print(".")