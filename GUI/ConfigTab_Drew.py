from tkinter import *
from tkinter import ttk



class Startup:
    #dictionary definitions for message construction
    dict_power = {  -9 : 0x00,
                    -6 : 0x01,
                    -3 : 0x02,
                    0 : 0x03,
                }
    dict_startFreq = {  1 : 5810,
                        2 : 5900,
                        3 : 909
                    }

    def __init__(self, parent, number, msg = '???'):
        self.number = number                            #PLL.number is identifier
        self.parent = parent                            #parent frame
        self.freq = self.dict_startFreq[self.number]    #frequency (integer multiple of 1 MHz)
        self.power = 0                                  #power level (in dBm)
        self.configured = 'not configured'              #indicates whether or not it is configured
        #set up U.I. based on number:
        #labels
        # ttk.Label(parent, text = 'PLL ' + str(number) + ': ' + msg).grid(column = 0, row = (2*(number-1)), sticky = (W), columnspan =7)
        ttk.Label(parent, text = 'PLL ' + str(number) + ':').grid(column = 0, row = (2*(number-1)), sticky = (N,S,E))
        ttk.Label(parent, text = msg).grid(column = 1, row = (2*(number-1)), columnspan = 6, sticky = (N,S,W))
        ttk.Label(parent, text = 'MHz',).grid(column = 1, row = 1 + 2*(number-1), sticky = W)
        ttk.Label(parent, text = 'dBm').grid(column = 3, row = 1 + 2*(number-1), sticky = W)
        #configured label
        self.configMsg = ttk.Label(parent, text = self.configured, foreground = 'red',  anchor = E)
        self.configMsg.grid(column = 4, row = 1 + 2*(number-1), sticky=(E,W))
        #configure button
        self.configBtn = ttk.Button(parent, text='configure', command = self.configureButtonPress)
        self.configBtn.grid(column = 5, row = 1 + 2*(number-1))
        #re-cal button
        self.recalBtn = ttk.Button(parent, text = 're-cal', command = self.recalButtonPress)
        self.recalBtn.grid(column = 6, row = 1 + 2*(number-1))
        #frequency entry
        self.freqEntry = ttk.Entry(parent, width = 6, validate = 'focusout', validatecommand = self.freqStringValidate)
        self.freqEntry.insert(0,str(self.freq))
        self.freqEntry.grid(column = 0, row = 1 + 2*(number-1), sticky = (W))
        #power level (spinbox)
        self.powerEntry = Spinbox(parent, value = ('-9', '-6', '-3', '0'), width=2, command = self.powerLevelChange)
        self.powerEntry.delete(0,'end')
        self.powerEntry.insert(0,'0')
        self.powerEntry.grid(column = 2, row = 1 + 2*(number-1), sticky = E)
        #configure row and column weights
        parent.rowconfigure(2 * (number-1), weight = 1)
        parent.rowconfigure(1 + 2 * (number-1), weight = 1)
        parent.columnconfigure(0, weight = 0)
        parent.columnconfigure(1, weight = 0)
        parent.columnconfigure(2, weight = 0)
        parent.columnconfigure(3, weight = 0)
        parent.columnconfigure(4, weight = 1)
        parent.columnconfigure(5, weight = 0)
        parent.columnconfigure(6, weight = 0)

    #config button pressed
    def configureButtonPress(self):
        #determine Odiv and N
        if self.freq >= 4200:
            Odiv = 1
        elif self.freq >= 2100:
            Odiv = 2
        elif self.freq >= 1400:
            Odiv = 3
        elif self.freq >= 1050:
            Odiv = 4
        elif self.freq >= 840:
            Odiv = 5
        elif self.freq >= 700:
            Odiv = 6
        N = self.freq * Odiv
        #print message to console
        print('PLL #' + str(self.number))
        print('N: ' + str(N))
        print('Odiv: ' + str(Odiv))
        print('dBm: ' + str(self.dict_power[self.power]))
        #construct message (Bytes):
        #[0] = CMD, PLL#
        #[1] = dBm, Odiv
        #[2] = N (upper)
        #[4] = N (lower)
        payload = [0, 0, 0, 0, 0, 0, 0] #7 nibbles long
        payload[0] = self.number
        payload[1] = self.dict_power[self.power]
        payload[2] = Odiv
        payload[3] = (N & 0xF000) >> 12
        payload[4] = (N & 0x0F00) >> 8
        payload[5] = (N & 0x00F0) >> 4
        payload[6] = (N & 0x000F)
        #SerialComms.HARA.command(cmd = 'PLL_RECONFIGURE', payload = payload)

        #update configured message
        self.configured = 'configured'
        self.configMsg['text'] = self.configured
        self.configMsg['foreground'] = 'green'

    #recalibrate button pressed
    def recalButtonPress(self):
        #TODO: UART comms
        print('*** PLL Recal ***')
        print('PLL #' + str(self.number))
        #SerialComms.HARA.command(cmd = 'PLL_RECAL', payload = (0, 0, self.number))


    #makes sure the frequency is set to an integer multiple of 1 MHz
    def freqStringValidate(self):
        freq = int(float(self.freqEntry.get()))
        if freq > 6390:
            freq = 6390
        if freq < 700:
            freq = 700
        self.freqEntry.delete(0,'end')
        self.freqEntry.insert(0,str(freq))
        #check if new value was entered
        if freq != self.freq:
            self.configured = 'not configured'
            self.configMsg['text'] = self.configured
            self.configMsg['foreground'] = 'red'
            self.freq = freq
        return 1

    #power level was changed
    def powerLevelChange(self):
        self.powerLevel = int(self.powerEntry.get())
        if self.powerLevel != self.power:
            self.configured = 'not configured'
            self.configMsg['text'] = self.configured
            self.configMsg['foreground'] = 'red'
            self.power = self.powerLevel


