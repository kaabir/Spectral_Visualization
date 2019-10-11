import serial # import Serial Library
import numpy as np # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

LuxR= []
arduinoData = serial.Serial('com23', 9600) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0

def makeFig(): #Create a function that makes our desired plot                             #Set y min and max values
    plt.title('Sensor Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('LDR O/P')                            #Set ylabels
    plt.plot(LuxR, 'ro-', label='LDR')       #plot the Luxerature
    plt.legend(loc='upper left')                    #plot the legend
    

while True: # While loop that loops forever
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline().decode('utf8')  #read the line of text from the serial port
    dataArray = arduinoString.split(',')   #Split it into an array called dataArray
    Lux = float( dataArray[0])            #Convert first element to floating number and put in Lux
    LuxR.append(Lux)                     #Build our LuxR array by appending Lux readings
    drawnow(makeFig)                       #Call drawnow to update our live graph
    plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
    cnt=cnt+1
    if(cnt>150):                            #If you have 50 or more points, delete the first one from the array
        LuxR.pop(0)                       #This allows us to just see the last 50 data points
