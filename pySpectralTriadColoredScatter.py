import serial  
import numpy   as np
import matplotlib.pyplot as plt  
import matplotlib.colors
from drawnow import *  
from serial import Serial
from scipy.interpolate import interp1d, InterpolatedUnivariateSpline
 
spectreData = serial.Serial("COM23", 115200) # replace by your real comport, on Linux it is something like "/dev/ttyACMx"
spectreData.reset_input_buffer()
resolution = 1000



loop=True

mp=interp1d([410,610,680,730,760,860,940],[100,200,300,400,500,600,720]) #mapping the sensor wavelenghts to the linear space (sometimes delta=25 sometimes 35 or 50...
 
spectreReadings = [0.0,0.0,0.0,0.0,0.0,0.0,]
spectreWavelenghts =[450,500,550,570,600,650] 
x = np.linspace(0, 5, num=6, endpoint=True)
xNew = np.linspace(0, 5, num=resolution, endpoint=True)
defaultYLimit = 700
wLspace = np.linspace(450, 650, num=resolution, endpoint=True) 
# ----------------------------------------------------------
norm = matplotlib.colors.Normalize(410,650)

fig,ax=plt.subplots() 	

plt.ion()   
  
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
	plt.ylabel('28.6 nW/cm2/count')
	plt.xlabel('Wavelength in nm')
	plt.xrange=[450,650]
    
	plt.legend(loc='upper left')                

	plt.scatter(wLspace,f(mp(wLspace)), c=wLspace, norm=norm)
	sc = ax.scatter(wLspace,f(mp(wLspace)), c=wLspace, norm=norm)
	#fig.colorbar(sc, orientation="horizontal")
	#plt.draw()	
	plt.show() 
	
while (loop):            
	while (spectreData.inWaiting()== 0):        
		pass            
	spectreString = spectreData.readline().decode('utf8')
	spectreList = spectreString.split(",")
	
	if(len(spectreList)==6):
		for num, value in enumerate(spectreList,start=0):
			spectreReadings[num]=float(value)
			
		defaultYLimit=max(spectreReadings)*1.1 # univariatespline is not a cubic one and WILL stay inside the plot area, at least at the top
		
		f=interp1d(x,spectreReadings,kind='cubic')
		#f=InterpolatedUnivariateSpline(x,spectreReadings)
		#plt.pause(.000001)  
		drawnow(doPlot)
	

print(".")
	