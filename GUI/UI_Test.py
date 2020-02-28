from tkinter import *
from tkinter import ttk 
import vnakit
#from vnakit_ex import getSettingsStr
#import matplotlib.backends.tkagg as FigureCanvasTkAgg
#from matplotlib.backends.tkagg as FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import figure
from matplotlib import axes
from matplotlib.animation import FuncAnimation

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

def checkLowerFrequencyBound():
    """Validates the input string of the lower X limit box"""
    lowerX = lowerXLimit.get()
    upperX = upperXLimit.get()
    if lowerX != '':
        lowerX = int(float(lowerXLimit.get()))
        if upperX != '':
            upperX = int(float(upperXLimit.get()))
            if lowerX > upperX:
                lowerX = upperX
        if lowerX < 100:
            lowerX = 100
    elif upperX != '':
        upperX = int(float(upperXLimit.get()))
        if upperX < 1000:
            lowerX = upperX
        else:
            lowerX = 1000
    lowerXLimit.delete(0, 'end')
    lowerXLimit.insert(0,lowerX)
    return 1

def checkUpperFrequencyBound():
    """Validates the input string of the upper X limit box"""
    lowerX = lowerXLimit.get()
    upperX = upperXLimit.get()
    if upperX != '':
        upperX = int(float(upperXLimit.get()))
        if upperX > 6000:
            upperX = 6000
        elif lowerX != '':
            lowerX = int(float(lowerXLimit.get()))
            if lowerX > upperX:
                upperX = lowerX
    else:
        upperX = 6000
    upperXLimit.delete(0, 'end')
    upperXLimit.insert(0,upperX)
    return 1

def checkResolutionBandwidth():
    """Validates the input divides evenly into the x-limits"""
    rbw = resolutionBandwidth.get()
    if rbw != '':
        rbw = int(float(rbw))
        lowerX = lowerXLimit.get()
        if lowerX != '':
            lowerX = int(float(lowerX))
            upperX = upperXLimit.get()
            if upperX != '':
                upperX = int(float(upperX))
                maxRbw = int((upperX - lowerX) / 2)
                if rbw > maxRbw:
                    rbw = maxRbw
        if rbw < 1:
            rbw = 1
    else:
        rbw = 500
    resolutionBandwidth.delete(0, 'end')
    resolutionBandwidth.insert(0, str(rbw))

    
def checkOutputPwrBounds():
    """Validates the output power is within the valide range -26 to 0"""
    currentValue = outputPwr.get()
    if currentValue != '':
        currentValue = int(float(currentValue))
        if currentValue < -26:
            currentValue = -26.0
        elif currentValue > 0:
            currentValue = 0.0
    else:
            currentValue = -3
    outputPwr.delete(0, 'end')
    outputPwr.insert(0,str(currentValue))
    
    return 1

def checkFrequencyPoints():
    currentValue = numberOfFrequencyPoints.get()
    if currentValue != '':
        currentValue = int(float(currentValue))
        if currentValue < 2:
            currentValue = 2
        elif currentValue > 1000:
            currentValue = 1000
        numberOfFrequencyPoints.delete(0, 'end')
        numberOfFrequencyPoints.insert(0, currentValue)
    else:
        numberOfFrequencyPoints.delete(0, 'end')
        numberOfFrequencyPoints.insert(0, 500)
    return 1

def initializeSemilogY():
    """The function used to initialize the semilogY animation."""
    semilogYData.set_data([], [])
    return semilogYData,
def animateSemilogY(i):
    """The function used by FuncAnimation to plot the animation."""
    i = i % 60
    xVals = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000]
    y = [-90, -80, -70, -60, -50, -40, -30, -20, -10, -5, 0, 3, 6, 9]
    for iterate in range(0, len(xVals)):
        xVals[iterate] = xVals[iterate] + i * 100
    semilogYData.set_data(xVals, y)
    return semilogYData,

def programVNA():
    semilogYAxes.clear()
    newYVals = [-90, -80, -70, -60, -50, -40, -30, -20, -10, -5, 0, 0,0,0]
    xVals = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000]
    semilogYFigure.axes[0].plot(xVals, newYVals, 'bx')
    semilogYPlotCanvas.draw()
    #canvas = FigureCanvasTkAgg(semilogYFigure, master = semilogY_frame)
    #canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

#create root window
root = Tk()
root.title("A.R.F. Interface") 

# Create Title frame and populate
title_frame = Frame(root)
title_frame.pack(side = TOP, fill = X)
logo = PhotoImage(file='radarcs.PNG')
Label(title_frame, image = logo).pack(side = LEFT, pady = 10, padx = 10)
Label(title_frame, text = 'A.R.F.', foreground = "#03244d", \
    font = ('TkDefaultFont', 40)).pack(side = LEFT, fill = X)
portMode = StringVar(title_frame)
portMode.set('Gamma')
portModeDropdown = OptionMenu(title_frame, portMode, 'Tau', 'Gamma', 'S11', \
     'S21', 'IL', 'RL', 'VSWR')
portModeDropdown.config(height = 2, width = 6, font = ('TkDefaultFont', 14))
portModeDropdown.pack(side = RIGHT, pady = 10, padx = 10)
Label(title_frame, text = 'Port Mode:', font = \
    ('TkDefaultFont', 20)).pack(side = RIGHT, pady = 10)

#Create notebook
notebook = ttk.Notebook(root)
ttk.Style().configure('TNotebook.Tab', background = '#F0F0F0')


