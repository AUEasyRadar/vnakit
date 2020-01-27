from tkinter import *
from tkinter import ttk 
import vnakit
from vnakit_ex import getSettingsStr
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
from random import *
#from ConfigTab import Startup
from CommandTab import CMD_Tab
from LivePlot import LivePlot
from MotorTab import MotorCont
from DataTab import DataGather
from PlotTab import DataPlot
from RadarTab import RadarPlot

VER_NUMBER = '0.1'
#configurationSettings

def Startup(parent, number, msg = '???'):

    
    def configureButtonPress():

        print('Button Was Pressed')
        print(parent.freqEntry.get(),'MHz')
        print(parent.powerEntry.get(),'dBm')
        
        # Define Settings for the Board
        rx_num = 4 #Reciever Port to be read from
        tx_num = 3 #Transmitter Port {VNAKit.RecordingSettings.txTr}
        LF = int(parent.freqEntry.get()) #Start Freq. (MHz) {VNAKit.RecordingSettings.freqRange.freqStartMHz}
        UF = int(parent.freqEntry.get()) #Stop Freq. (MHz) {VNAKit.RecordingSettings.freqRange.freqStopMHz}
        PTS = 1000 #Num Freq. Pts (MHz) {VNAKit.RecordingSettings.freqRange.numFreqPoints}
        RBW = 10 #Resolution BW (KHz) {VNAKit.RecordingSettings.rbw_khz}
        PWR = int(parent.powerEntry.get()) #Tx Power setting (dBm) {VNAKit.RecordingSettings.outputPower_dbm)
        #VNA Kit Mode {VNAKit.RecordingSettings.mode}
        #MODE = self.mode_sel[v.get()]

        # Create RecordingSettings Object and apply settings to the board
        settings = vnakit.RecordingSettings(vnakit.FrequencyRange(LF,UF,PTS),RBW,PWR,tx_num, vnakit.VNAKIT_MODE_ONE_PORT)
        #vnakit.ApplySettings(settings)

        print('The board is initialized with settings:\n')
        print(getSettingsStr(settings))
        parent.configured = 'Configured'
        parent.configMsg['text'] = parent.configured
        parent.configMsg['foreground'] = 'green'

    def freqStringValidate():
        freq = int(float(parent.freqEntry.get()))
        if freq > 6000:
            freq = 6000
            parent.configured = 'not configured'
            parent.configMsg['text'] = parent.configured
            parent.configMsg['foreground'] = 'red'
        elif freq < 100:
            freq = 100
            parent.configured = 'not configured'
            parent.configMsg['text'] = parent.configured
            parent.configMsg['foreground'] = 'red'
        parent.freqEntry.delete(0,'end')
        parent.freqEntry.insert(0,str(freq))
        return 1
    def powerLevelChange(newVal):
        parent.configured = 'not configured'
        parent.configMsg['text'] = configured
        parent.configMsg['foreground'] = 'red'
        power = int(parent.powerEntry.get()) 

    #parent.number = number
    #parent.parent = parent
    freq = 700#parent.LF
    power = -26#parent.PWR
    #parent.
    configured = 'Not Configured'
    #
    ttk.Label(parent, text = 'Startup :').grid(column = 0, row = (2*(number-1)), sticky = (N,S,E))
    ttk.Label(parent, text = msg).grid(column = 1, row = (2*(number-1)), columnspan = 6, sticky = (N,S,W))
    ttk.Label(parent, text = 'MHz',).grid(column = 1, row = 1 + 2*(number-1), sticky = W)
    ttk.Label(parent, text = 'dBm').grid(column = 3, row = 1 + 2*(number-1), sticky = W)
    #Configured Label
    parent.configMsg = ttk.Label(parent, text = configured, foreground = 'red', anchor = E)
    parent.configMsg.grid(column = 4, row = 1 + 2*(number-1), sticky=(E,W))
    #Configure Button
    parent.configBtn = ttk.Button(parent, text='Setup', command = configureButtonPress)
    parent.configBtn.grid(column = 5, row = 1 + 2*(number-1))
    # Enter Frequency
    parent.freqEntry = ttk.Entry(parent, width = 6, validate = 'focusout', validatecommand = freqStringValidate)
    parent.freqEntry.insert(0,str(freq))
    parent.freqEntry.grid(column = 0, row = 1 + 2*(number-1), sticky = (W))
    # Enter Power
    parent.powerEntry = Scale(parent, from_=-26, to=0, orient=HORIZONTAL, command = powerLevelChange)
    parent.powerEntry.set(power)
    #parent.powerEntry.delete(0,'end')
    #parent.powerEntry.insert(0,'0')
    parent.powerEntry.grid(column = 2, row = 1 + 2*(number-1), sticky = E)
    # Radio Widgit
    #v = tk.IntVar()
    #v.set(1)
    #parent.modeButton1 = ttk.Radiobutton(parent, text = "Single Port Mode", variable = v, value = 1)
    #parent.modeButton1.grid(column = 0, row = 2)
    #parent.modeButton2 = ttk.Radiobutton(parent, text = "Dual Port Mode", variable = v, value = 2)
    #parent.modeButton2.grid(column = 0, row = 3)
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

