from tkinter import *
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
from random import random
from numpy import linspace
from numpy import zeros

class LivePlot:
    titleFontSize = 8   #font size for subplot titles
    axesFontSize = 6
    refreshRate = 10    #number of frames per second
    VER_NUMBER = 0

    def __init__(self, parent, log_parent, ver):
        #store version number
        self.VER_NUMBER = ver
        #####   SParam graphs  #####
        #create figure for graphing
        self.f = Figure(figsize = (4,5), dpi = 100, tight_layout = 'true')
        #SParam subplot initialization
        self.SParamsub = [0,1,2,3]
        self.SParamln = [0,1,2,3]
        self.xdata = [0,1,2,3]
        self.ydata = [0,1,2,3]
        loc = [1,2,3,4]
        for i in [0, 1, 2, 3]:
            self.SParamsub[i] = self.f.add_subplot(4,1,loc[i])
            self.SParamsub[i].set_xlabel('Time (s)',fontsize = self.axesFontSize)
            self.SParamsub[i].set_ylabel('S Param (Mag)',fontsize = self.axesFontSize)
            self.SParamsub[i].set_xticklabels([-5, -4, -3, -2, -1, 0], fontsize = self.axesFontSize)
            self.SParamsub[i].set_yticklabels([0, 1, 2, 3], fontsize = self.axesFontSize)
            self.xdata[i] = linspace(-5, 0, 51)
            self.ydata[i] = zeros(51)
            self.SParamln[i], = self.SParamsub[i].plot(self.xdata[i],self.ydata[i])
                    #create canvas widget with figure embedded in it
        self.SParamsub[0].set_title('S ' + '11',fontsize = self.titleFontSize)
        self.SParamsub[1].set_title('S ' + '12',fontsize = self.titleFontSize)
        self.SParamsub[2].set_title('S ' + '21',fontsize = self.titleFontSize)
        self.SParamsub[3].set_title('S ' + '22',fontsize = self.titleFontSize)
        self.canvas = FigureCanvasTkAgg(self.f, parent)
        self.grid(column=0, row=0, sticky =(N,S,E,W), columnspan=4)
        #configure animation
        self.ani = animation.FuncAnimation(self.f, self.animateFcn, interval = (1000/self.refreshRate), init_func=self.animateInit, blit=True)

    #call to grid function for GUI placement
    def grid(self, **keyword_params):
        self.canvas.get_tk_widget().grid(keyword_params)

    def animateFcn(self,frame_num):

    	self.SParamln = 1

    	return tuple(self.SParamln,)

    #initialization for animation (sets up backgrounds)
    def animateInit(self):
        for i in [0,1,2,3]:
            self.SParamsub[i].set_xlim(-5, 0)
            self.SParamsub[i].set_ylim(0, 4)
        return tuple(self.SParamln,)