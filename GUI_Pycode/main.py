import paho.mqtt.client as paho
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sys
import datetime
import time
import os
import json
import tkinter as tk
from tkinter import ttk

#GUI codes
#Create main page
root = tk.Tk();
root.title("GUI");
root.configure(background = 'light blue')
root.geometry("700x500") # set the window size
#Global vars
data = ["0","0","0","0"];
data_VBAT = np.array([])
y = 450;#Buttons location in y axis
#host name is localhost because both broker and python are Running on same machine/Computer.
broker="localhost";  #host name
port=1883;
topic="Sub"
ACCESS_TOKEN='TestCode' #not manditory
#Publisher
def on_publish(client,userdata,result): #create function for callback
  print("published data is : ")
  pass
#Subscriber
def on_message(client, userdata, message):
  print("received data is :")  
  print(str(message.payload.decode("utf-8")) ) #printing Received message
  print("..................................");
  data = str(message.payload.decode("utf-8"));
  print("This is data:" + data);
  split_data(data);
#Spliting data
def split_data(data):
  x = data.split(" ");
  print(x[0]);# Battery voltage
  print(x[1]);# Battery current
  print(x[2]);# Fuel cell voltage
  print(x[3]);# Fuel cell current
  print("Task done");
  plot_data(float(x[0]))

client= paho.Client("user") #create client object

client.on_publish = on_publish #assign function to callback
client.username_pw_set(ACCESS_TOKEN) #access token from thingsboard device
client.connect(broker,port,keepalive=60) #establishing connection

client.on_message=on_message
   
print("connecting to broker host",broker)
print("On topic",topic)
client.connect(broker,port)#connection establishment with broker
print("Waiting for data...................")    
client.subscribe(topic)#subscribe topic test

#------create plot function---------------
def plot_data(x):
    global data_VBAT
    V_BAT = float(x)/1000
    print(V_BAT)
    if(len(data_VBAT) < 100):
            data_VBAT = np.append(data_VBAT,float(V_BAT))
    else:
            data_VBAT[0:99] = data_VBAT[1:100]
            data_VBAT[99] = float(data_VBAT[0:4])
    lines.set_xdata(np.arange(0,len(data_VBAT)))
    lines.set_ydata(data_VBAT)
    canvas.draw()
    root.after(1,plot_data)

#------create Plot object on GUI----------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('Battery voltage');
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.set_xlim(0,100)
ax.set_ylim(0,20)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().place(x = 10,y=10, width = 500,height = 400)
canvas.draw()

#----------Create Buttons-----------------
#Buttons Function
#Turn on Battery PMC
def TurnOnBatPMC():
    ret= client.publish("test","TurnOnBATPMC")
#Button
root.update()
BATPMCONButton = ttk.Button(root, text="Turn on Bat PMC", command=TurnOnBatPMC);
BATPMCONButton.pack();
BATPMCONButton.place(x=60, y=y)
#Turn off Battery PMC
def TurnOffBatPMC():
    ret= client.publish("test","TurnOffBATPMC")
#Button
root.update()
BATPMCOFFButton = ttk.Button(root, text="Turn off Bat PMC", command=TurnOffBatPMC);
BATPMCOFFButton.pack();
BATPMCOFFButton.place(x=BATPMCONButton.winfo_x()+BATPMCONButton.winfo_reqwidth()+10, y=y)
#BATPMCOFFButton.place(x=170, y=y)
#Turn on Fuelcell PMC
def TurnOnFCPMC():
    ret= client.publish("test","TurnOnFCPMC")
#Button
root.update()
FCPMCONButton = ttk.Button(root, text="Turn on FC PMC", command=TurnOnFCPMC);
FCPMCONButton.pack(side="right" , fill="x");
FCPMCONButton.place(x=BATPMCOFFButton.winfo_x()+BATPMCOFFButton.winfo_reqwidth()+10, y=y)
#FCPMCONButton.place(x=280, y=y)
#Turn off Fuelcell PMC
def TurnOffFCPMC():
    ret= client.publish("test","TurnOffFCPMC")
#Button
root.update()
FCPMCOFFButton = ttk.Button(root, text="Turn off FC PMC", command=TurnOffFCPMC);
FCPMCOFFButton.pack(side="right" , fill="x");
FCPMCOFFButton.place(x=FCPMCONButton.winfo_x()+FCPMCONButton.winfo_reqwidth()+10, y=y)
#FCPMCOFFButton.place(x=390, y=y)
while 1:
    client.loop_start() #contineously checking for message
    root.mainloop()

