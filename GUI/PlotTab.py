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
		ttk.Label(parent, text='Custom Plots:').grid(column = 0, row = (2*(number-1)), sticky = (N,S,E))