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
		self.f = Figure(figsize = (2,2), dpi = 100, tight_layout = 'true')
		self.f.add_axes()
		self.canvas = FigureCanvasTkAgg(self.f, parent)
		self.grid(column=0, row=1, sticky =(N,S,E,W), columnspan=2)

	    #call to grid function for GUI placement
	def grid(self, **keyword_params):
		self.canvas.get_tk_widget().grid(keyword_params)