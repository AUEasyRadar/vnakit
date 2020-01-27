from tkinter import *
from tkinter import ttk
#for plotting
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
style.use('ggplot')
#for numbers
from random import random
from numpy import linspace
from numpy import zeros
import os
import vnakit
from vnakit_ex import getSettingsStr
import tkinter as tk

class RadarPlot:

	def __init__(self, parent, number, msg = '???'):
		self.number = number
		self.parent = parent
		ttk.Label(parent, text='Radar Plot:').grid(column = 0, row = (2*(number-1)), sticky = (N,S,E))
		self.f = Figure(figsize = (4,4), dpi = 100, tight_layout = 'true')
		self.f.add_axes([0.1, 0.1, 0.8, 0.8],projection='polar')
		self.canvas = FigureCanvasTkAgg(self.f, parent)
		self.canvas.get_tk_widget().grid(column=0, row=1, sticky =(N,S,E,W), columnspan=2, rowspan = 2)
		ttk.Label(parent, text='Radar Angle').grid(column = 5, row = 0, columnspan = 7, sticky = N)
		ttk.Label(parent, text=' Radar Distance').grid(column = 5, row = 2, columnspan = 7, sticky = N)
	    #call to grid function for GUI placement
		
		self.angleBox = ttk.Entry(parent,validate = 'focusout', validatecommand = self.updateAngle)
		self.angleBox.grid(column = 6, row = 1, columnspan = 6)
		
		self.rangeBox = ttk.Entry(parent,validate = 'focusout', validatecommand = self.updateRange)
		self.rangeBox.grid(column = 6, row = 2, columnspan = 6)

		self.dataGather = ttk.Button(parent, text = 'Begin Radar', command = self.startRadar)
		self.dataGather.grid(column = 0, row = 3, columnspan = 6, sticky = (W), padx = 10, pady = 10)

		self.dataStop = ttk.Button(parent, text = 'Stop Radar', command = self.startRadar)
		self.dataStop.grid(column = 0, row = 3, columnspan = 6, sticky = (E), padx = 10, pady = 10)

	def startRadar(self):

		print('Radar has started')
		print('S plots have stopped')

	def updateAngle(self):

		self.angleBox.insert(0,32)

	def updateRange(self):

		self.rangeBox.insert(0,2)