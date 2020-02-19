import numpy as np
import skrf as rf

class dataProcess:

    def __init__(self):

        self.potato = 0 # = dead irishmen

    def processAllTheData(self, pwrdict, returnVar)

        portone = np.array(pwrdict[1]) # TX Power, coupled off
        porttwo = np.array(pwrdict[2]) # Reflected TX Power
        portthree = np.array(pwrdict[3]) # TX Port
        portfour = np.array(pwrdict[4]) # RX Port
        portfive = np.array(pwrdict[5]) # Gibberish
        portsix = np.array(pwrdict[6]) # Gibberish

        s_11 = porttwo/portone  # (Pwr out port 1)/(Pwr in port 1)
        s_21 = portfour/portone # (Pwr out port 2)/(Pwr in port 1)
        s_12 = portone/portfour # Basically useless
        s_22 = portfour/portsix # Basically useless

        gamma = s_11 # Assuming termination is a matched load
        tau = 1 + s_11 # Transmission coefficient of network

        insertionloss = -10*np.log10(np.absolute(sparams[1]))
        returnloss = -10*np.log10(np.absolute(sparams[0]))

        vswr = (1+np.absolute(gamma))/(1-np.absolute(gamma))

        outputDict = {"S11": s11, "S21": s21, "Gamma": gamma, "Tau": tau,
                        "IL": insertionloss, "RL": returnloss, "VSWR": vswr}

        return(outputDict[returnVar])                