# Create semilogY frame
semilogY_frame = Frame(notebook, bg = '#F0F0F0', pady = 10, padx = 10)
semilogY_frame.pack(side = TOP, fill = BOTH, expand = True)
semilogYFigure = figure.Figure(figsize=(4,2), dpi=100, facecolor="#F0F0F0")
semilogYAxes = axes.Axes(semilogYFigure, [0.1, 0.1, 0.8, 0.85], frameon = True, \
    adjustable = 'box', in_layout = True, xscale = 'linear', autoscalex_on = True, \
        xlabel = 'frequency', xlim = (1000, 6000), yscale = 'symlog', ylim = (-90, 100))
semilogYAxes.grid(which = 'both')
semilogYFigure.add_axes(semilogYAxes)
semilogYPlotCanvas = FigureCanvasTkAgg(semilogYFigure, master = semilogY_frame)
semilogYPlotCanvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)
semilogYData, = semilogYFigure.axes[0].plot([], [], 'rx')

semilogYAnimation = FuncAnimation(semilogYFigure, animateSemilogY, \
    init_func=initializeSemilogY, frames = 600, interval = 200, blit = True)



# Create Settings frame
settings_frame = Frame(semilogY_frame)
settings_frame.pack(side = RIGHT, padx = 20, pady = 11, anchor = N)
Label(settings_frame, text = 'X - Axis Limits ').grid(row = 0, column = 0, pady = 7)
lowerXLimit = Entry(settings_frame, width = 5, validate = 'focusout', \
    validatecommand = checkLowerFrequencyBound)
lowerXLimit.insert(0, 1000)
lowerXLimit.grid(row = 0, column = 1, pady = 7)
Label(settings_frame, text = 'Mhz  to ').grid(row = 0, column = 2, pady = 7)
upperXLimit = Entry(settings_frame, width = 5, validate = 'focusout', \
    validatecommand = checkUpperFrequencyBound)
upperXLimit.insert(0, 6000)
upperXLimit.grid(row = 0, column = 3, pady = 7)
Label(settings_frame, text = 'Mhz').grid(row = 0, column = 4, pady = 7)
Label(settings_frame, text = 'Number of Frequency points ').grid(row = 1, column = 0, \
    columnspan = 3, pady = 7, sticky = W)
numberOfFrequencyPoints = Entry(settings_frame, width = 5, \
    validate = 'focusout', validatecommand = checkFrequencyPoints)
numberOfFrequencyPoints.insert(0, 500)
numberOfFrequencyPoints.grid(row = 1, column = 3, pady = 7)
Label(settings_frame, text = 'Resolution Bandwidth ').grid(row = 2, column = 0, \
    columnspan = 3, pady = 7, sticky = W)
resolutionBandwidth = Entry(settings_frame, width = 16, \
    validate = 'focusout', validatecommand = checkResolutionBandwidth)
resolutionBandwidth.insert(0, 100)
resolutionBandwidth.xview_scroll(2, UNITS)
resolutionBandwidth.grid(row = 2, column = 1, columnspan = 3, pady = 7, sticky = E)
Label(settings_frame, text = 'khz').grid(row = 2, column = 4, pady = 7)
Label(settings_frame, text='Output Power ').grid(row = 3, column = 0, \
    pady = 7, sticky = W)
outputPwr = Entry(settings_frame, width = 5, \
    validate = 'focusout', validatecommand = checkOutputPwrBounds)
outputPwr.insert(0, -3)
outputPwr.grid(row = 3, column = 1, pady = 7)
Label(settings_frame, text = 'dbm').grid(row = 3, column = 2, pady = 7, sticky = W)
#Label(settings_frame, text = 'Transmit Port').grid(row = 4, column = 0, pady = 7, sticky = W)
#txMode = StringVar(settings_frame)
#txMode.set(4)
#txDropdown = OptionMenu(settings_frame, txMode, 1, 2, 3, 4, 5, 6)
#txDropdown.grid(row = 4, column = 1, pady = 7)
Label(settings_frame, text = 'Recording Mode ').grid(row = 5, column = 0, \
    pady = 7, sticky = W)
recordingMode = IntVar()
Radiobutton(settings_frame, text = '1 Port Mode', variable = recordingMode, \
    value = vnakit.VNAKIT_MODE_ONE_PORT).grid(row = 6, column = 0, \
        columnspan = 2, sticky = W)
Radiobutton(settings_frame, text = '2 Port Mode', variable = recordingMode, \
    value = vnakit.VNAKIT_MODE_TWO_PORTS).grid(row = 6, column = 1, columnspan = 2)
notebook.add(semilogY_frame, text='SemilogY')

#Polar Plot
polar_frame = Frame(notebook, bg = '#F0F0F0', pady = 10, padx = 10)
polar_frame.pack(side = LEFT, fill = BOTH, expand = True)
polarFigure = figure.Figure(figsize=(4,2), dpi=100, facecolor="#F0F0F0")
polarFigure.add_axes([0.1, 0.15, 0.7, 0.7], projection = 'polar')
polarPlotCanvas = FigureCanvasTkAgg(polarFigure, master = polar_frame)
polarPlotCanvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)
notebook.add(polar_frame, text='Polar')
notebook.pack(side = TOP, fill = BOTH, expand = True, padx = 11)



# Add buttons to the bottom of the GUI
button_frame = Frame(root, height = 45, pady = 10)
button_frame.pack(side = BOTTOM, fill = X)
Button(button_frame, text = 'Program', command = programVNA).place(relx = 0.3, y = -5)
Button(button_frame, text = 'Begin Run').place(relx = 0.7, y = -5)



root.mainloop()