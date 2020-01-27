class Antenna:
    #The constructor. Run when the class is called by Antenna() 
    def __init__(self, antennaName):
        self.name =  antennaName
    def printName(self):
        print(self.name)
        return 

ant = Antenna('Antenna name')
ant.printName()