#to create PLL tab, simply instantiate 3 PLLs within a frame!

class PFD:
    #dictionary of mux switch values
    dict_mux = {    '3-State'                           : 0,
                    'Digital Lock Detect'               : 1,
                    'N Divider Output'                  : 2,
                    'DVdd'                              : 3,
                    'R Divider Output'                  : 4,
                    'N-Channel Open Drain Lock Detect'  : 5,
                    'Serial Data Out'                   : 6,
                    'DGnd'                              : 7
                    }
    dict_apbw = {   '2.9 ns' : 0,
                    '6.0 ns' : 2
                    }
    dict_icp = {    '0.625 mA' : 0,
                    '1.250 mA' : 1,
                    '1.875 mA' : 2,
                    '2.500 mA' : 3,
                    '3.125 mA' : 4,
                    '3.750 mA' : 5,
                    '4.375 mA' : 6,
                    '5.000 mA' : 7
                    }
    dict_polarity = {'+' : 1,
                     '-' : 0
                    }
    dict_ele = {
        '1' : [1],
        '2' : [2],
        '3' : [3],
        'all' : [1, 2, 3],
    }

    def __init__(self, parent):
        #separator
        ttk.Separator(parent, orient = HORIZONTAL).grid(row = 4, column = 0, columnspan = 7, sticky = (E,W))
        #Label:
        ttk.Label(parent, text = "PFD:").grid(row = 5, column = 0, columnspan = 1, sticky = (N,S,E))
        self.configMsg = ttk.Label(parent, text = 'not configured', foreground = 'red', anchor = E)
        self.configMsg.grid(row = 5, column = 4, columnspan = 1, sticky = (N,S,E,W))
        #PFD element selector (spinbox)
        self.elementSelect = Spinbox(parent, value = ('1', '2', '3', 'all'), width=2)
        self.elementSelect.delete(0,'end')
        self.elementSelect.insert(0,'all')
        self.elementSelect.grid(row = 5, column = 1, sticky = (N,S,W))
        #configure button
        ttk.Button(parent, text = 'Send Message', command = self.PFDmsg).grid(row = 5, column = 5, columnspan = 2, sticky = (E,W))
        #Mux out:
        ttk.Label(parent, text = "Mux:").grid(row = 6, column = 0, columnspan = 1, sticky = (E))
        self.muxSelectCombobox = ttk.Combobox(parent, values = ('N Divider Output', 'R Divider Output', 'Digital Lock Detect', 'N-Channel Open Drain Lock Detect', 'DVdd', 'DGnd', '3-State', 'Serial Data Out'))
        self.muxSelectCombobox.bind('<<ComboboxSelected>>',self.ComboBoxChange)
        self.muxSelectCombobox.set('Digital Lock Detect')
        self.muxSelectCombobox.grid(row = 6, column = 1, columnspan = 4, sticky = (N,S,E,W))
        #Polarity
        ttk.Label(parent, text = "CP Polarity:").grid(row = 6, column = 5, sticky = (N,S,E))
        self.polaritySelectCombobox = ttk.Combobox(parent, values = ('+','-'), width = 2)
        self.polaritySelectCombobox.bind('<<ComboboxSelected>>',self.ComboBoxChange)
        self.polaritySelectCombobox.set('-')
        self.polaritySelectCombobox.grid(row = 6, column = 6, sticky = W)
        #Charge Pump Current
        ttk.Label(parent, text = "Icp:").grid(row = 7, column = 0, sticky = (E))
        self.icpSelectCombobox = ttk.Combobox(parent, values = ('0.625 mA','1.250 mA','1.875 mA','2.500 mA','3.125 mA','3.750 mA','4.375 mA','5.000 mA'), width = 8)
        self.icpSelectCombobox.bind('<<ComboboxSelected>>',self.ComboBoxChange)
        self.icpSelectCombobox.set('0.625 mA')
        self.icpSelectCombobox.grid(row = 7, column = 1, columnspan = 2, sticky = (N,S,E,W))
        #Anti-Backlask Pulse Width
        ttk.Label(parent, text = 'Anti-Backlash Pulse Width:').grid(row = 7, column = 3, columnspan = 3, sticky = (N,S,E))
        self.apbwSelectCombobox = ttk.Combobox(parent, values = ('2.9 ns','6.0 ns'), width = 5)
        self.apbwSelectCombobox.bind('<<ComboboxSelected>>',self.ComboBoxChange)
        self.apbwSelectCombobox.set('6.0 ns')
        self.apbwSelectCombobox.grid(row = 7, column = 6, columnspan = 1, sticky = (N,S,E,W))
        #R divider selection
        ttk.Label(parent, text = 'R Div:').grid(row = 8, column = 0, columnspan = 1, sticky = (N,S,E))
        self.rDivEntry = ttk.Entry(parent, width = 6)
        self.rDivEntry.insert(0,str(50))
        self.rDivEntry.grid(row = 8, column = 1, columnspan = 2, sticky = (W))
        #N divider selection
        ttk.Label(parent, text = 'N Div:').grid(row = 8, column = 3, columnspan = 1, sticky = (N,S,E))
        self.nDivEntry = ttk.Entry(parent, width = 6)
        self.nDivEntry.insert(0,str(50))
        self.nDivEntry.grid(row = 8, column = 4, columnspan = 1, sticky = (W))
        

    def PFDmsg(self):
        #construct and send message
        for ele in self.dict_ele[self.elementSelect.get()]:
            # ele = int(self.elementSelect.get())
            mux = self.dict_mux[self.muxSelectCombobox.get()]
            icp = self.dict_icp[self.icpSelectCombobox.get()]
            apbw = self.dict_apbw[self.apbwSelectCombobox.get()]
            pol = self.dict_polarity[self.polaritySelectCombobox.get()]
            msg = [0,0,0,0,0,0,0,0,0]
            msg[0] = (ele << 1) | ((mux & 0x04) >> 2)
            msg[1] = ((mux & 0x03) << 2) | ((icp & 0x06) >> 1)
            msg[2] = ((icp & 0x01) << 3) | (apbw << 1) | (pol)
            #R divider - 14 bit
            r = int(float(self.rDivEntry.get()))
            msg[3] = (r & (0x0300)) >> 8
            msg[4] = (r & (0x00F0)) >> 4
            msg[5] = (r & (0x000F))
            #N divider - 13 bit
            n = int(float(self.nDivEntry.get()))
            msg[6] = (n & (0x0100)) >> 8
            msg[7] = (n & (0x00F0)) >> 4
            msg[8] = (n & (0x000F))
            #SerialComms.HARA.command('PFD_RECONFIGURE',msg)
        #update configured message
        self.configMsg['text'] = 'configured'
        self.configMsg['foreground'] = 'green'
        #update entry fields
        self.nDivEntry.delete(0,'end')
        self.nDivEntry.insert(0,str(n))
        self.rDivEntry.delete(0,'end')
        self.rDivEntry.insert(0,str(r))

    def ComboBoxChange(self, other):
        self.configMsg['text'] = 'not configured'
        self.configMsg['foreground'] = 'red'
        self.muxSelectCombobox.selection_clear()
        self.icpSelectCombobox.selection_clear()
        self.apbwSelectCombobox.selection_clear()
        self.polaritySelectCombobox.selection_clear()
