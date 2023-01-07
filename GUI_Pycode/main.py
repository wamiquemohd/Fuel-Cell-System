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
root.geometry("1400x750") # set the window size 1400*850
#Global vars
data = ["0","0","0","0"];
data_VBAT=np.array([])
data_CBAT=np.array([])
data_VFC=np.array([])
data_CFC=np.array([])
width_plt = (root.winfo_screenwidth()/2) - 80
#print(width_plt)
height_plt = (root.winfo_screenheight()/2) - 150#180
#print(height_plt)
y = 700;#Buttons location in y axis
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
  plot_data_VBAT(float(x[0]))
  plot_data_CBAT(float(x[1]))
  plot_data_VFC(float(x[2]))
  plot_data_CFC(float(x[3]))

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
#------Plot Battery voltage---------------
def plot_data_VBAT(x):
    global data_VBAT
    V_BAT = float(x)/1000;
    if(len(data_VBAT) < 100):
            data_VBAT = np.append(data_VBAT,float(V_BAT))
    else:
            data_VBAT[0:99] = data_VBAT[1:100]
            data_VBAT[99] = float(V_BAT)
    lines_VBAT.set_xdata(np.arange(0,len(data_VBAT)))
    lines_VBAT.set_ydata(data_VBAT)
    canvas_VBAT.draw()
    root.after(1,plot_data_VBAT)

    #------Plot Battery current---------------
def plot_data_CBAT(x):
    global data_CBAT
    C_BAT = float(x)/1000;
    if(len(data_CBAT) < 100):
            data_CBAT = np.append(data_CBAT,float(C_BAT))
    else:
            data_CBAT[0:99] = data_CBAT[1:100]
            data_CBAT[99] = float(C_BAT)
    lines_CBAT.set_xdata(np.arange(0,len(data_CBAT)))
    lines_CBAT.set_ydata(data_CBAT)
    canvas_CBAT.draw()
    root.after(1,plot_data_CBAT)

   #------Plot Fuel-cell voltage---------------
def plot_data_VFC(x):
    global data_VFC
    V_FC = float(x)/1000;
    if(len(data_VFC) < 100):
            data_VFC = np.append(data_VFC,float(V_FC))
    else:
            data_VFC[0:99] = data_VFC[1:100]
            data_VFC[99] = float(V_FC)
    lines_VFC.set_xdata(np.arange(0,len(data_VFC)))
    lines_VFC.set_ydata(data_VFC)
    canvas_VFC.draw()
    root.after(1,plot_data_VFC)

      #------Plot Fuel-cell current---------------
def plot_data_CFC(x):
    global data_CFC
    C_FC = float(x)/1000;
    if(len(data_CFC) < 100):
            data_CFC = np.append(data_CFC,float(C_FC))
    else:
            data_CFC[0:99] = data_CFC[1:100]
            data_CFC[99] = float(C_FC)
    lines_CFC.set_xdata(np.arange(0,len(data_CFC)))
    lines_CFC.set_ydata(data_CFC)
    canvas_CFC.draw()
    root.after(1,plot_data_CFC)
#------create Plot object on GUI----------
# add figure canvas
#------plot for Battery voltage-----------
fig_VBAT = Figure();
ax_VBAT = fig_VBAT.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax_VBAT.set_title('Battery voltage');
ax_VBAT.set_xlabel('Time')
ax_VBAT.set_ylabel('Voltage')
ax_VBAT.set_xlim(0,100)
ax_VBAT.set_ylim(0,20)
lines_VBAT = ax_VBAT.plot([],[])[0]

canvas_VBAT = FigureCanvasTkAgg(fig_VBAT, master=root)  # A tk.DrawingArea.
canvas_VBAT.get_tk_widget().place(x = 10,y=10, width = width_plt,height = height_plt)
canvas_VBAT.draw()

#------plot for Battery current-----------
fig_CBAT = Figure();
ax_CBAT = fig_CBAT.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax_CBAT.set_title('Battery current');
ax_CBAT.set_xlabel('Time')
ax_CBAT.set_ylabel('Current')
ax_CBAT.set_xlim(0,100)
ax_CBAT.set_ylim(0,10)
lines_CBAT = ax_CBAT.plot([],[])[0]

canvas_CBAT = FigureCanvasTkAgg(fig_CBAT, master=root)  # A tk.DrawingArea.
width_height_canvas_VBAT = canvas_VBAT.get_width_height()
canvas_CBAT.get_tk_widget().place(x = width_height_canvas_VBAT[0] + (width_height_canvas_VBAT[0])/10,y=10, width = width_plt,height = height_plt)
canvas_CBAT.draw()

#------plot for Fuel-cell voltage-----------
fig_VFC = Figure();
ax_VFC = fig_VFC.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax_VFC.set_title('Fuel-cell voltage');
ax_VFC.set_xlabel('Time')
ax_VFC.set_ylabel('Voltage')
ax_VFC.set_xlim(0,100)
ax_VFC.set_ylim(0,65)
lines_VFC = ax_VFC.plot([],[])[0]

canvas_VFC = FigureCanvasTkAgg(fig_VFC, master=root)  # A tk.DrawingArea.
width_height_canvas_VBAT = canvas_VBAT.get_width_height()
canvas_VFC.get_tk_widget().place(x = 10,y=width_height_canvas_VBAT[1] - 130, width = width_plt,height = height_plt)
canvas_VFC.draw()

#------plot for Fuel-cell current-----------
fig_CFC = Figure();
ax_CFC = fig_CFC.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax_CFC.set_title('Fuel-cell current');
ax_CFC.set_xlabel('Time')
ax_CFC.set_ylabel('Current')
ax_CFC.set_xlim(0,100)
ax_CFC.set_ylim(0,20)
lines_CFC = ax_CFC.plot([],[])[0]

canvas_CFC = FigureCanvasTkAgg(fig_CFC, master=root)  # A tk.DrawingArea.
width_height_canvas_VBAT = canvas_VBAT.get_width_height()
canvas_CFC.get_tk_widget().place(x = width_height_canvas_VBAT[0] + (width_height_canvas_VBAT[0])/10,y=width_height_canvas_VBAT[1] - 130, width = width_plt,height = height_plt)
canvas_CFC.draw()

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
#exit Button
root.update()
exitButton = ttk.Button(root, text="Quit", command=root.destroy);
exitButton.pack(side="left" , fill="x");
exitButton.place(x=1300, y=y)
while 1:
    client.loop_start() #contineously checking for message
    root.mainloop()

