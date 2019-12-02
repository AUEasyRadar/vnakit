from tkinter import *
from tkinter import ttk
import os
import vnakit
from vnakit_ex import getSettingsStr
import tkinter as tk
class DataPlot:    

	def __init__(self, parent, number, msg = '???'):
		self.number = number
		self.parent = parent
		def browseToFile():
			print("Browsing to file")
		def toggleButtonState():
			if actualOrLoad.get() == 0:
				browseButton['state'] = 'disabled'
			
			else:
				browseButton['state'] = 'normal'
			
		#x-axis
		ttk.Label(parent, text='x-Axis:').grid(column = 0, row = (2*(number-1)), sticky = (W), padx = 10, pady = 10)
		xAxisOptions = ["", "S11", "S12", "S21", "S22", "Gain", "VSWR"]
		xAxisOptionsSelect = StringVar(parent)
		xAxisOptionsSelect.set(xAxisOptions[1])
		ttk.OptionMenu(parent, xAxisOptionsSelect, *xAxisOptions).grid(column = 1, row = (2*(number-1)), sticky = (W), pady = 10)
		#y-axis
		ttk.Label(parent, text='y-Axis:').grid(column = 2, row = (2*(number-1)), sticky = (W), padx = 10, pady = 10)
		yAxisOptions = ["Frequency", "Time"]
		yAxisOptionsSelect = StringVar(parent)
		yAxisOptionsSelect.set(yAxisOptions[0])
		ttk.OptionMenu(parent, yAxisOptionsSelect, *yAxisOptions).grid(column = 3, row = (2*(number-1)), sticky = (W), pady = 10)
		#Data type
		ttk.Label(parent, text='Data Type:').grid(column = 0, row = (2*number), sticky = (W), padx = 10, pady = 10)
		dataType = IntVar()
		ttk.Radiobutton(parent, text = "Phase", variable = dataType, value = 0).grid(column = 1, columnspan = 3, row = (2 * number), sticky = W)
		ttk.Radiobutton(parent, text = "Magnitude", variable = dataType, value = 1).grid(column = 1, columnspan = 3, row = (2 * number))
		ttk.Radiobutton(parent, text = "Complex", variable = dataType, value = 2).grid(column = 1, columnspan = 3, row = (2 * number), sticky = E)
		#x-axis range
		ttk.Label(parent, text='x-Axis Range').grid(column = 0, row = (2*(number + 1)), sticky = (W), padx = 10, pady = 10)
		xAxisLeft = Entry(parent, width = "17")
		xAxisRight = Entry(parent, width = "17")
		xAxisLeft.grid(column = 1, row = (2*(number + 1)))
		ttk.Label(parent, text='to').grid(column = 2, row = (2* (number + 1)), padx = 10, pady = 10)
		xAxisRight.grid(column = 3, row = (2*(number + 1)))
		#y-axis range
		ttk.Label(parent, text='y-Axis Range').grid(column = 0, row = (2*(number + 2)), sticky = (W), padx = 10, pady = 10)
		yAxisLeft = Entry(parent, width = "17")
		yAxisRight = Entry(parent, width = "17")
		yAxisLeft.grid(column = 1, row = (2*(number + 2)))
		ttk.Label(parent, text='to').grid(column = 2, row = (2*(number + 2)), padx = 10, pady = 10)
		yAxisRight.grid(column = 3, row = (2*(number + 2)))
		#chart type
		ttk.Label(parent, text='Plot Type').grid(column = 0, row = (2*(number + 3)), sticky = (W), padx = 10, pady = 10)
		smithChart = IntVar()
		Checkbutton(parent, text="Smith", variable = smithChart).grid(column = 1, row = (2*(number + 4)), sticky = (W))
		polarChart = IntVar()
		Checkbutton(parent, text="Polar", variable = polarChart).grid(column = 1, row = (2*(number + 5)), sticky = (W))
		linearChart = IntVar()
		Checkbutton(parent, text="Linear", variable = linearChart).grid(column = 1, row = (2*(number + 6)), sticky = (W))
		logscaleChart = IntVar()
		Checkbutton(parent, text="Logscale", variable = logscaleChart).grid(column = 1, row = (2*(number + 7)), sticky = (W))
		#real time or Load File
		actualOrLoad = IntVar()
		ttk.Radiobutton(parent, text = "Real Tme", variable = actualOrLoad, value = 0, command = toggleButtonState).grid(column = 0, columnspan = 1, row = (2 * (number + 8)), sticky = W, padx = 10, pady = 10)
		ttk.Radiobutton(parent, text = "Use File", variable = actualOrLoad, value = 1, command = toggleButtonState).grid(column = 1, columnspan = 1, row = (2 * (number + 8)), sticky = E, padx = 4, pady = 10)
		browseButton = ttk.Button(parent, text = "Browse", command = browseToFile, state = 'disabled')
		browseButton.grid(column = 2, row = (2 * (number + 8)), sticky = W, pady = 10)
		#Samples
		ttk.Label(parent, text = "Number of samples per frequency").grid(column = 0, columnspan = 2, row = (2 * (number + 9)), sticky = W, pady = 10, padx = 10)
		samples = Entry(parent)
		samples.grid(column = 2, columnspan = 2, row = (2 * (number + 9)), sticky = W)
		#sample type
		sampleType = IntVar()
		ttk.Radiobutton(parent, text = "Average", variable = sampleType, value = 0).grid(column = 1, columnspan = 1, row = (2 * (number + 10)), sticky = W)
		ttk.Radiobutton(parent, text = "Min Hold", variable = sampleType, value = 1).grid(column = 1, columnspan = 1, row = (2 * (number + 11)), sticky = W)
		ttk.Radiobutton(parent, text = "Max Hold", variable = sampleType, value = 2).grid(column = 1, columnspan = 1, row = (2 * (number + 12)), sticky = W)
		#Measure Duration
		ttk.Label(parent, text = "Measure Duration").grid(column = 0, row = (2 * (number + 13)), sticky = W, pady = 10, padx = 10)
		measureTime = Entry(parent, width = "15")
		measureTime.grid(column = 1, row = (2*(number + 13)))
		timeOptions = ["", "s", "ms", "μs", "ns"]
		timeOptionsSelect = StringVar(parent)
		timeOptionsSelect.set(timeOptions[1])
		ttk.OptionMenu(parent, timeOptionsSelect, *timeOptions).grid(column = 2, row = (2*(number + 13)), sticky = (W), pady = 10)