from tkinter import *
from tkinter import ttk
import os
import vnakit
from vnakit_ex import getSettingsStr
import tkinter as tk
class MotorCont: 

	def __init__(self, parent, number, msg = '???'):
		self.number = number
		self.parent = parent
		#
		ttk.Label(parent, text='Motor Control:').grid(column = 0, row = (2*(number-1)), sticky = (N,S,E))
		self.xSlider = Scale(parent, from_=0, to=10,orient=VERTICAL)
		self.xSlider.grid(column = 4, row = 1)

		self.ySlider = Scale(parent, from_=0, to=10,orient=HORIZONTAL)
		self.ySlider.grid(column = 5, row = 1)

		self.zSlider = Scale(parent, from_=0, to=10,orient=HORIZONTAL)
		self.zSlider.grid(column = 6, row = 1)