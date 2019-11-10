import serial  
import numpy   as np
import matplotlib.pyplot as plt
from drawnow import *  
from serial import Serial
from scipy.interpolate import interp1d
import pandas as pd

spectreData = serial.Serial("COM23", 115200) 

loop=True

spectreReadings = [0.0,0.0,0.0,0.0,0.0,0.0] 
x = np.linspace(450.00, 650.00, num=6, endpoint=True)
defaultYLimit = 860
xnew = np.linspace(450.00, 650.00, num=6, endpoint=True) 
fig = plt.figure()
plt.ion()     

def getMaximumIntensity(currentReadings):
    maxIntensityIndex = 0
    for num, value in enumerate(currentReadings,start=1):
        if (value > currentReadings[maxIntensityIndex]):
                maxIntensityIndex = num
    return maxIntensityIndex
        
def handle_close(evt):
	spectreData.reset_input_buffer()
	plt.ioff()
	plt.close()
	global loop
	loop=False
	#print("close event")
	#exit()
	#sys.exit()
 
def doPlot():     
	fig.canvas.mpl_connect('close_event', handle_close) # figured out finally how to close the "groundhog" window
	plt.ylim(0,defaultYLimit)                            
	plt.title('Spectral Response')           
	plt.grid(True)                              
	plt.ylabel('Intensity Count')    
	plt.xlabel('Wavelength in nm')                      
	#plt.plot(spectreReadings, 'ro-', label='Spectral readings') 
	plt.plot(x, spectreReadings, 'o', xnew, f(xnew), '-')       
	plt.legend(loc='upper left')                
	 
while (loop):            
	while (spectreData.inWaiting()== 0):        
		pass            
	spectreString = spectreData.readline().decode('utf8')
	spectreList = spectreString.split(",")
	if(len(spectreList)==6):
		for num, value in enumerate(spectreList,start=0):
			spectreReadings[num]=float(value)
        
		maxIntensityIndex = getMaximumIntensity(spectreReadings)
		print("Maximum intensity is " + str(spectreReadings[maxIntensityIndex]))
        
		defaultYLimit=max(spectreReadings)*1.1 # thus, the cubic spline should remain inside the plotarea
		f=interp1d(x,spectreReadings,kind='cubic')

		drawnow(doPlot)

data = {'Wavelength':[x],
        'Intensity':[spectreReadings]}        
df = pd.DataFrame(data, columns= ['Wavelength', 'Intensity'])
export_csv = df.to_csv (r'C:\Users\debacle\Documents\Plot\DAQ\export_dataframe.csv', index = True, header=True)
#export_csv = df.to_csv (r'C:\Users\debacle\Documents\Plot\DAQ\export_dataframe.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path        
print(".")
