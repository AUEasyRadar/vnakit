from tkinter import *
#from tkinter import ttk 
import vnakit
#from vnakit_ex import getSettingsStr
import matplotlib.backends.tkagg as FigureCanvasTkAgg
#from matplotlib.backends.tkagg as FigureCanvasTkAgg
#from matplotlib.figure import Figure 
#import matplotlib.animation as animation
#from matplotlib import style
#style.use('ggplot')
#from random import *
#from ConfigTab import Startup
#from CommandTab import CMD_Tab
#from LivePlot import LivePlot
#from MotorTab import MotorCont
#from DataTab import DataGather
#from PlotTab import DataPlot
#from RadarTab import RadarPlot

#VER_NUMBER = '0.1'
#configurationSettings

def drawPlot(canvas, figure):
    canvasFigure = FigureCanvasAgg(figure, master=canvas)
    canvasFigure.draw()
    canvasFigure.get_tk_widget().grid(column = 0, row = 0)

def checkBounds()
#create root window
root = Tk()
root.title("A.R.F. Interface") 

# Create Title frame and populate
title_frame = Frame(root)
title_frame.pack(side = TOP, fill = X)
logo = PhotoImage(file='radarcs.PNG')
Label(title_frame, image = logo).pack(side = LEFT, pady = 10, padx = 10)
Label(title_frame, text = 'A.R.F.', foreground = "#03244d", font = ('TkDefaultFont', 40)).pack(side = LEFT, fill = X)
portMode = StringVar(title_frame)
portMode.set(11)
portModeDropdown = OptionMenu(title_frame, portMode, 11, 12, 21, 22)
portModeDropdown.config(height = 2, width = 3, font = ('TkDefaultFont', 14))
portModeDropdown.pack(side = RIGHT, pady = 10, padx = 10)
Label(title_frame, text = 'Port Mode:', font = ('TkDefaultFont', 20)).pack(side = RIGHT, pady = 10)

# Create graph frame
graph_frame = Frame(root)
graph_frame.pack(side = TOP)#.grid(column = 0, columnspan = 1, row = 1)
dataPlot = Canvas(graph_frame, width = 896, height = 509, bg = "black")
dataPlot.pack(side = LEFT, padx = 10, pady = 10)#grid(column = 0, row = 0, sticky = (W,N), padx = 10, pady = 10)

# Create Settings frame
settings_frame = Frame(graph_frame)
settings_frame.pack(side = RIGHT, padx = 20, pady = 11, anchor = N)#grid(column = 1, row = 0, sticky = N, padx = 20, pady = 11)
Label(settings_frame, text = 'X - Axis Limits ').grid(row = 0, column = 0, pady = 7)
Entry(settings_frame, width = 5).grid(row = 0, column = 1, pady = 7)
Label(settings_frame, text = 'Mhz  to ').grid(row = 0, column = 2, pady = 7)
Entry(settings_frame, width = 5).grid(row = 0, column = 3, pady = 7)
Label(settings_frame, text = 'Mhz').grid(row = 0, column = 4, pady = 7)
Label(settings_frame, text = 'Number of Frequency points ').grid(row = 1, column = 0, \
    columnspan = 3, pady = 7, sticky = W)
Entry(settings_frame, width = 5).grid(row = 1, column = 3, pady = 7)
Label(settings_frame, text='Resolution Bandwidth ').grid(row = 2, column = 0, columnspan = 3, \
    pady = 7, sticky = W)
Entry(settings_frame, width = 5).grid(row = 2, column = 2, pady = 7)
Label(settings_frame, text = 'khz').grid(row = 2, column = 3, pady = 7, sticky = W)
Label(settings_frame, text='Output Power ').grid(row = 3, column = 0, pady = 7, sticky = W)
Entry(settings_frame, width = 5).grid(row = 3, column = 1, pady = 7)
Label(settings_frame, text = 'dbm').grid(row = 3, column = 2, pady = 7, sticky = W)
Label(settings_frame, text = 'tx_num').grid(row = 4, column = 0, pady = 7, sticky = W)
Label(settings_frame, text = 'Recording Mode ').grid(row = 5, column = 0, pady = 7, sticky = W)
recordingMode = IntVar()
Radiobutton(settings_frame, text = '1 Port Mode', variable = recordingMode, \
    value = vnakit.VNAKIT_MODE_ONE_PORT).grid(row = 6, column = 0, columnspan = 2, sticky = W)
Radiobutton(settings_frame, text = '2 Port Mode', variable = recordingMode, \
    value = vnakit.VNAKIT_MODE_TWO_PORTS).grid(row = 6, column = 1, columnspan = 2)

# Add buttons to the bottom of the GUI
button_frame = Frame(root)
button_frame.pack(side = BOTTOM)#.grid(column = 0, row = 2, padx = 10, pady = 10, sticky = W)
Button(button_frame, text = 'Program').grid(row = '0', column = '0')
Button(button_frame, text = 'Begin Run').grid(row = '0', column = '1')

#label1.grid(row = 0, column = 0, sticky = N)

root.mainloop()