def connectButton():
    print("Connect Button Pressed")
    #vnakit.Init()
    connected = "Connected"
    root.connectBtn.configure(text = connected, bg = 'green')
    # Add error trapping if vnakit.Init() fails
#create root window
root = Tk()
root.title("A.R.F. Interface") 

# Create Title frame and populate
title_frame = ttk.Frame(root)
title_frame['padding'] = (10, 10)
title_frame.columnconfigure(2, weight=1)

logo = PhotoImage(file='radarcs.PNG')
ttk.Label(title_frame, image = logo, anchor = 'e').grid(column=2, row=0, sticky = (N, S, E, W))

#title
ttk.Label(title_frame, text = 'A.R.F.', foreground = "#03244d", anchor = 'sw', font = ('TkDefaultFont', 40)).grid(column=0, row=0, sticky=(N, S, E, W), pady = 10)
ttk.Label(title_frame, text = 'v' + VER_NUMBER, foreground = '#dd550c', anchor = 'sw', font = ('TkDefaultFont', 10)).grid(column=1, row=0, sticky = (N, S, E, W), pady = 20)

#create button for connecting
connected = "Not Connected"
root.connectBtn = Button(root, text = connected, bg = 'red', command = connectButton)
root.connectBtn.grid(column=0, row=5, sticky = (N,E))

#create notebook for middle section
notebook_frame = ttk.Frame(root)
notebook_frame['padding'] = (10,5)
notebook_frame.rowconfigure(0, weight = 1)
notebook_frame.columnconfigure(0, weight = 1)
notebook = ttk.Notebook(notebook_frame)
notebook.grid(row=0,column=0,sticky=(N,S,E,W))

#frames for notebook tabs
Config_frame = ttk.Frame(root, padding = (10,5))
CMD_frame = ttk.Frame(notebook)
ManualPlt_frame = ttk.Frame(notebook)
Data_frame = ttk.Frame(notebook)
Radar_frame = ttk.Frame(notebook)
notebook.add(Config_frame, text = 'Setup')
notebook.add(CMD_frame, text = 'Motor Commands')
notebook.add(ManualPlt_frame, text = 'Manual Plot')
notebook.add(Data_frame, text = 'Manual Data Gather')
notebook.add(Radar_frame, text = 'Radar Plots')

#Startup Tab
#STRT = 
Startup(Config_frame, 1, 'Setup')
#Motor Tab
MOTOR = MotorCont(CMD_frame, 1, 'Motor Command')
#Plot Tab
DATAPLT = DataPlot(ManualPlt_frame, 1, 'Manual Plot')
#Data Gather Tab
DATAGAT = DataGather(Data_frame, 1, 'Manual Data')
#Radar Tab
RADPLT = RadarPlot(Radar_frame, 1, 'Radar Data')
#create frames for ADC graphing and csv logging
Plot_frame = ttk.Frame(root, padding = (10,5))
Plot_frame.rowconfigure(0, weight = 1)
Plot_frame.columnconfigure(0, weight = 1)
LOG_frame = ttk.Frame(root, padding = (10,5))
LOG_frame.rowconfigure(0, weight = 1)
LOG_frame.columnconfigure(0, weight = 1)
pkt_frame = ttk.Frame(root, padding = (10,5))
LivePlots = LivePlot(Plot_frame, LOG_frame, VER_NUMBER)

#place frames
title_frame.grid(column=0, row=0, sticky = (N,S,E,W))
notebook_frame.grid(column=0, row=1, sticky = (N, S, E, W))
LOG_frame.grid(column=0, row=2, sticky = (N,S,E,W))
pkt_frame.grid(column=0, row=3, sticky = (N,S,E,W))
Plot_frame.grid(column=1, row=0, rowspan = 4, sticky = (N,S,E,W))
root.columnconfigure(0,weight = 0)
root.rowconfigure(0,weight = 0)
root.rowconfigure(1, weight = 0)
root.rowconfigure(2, weight = 0)
root.rowconfigure(3, weight = 1)

root.mainloop()


   