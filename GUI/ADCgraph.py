from tkinter import *
from tkinter import ttk
#for plotting
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
#for numbers
from random import random
from numpy import linspace
from numpy import zeros
import datetime
import SerialComms


class ADCgraph:
    titleFontSize = 8   #font size for subplot titles
    axesFontSize = 6
    refreshRate = 10    #number of frames per second
    VER_NUMBER = 0

    def __init__(self, parent, log_parent, ver):
        #store version number
        self.VER_NUMBER = ver
        #####   ADC graphs  #####
        #create figure for graphing
        self.f = Figure(figsize = (4,5), dpi = 100, tight_layout = 'true')
        #adc subplot initialization
        self.adcsub = [0,1,2,3]
        self.adcln = [0,1,2,3]
        self.xdata = [0,1,2,3]
        self.ydata = [0,1,2,3]
        loc = [1,2,3,4]
        for i in [0, 1, 2, 3]:
            self.adcsub[i] = self.f.add_subplot(4,1,loc[i])
            self.adcsub[i].set_title('ADC ' + str(i),fontsize = self.titleFontSize)
            self.adcsub[i].set_xlabel('Time (s)',fontsize = self.axesFontSize)
            self.adcsub[i].set_ylabel('V',fontsize = self.axesFontSize)
            self.adcsub[i].set_xticklabels([-5, -4, -3, -2, -1, 0], fontsize = self.axesFontSize)
            self.adcsub[i].set_yticklabels([0, 2048, 4096], fontsize = self.axesFontSize)
            self.xdata[i] = linspace(-5, 0, 51)
            self.ydata[i] = zeros(51)
            self.adcln[i], = self.adcsub[i].plot(self.xdata[i],self.ydata[i])
        #create canvas widget with figure embedded in it
        self.canvas = FigureCanvasTkAgg(self.f, parent)
        self.grid(column=0, row=0, sticky =(N,S,E,W), columnspan=4)
        #configure animation
        self.ani = animation.FuncAnimation(self.f, self.animateFcn, interval = (1000/self.refreshRate), init_func=self.animateInit, blit=True)
        #####   LOG area    #####
        #create button for logging data
        self.logging = False
        self.logBtn = ttk.Button(log_parent, text = 'Log', command = self.logBtnPress,width=10)
        self.logBtn.grid(column=2,row=0,sticky=(N,S,E,W))
        #create text entry for log file
        ttk.Label(log_parent, text = 'Filename:',anchor='w').grid(column=0, row=0, sticky=(N,S,E,W))
        self.logFileName = StringVar()
        self.logFileName.set(datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S') + '.csv')
        ttk.Entry(log_parent, textvariable=self.logFileName, width = 20).grid(column=1,row=0,sticky=(N,S,E,W))
        #create button for logging a flag
        self.logFlag = False
        ttk.Button(log_parent, text = 'Log Flag', command = self.logFlagBtnPress, width = 10).grid(column = 3, row = 0, sticky = (N,S,E,W))

    #call to grid function for GUI placement
    def grid(self, **keyword_params):
        self.canvas.get_tk_widget().grid(keyword_params)

    #initialization for animation (sets up backgrounds)
    def animateInit(self):
        for i in [0,1,2,3]:
            self.adcsub[i].set_xlim(-5, 0)
            self.adcsub[i].set_ylim(0, 4096)
        return tuple(self.adcln,)

    #animation function called once per frame
    def animateFcn(self,frame_num):
        #if we've got new data to plot/log
        if SerialComms.HARA.newData:
            #update graphs
            for i in [0,1,2,3]:
                self.ydata[i][:len(self.ydata[i])-1] = self.ydata[i][1:]
                self.ydata[i][len(self.ydata[i])-1] = SerialComms.HARA.adc[i]
                self.adcln[i].set_data(self.xdata[i],self.ydata[i])
            #if logging, populate row
            if self.logging:
                self.logfile.write(str(SerialComms.HARA.state) + ', ')
                self.logfile.write(str(SerialComms.HARA.adc[0]) + ', ')
                for i in [1,2,3]:
                    self.logfile.write(str(SerialComms.HARA.mux_val[i]) + ', ')
                    self.logfile.write(str(SerialComms.HARA.adc[i]) + ', ')
                    self.logfile.write(str(SerialComms.HARA.psi[i]) + ', ')
                    self.logfile.write(str(SerialComms.HARA.theta[i]) + ',')
                    self.logfile.write(str(SerialComms.HARA.xi[i])+ ',')
                    self.logfile.write(str(SerialComms.HARA.delta_i[i]) + ', ')
                    self.logfile.write(str(SerialComms.HARA.delta_j[i]) + ',')
                    self.logfile.write(str(SerialComms.HARA.sw[i]) + ', ')
                self.logfile.write('%d,' % self.logFlag)
                self.logFlag = False
                now = datetime.datetime.now()
                self.logfile.write('%d, %d, %d, %d\n' % (now.hour, now.minute, now.second, now.microsecond))
            #clear new data flag
            SerialComms.HARA.newData = False
        return tuple(self.adcln,)

    def logBtnPress(self):
        #if we aren't logging, start
        if not self.logging:
            self.logBtn['text'] = 'Stop logging'
            #open file and write header
            self.logfile = open(self.logFileName.get(),'w')
            self.logfile.write('Version:,' + self.VER_NUMBER + '\n')
            self.logfile.write('state, adc0, mux1, adc1, psi1, theta1, xi1, di1, dj1, sw1, mux2, adc2, psi2, theta2, xi2, di2, dj2, sw2, mux3, adc3, psi3, theta3, xi3, di3, dj3, sw3, Flag, SystemHour, SystemMinute, SystemSecond, SystemuS\n')
            #update flag to start logging in animation loop
            self.logging = True
        #if we are logging, stop
        else:
            #update button and flag
            self.logging = False
            self.logBtn['text'] = 'Log'
            #close file
            self.logfile.close()
            temp = self.logFileName.get()
            #if we were just using the datetime as a log name, just use the new datetime
            if datetime.datetime.now().strftime('%Y_%m_%d') in temp:
                self.logFileName.set(datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S') + '.csv')
            #if our file ends in _x, increment it
            elif temp[len(temp) - 6] is '_':
                self.logFileName.set(temp[:len(temp)-5] + str(int(temp[len(temp)-5])+1) + temp[len(temp)-4:])
            #if our file ends in _xx, increment it
            elif temp[len(temp) - 7] is '_':
                self.logFileName.set(temp[:len(temp)-6] + str(int(temp[(len(temp)-6):(len(temp)-4)])+1) + temp[len(temp)-4:])
            #if using some other format, add a b!
            else:
                self.logFileName.set(temp[:len(temp)-4] + 'b' + temp[len(temp)-4:])

    def logFlagBtnPress(self):
        self.logFlag = True
