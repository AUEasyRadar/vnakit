import numpy as np
import skrf as rf


class SignalMath:

    def __init__(self):

        self.potato = 0  # = dead irishmen

    def parsePwrData(self, pwrdict):
        """
        parsePwrData is intended to take the data gathered by the VNA, in dictionary form, and divide the data into
        arrays for each ports received data.
        Input: pwrDict - a dictionary data type containing the data from all 6 ports on the VNA
        :return: dataarray - An array containing the data output by the vna, made more easily accessible.
        """
        portone = np.array(pwrdict[0])
        porttwo = np.array(pwrdict[1])
        portthree = np.array(pwrdict[2])
        portfour = np.array(pwrdict[3])
        portfive = np.array(pwrdict[4])
        portsix = np.array(pwrdict[5])

        dataarray = [portone, porttwo, portthree, portfour, portfive, portsix]
        return dataarray

    def scatMat(self, portdata, freqvec):
        """
        scatMat is intended to determine the scattering matrix for the device under test
        :return:
        """
        s11 = portdata[2]/portdata[0]
        s12 = portdata[3]/portdata[0]
        s21 = portdata[3]/portdata[0]
        s22 = portdata[2]/portdata[0]

        scatmat = [[s11, s21], [s12, s22]]

        s_mat = np.swapaxes(np.array([[s11, s12], [s21, s22]]), 0, 2)
        n_mat = rf.Network(f=freqvec, s=s_mat, z0=50, f_unit='MHz')

        return [scatmat, n_mat]

    def getGamma(self, sparams):
        """
        getGamma determines the reflection coefficient of the device under test. It does this using the S11 parameter of
        the scattering matrix. Assuming that the system is terminated in a matched load.
        :return:
        """
        s_11 = sparams[0]

        gamma = s_11

        return gamma

    def getVSWR(self, gamma):
        """
        getVSWR determines the voltage standing wave ratio (VSWR) associated with the DUT. It uses the gamma found in
        getGamma to determine the VSWR.
        :return:
        """
        vswr = (1+np.absolute(gamma))/(1-np.absolute(gamma))

        return vswr

    def getPortLoss(self, sparams):
        """

        :return:
        """
        insertionloss = -10*np.log10(np.absolute(sparams[1]))  # IL = -10log(S21)
        returnloss = -10*np.log10(np.absolute(sparams[0]))     # RL = -10log(S11)
        lossarray = [insertionloss, returnloss]

        return lossarray

    def getTau(self, gamma):
        """
        getTau takes the gamma value from
        :return:
        """
        tau = 1 + gamma

        return tau
