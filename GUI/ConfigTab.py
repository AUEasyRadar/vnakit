from tkinter import *
from tkinter import ttk
import os
import vnakit
from vnakit_ex import getSettingsStr
import tkinter as tk
class Startup:
    PWR = -26
    LF = 700
    mode_sel = ["vnakit.VNAKIT_MODE_TWO_PORTS" , "vnakit.VNAKIT_MODE_TWO_PORTS"]

        # General settings and connect button for VNAKit
    def __init__(self, parent, number, msg = '???'):
        self.number = number
        self.parent = parent
        self.freq = self.LF
        self.power = self.PWR
        self.configured = 'Not Configured'
        #
        ttk.Label(parent, text = 'Startup :').grid(column = 0, row = (2*(number-1)), sticky = (N,S,E))
        ttk.Label(parent, text = msg).grid(column = 1, row = (2*(number-1)), columnspan = 6, sticky = (N,S,W))
        ttk.Label(parent, text = 'MHz',).grid(column = 1, row = 1 + 2*(number-1), sticky = W)
        ttk.Label(parent, text = 'dBm').grid(column = 3, row = 1 + 2*(number-1), sticky = W)
        #Configured Label
        self.configMsg = ttk.Label(parent, text = self.configured, foreground = 'red', anchor = E)
        self.configMsg.grid(column = 4, row = 1 + 2*(number-1), sticky=(E,W))
        #Configure Button
        self.configBtn = ttk.Button(parent, text='Setup', command = self.configureButtonPress)
        self.configBtn.grid(column = 5, row = 1 + 2*(number-1))
        # Enter Frequency
        self.freqEntry = ttk.Entry(parent, width = 6, validate = 'focusout', validatecommand = self.freqStringValidate)
        self.freqEntry.insert(0,str(self.freq))
        self.freqEntry.grid(column = 0, row = 1 + 2*(number-1), sticky = (W))
        # Enter Power
        self.powerEntry = Scale(parent, from_=-26, to=0, orient=HORIZONTAL)
        self.powerEntry.set(self.power)
        #self.powerEntry.delete(0,'end')
        #self.powerEntry.insert(0,'0')
        self.powerEntry.grid(column = 2, row = 1 + 2*(number-1), sticky = E)
        # Radio Widgit
        v = tk.IntVar()
        v.set(1)
        self.modeButton1 = ttk.Radiobutton(parent, text = "Single Port Mode", variable = v, value = 1)
        self.modeButton1.grid(column = 0, row = 2)
        self.modeButton2 = ttk.Radiobutton(parent, text = "Dual Port Mode", variable = v, value = 2)
        self.modeButton2.grid(column = 0, row = 3)
        #Configure Row and Column Weight
        parent.rowconfigure(2 * (number-1), weight = 1)
        parent.rowconfigure(1 + 2 * (number-1), weight = 1)
        parent.columnconfigure(0, weight = 0)
        parent.columnconfigure(1, weight = 0)
        parent.columnconfigure(2, weight = 0)
        parent.columnconfigure(3, weight = 0)
        parent.columnconfigure(4, weight = 1)
        parent.columnconfigure(5, weight = 0)
        parent.columnconfigure(6, weight = 0)
   
    def configureButtonPress(self):

        print('Button Was Pressed')
        print(self.freqEntry.get(),'MHz')
        print(self.powerEntry.get(),'dBm')
        
        # Define Settings for the Board
        rx_num = 4 #Reciever Port to be read from
        tx_num = 3 #Transmitter Port {VNAKit.RecordingSettings.txTr}
        LF = int(self.freqEntry.get()) #Start Freq. (MHz) {VNAKit.RecordingSettings.freqRange.freqStartMHz}
        UF = int(self.freqEntry.get()) #Stop Freq. (MHz) {VNAKit.RecordingSettings.freqRange.freqStopMHz}
        PTS = 1000 #Num Freq. Pts (MHz) {VNAKit.RecordingSettings.freqRange.numFreqPoints}
        RBW = 10 #Resolution BW (KHz) {VNAKit.RecordingSettings.rbw_khz}
        PWR = int(self.powerEntry.get()) #Tx Power setting (dBm) {VNAKit.RecordingSettings.outputPower_dbm)
        #VNA Kit Mode {VNAKit.RecordingSettings.mode}
        MODE = self.mode_sel[v.get()]

        # Create RecordingSettings Object and apply settings to the board
        settings = vnakit.RecordingSettings(vnakit.FrequencyRange(LF,UF,PTS),RBW,PWR,tx_num,MODE)
        vnakit.ApplySettings(settings)

        print('The board is initialized with settings:\n')
        print(getSettingsStr(settings))
        self.configured = 'Configured'
        self.configMsg['text'] = self.configured
        self.configMsg['foreground'] = 'green'

    def freqStringValidate(self):
        freq = int(float(self.freqEntry.get()))
        if freq > 6000:
            freq = 6000
        if freq < 100:
            freq = 100
        self.freqEntry.delete(0,'end')
        self.freqEntry.insert(0,str(freq))
        #check if new value was entered
        if freq != self.freq:
            self.configured = 'not configured'
            self.configMsg['text'] = self.configured
            self.configMsg['foreground'] = 'red'
            self.freq = freq
        return 1
    def powerLevelChange(self):
        self.powerLevel = int(self.powerEntry.get())
        if self.powerLevel != self.power:
            self.configured = 'not configured'
            self.configMsg['text'] = self.configured
            self.configMsg['foreground'] = 'red'
            self.power = self.powerLevel     
