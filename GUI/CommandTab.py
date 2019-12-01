from tkinter import *
from tkinter import ttk
import os
import vnakit
from vnakit_ex import getSettingsStr
import tkinter as tk

class CMD_Tab:

	def __init__(self, parent, number, msg = '???'):
		# SELF VARIABLES GO HERE!
		
		# Button
		self.commBtn = ttk.Button(parent, text = 'Send Test', command = self.sendCommand)

	def sendCommand(self):
		
		print('Command Sent.')	