from tkinter import *
from tkinter import ttk
import os
import vnakit
from vnakit_ex import getSettingsStr
import tkinter as tk
class DataGather:

	

	def __init__(self, parent, number, msg = '???'):
		self.number = number
		self.parent = parent
		def browseToFolder():
			print("Browsing to folder")
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
		#Data store options
		ttk.Label(parent, text='Data form:').grid(column = 0, row = (2*number), sticky = (W), padx = 10, pady = 10)
		dataStoreType = IntVar()
		ttk.Radiobutton(parent, text = "Polar", variable = dataStoreType, value = 0).grid(column = 1, columnspan = 3, row = (2 * number), sticky = W)
		ttk.Radiobutton(parent, text = "Rectangular", variable = dataStoreType, value = 1).grid(column = 1, columnspan = 3, row = (2 * number), sticky = E)
		#Delimiter selection
		ttk.Label(parent, text='Delimiter').grid(column = 0, row = (2*(number + 1)), sticky = (W), padx = 10, pady = 10)
		dataDelimiter = Entry(parent, width = "10")
		dataDelimiter.grid(column = 1, row = (2*(number + 1)))
		#Frequency Sweep
		ttk.Label(parent, text = "Number of samples per frequency").grid(column = 0, columnspan = 2, row = (2 * (number + 2)), sticky = W, pady = 10, padx = 10)
		samples = Entry(parent, width = 10)
		samples.grid(column = 2, columnspan = 2, row = (2 * (number + 2)), sticky = W)
		sampleGatherType = IntVar()
		ttk.Radiobutton(parent, text = "Average", variable = sampleGatherType, value = 0).grid(column = 1, columnspan = 1, row = (2 * (number + 3)), sticky = W)
		ttk.Radiobutton(parent, text = "Min Hold", variable = sampleGatherType, value = 1).grid(column = 1, columnspan = 1, row = (2 * (number + 4)), sticky = W)
		ttk.Radiobutton(parent, text = "Max Hold", variable = sampleGatherType, value = 2).grid(column = 1, columnspan = 1, row = (2 * (number + 5)), sticky = W)
		#Measure Duration
		ttk.Label(parent, text = "Measure Duration").grid(column = 0, row = (2 * (number + 6)), sticky = W, pady = 10, padx = 10)
		measureTime = Entry(parent, width = "15")
		measureTime.grid(column = 1, row = (2*(number + 6)))
		timeOptions = ["", "s", "ms", "μs", "ns"]
		timeOptionsSelect = StringVar(parent)
		timeOptionsSelect.set(timeOptions[1])
		ttk.OptionMenu(parent, timeOptionsSelect, *timeOptions).grid(column = 2, row = (2*(number + 6)), sticky = (W), pady = 10)
		#File name
		ttk.Label(parent, text = "File Name").grid(column = 0, row = (2 * (number + 7)), sticky = W, pady = 10, padx = 10)
		measureTime = Entry(parent, width = "30")
		measureTime.grid(column = 1, columnspan = 2, row = (2*(number + 7)))
		#Save location
		ttk.Label(parent, text = "Save Location").grid(column = 0, row = (2 * (number + 8)), sticky = W, pady = 10, padx = 10)
		measureTime = Entry(parent, width = "30")
		measureTime.grid(column = 1, columnspan = 2, row = (2*(number + 8)))
		saveLocationButton = ttk.Button(parent, text = "Browse", command = browseToFolder)
		saveLocationButton.grid(column = 3, row = (2 * (number + 8)), sticky = W, pady = 10, padx = 5)
		'''#x-axis range
		ttk.Label(parent, text='x-Axis Range').grid(column = 0, row = (2*number), sticky = (W), padx = 10, pady = 10)
		xAxisLeft = Entry(parent, width = "17")
		xAxisRight = Entry(parent, width = "17")
		xAxisLeft.grid(column = 1, row = (2*number))
		ttk.Label(parent, text='to').grid(column = 2, row = (2*number), padx = 10, pady = 10)
		xAxisRight.grid(column = 3, row = (2*number))
		#y-axis range
		ttk.Label(parent, text='y-Axis Range').grid(column = 0, row = (2*(number + 1)), sticky = (W), padx = 10, pady = 10)
		yAxisLeft = Entry(parent, width = "17")
		yAxisRight = Entry(parent, width = "17")
		yAxisLeft.grid(column = 1, row = (2*(number + 1)))
		ttk.Label(parent, text='to').grid(column = 2, row = (2*(number + 1)), padx = 10, pady = 10)
		yAxisRight.grid(column = 3, row = (2*(number + 1)))
		#chart type
		ttk.Label(parent, text='Plot Type').grid(column = 0, row = (2*(number + 2)), sticky = (W), padx = 10, pady = 10)
		smithChart = IntVar()
		Checkbutton(parent, text="Smith", variable = smithChart).grid(column = 1, row = (2*(number + 3)), sticky = (W))
		polarChart = IntVar()
		Checkbutton(parent, text="Polar", variable = polarChart).grid(column = 1, row = (2*(number + 4)), sticky = (W))
		linearChart = IntVar()
		Checkbutton(parent, text="Linear", variable = linearChart).grid(column = 1, row = (2*(number + 5)), sticky = (W))
		logscaleChart = IntVar()
		Checkbutton(parent, text="Logscale", variable = logscaleChart).grid(column = 1, row = (2*(number + 6)), sticky = (W))
		#real time or Load File
		actualOrLoad = IntVar()
		ttk.Radiobutton(parent, text = "Real Tme", variable = actualOrLoad, value = 0, command = toggleButtonState).grid(column = 0, columnspan = 1, row = (2 * (number + 7)), sticky = W, padx = 10, pady = 10)
		ttk.Radiobutton(parent, text = "Use File", variable = actualOrLoad, value = 1, command = toggleButtonState).grid(column = 1, columnspan = 1, row = (2 * (number + 7)), sticky = E, padx = 4, pady = 10)
		browseButton = ttk.Button(parent, text = "Browse", command = browseToFile, state = 'disabled')
		browseButton.grid(column = 2, row = (2 * (number + 7)), sticky = W, pady = 10)
		#Samples
		ttk.Label(parent, text = "Number of samples per frequency").grid(column = 0, columnspan = 2, row = (2 * (number + 8)), sticky = W, pady = 10, padx = 10)
		samples = Entry(parent)
		samples.grid(column = 2, columnspan = 2, row = (2 * (number + 8)), sticky = W)
		#sample type
		sampleType = IntVar()
		ttk.Radiobutton(parent, text = "Average", variable = sampleType, value = 0).grid(column = 1, columnspan = 1, row = (2 * (number + 9)), sticky = W)
		ttk.Radiobutton(parent, text = "Min Hold", variable = sampleType, value = 1).grid(column = 1, columnspan = 1, row = (2 * (number + 10)), sticky = W)
		ttk.Radiobutton(parent, text = "Max Hold", variable = sampleType, value = 2).grid(column = 1, columnspan = 1, row = (2 * (number + 11)), sticky = W)
		#Measure Duration
		ttk.Label(parent, text = "Measure Duration").grid(column = 0, row = (2 * (number + 12)), sticky = W, pady = 10, padx = 10)
		measureTime = Entry(parent, width = "15")
		measureTime.grid(column = 1, row = (2*(number + 12)))
		timeOptions = ["", "s", "ms", "μs", "ns"]
		timeOptionsSelect = StringVar(parent)
		timeOptionsSelect.set(timeOptions[1])
		ttk.OptionMenu(parent, timeOptionsSelect, *timeOptions).grid(column = 2, row = (2*(number + 12)), sticky = (W), pady = 10)
		'''