import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWPEPPER-Margin-Deepvariant(OWBwBWidget):
    name = "PEPPER-Margin-Deepvariant"
    description = "PEPPER-Margin-Deepvariant"
    priority = 9
    icon = getIconName(__file__,"default.png")
    want_main_area = False
    docker_image_name = "kishwars/pepper_deepvariant"
    docker_image_tag = "r0.8-gpu"
    inputs = [("inputFile",str,"handleInputsinputFile"),("inputGenome",str,"handleInputsinputGenome"),("inputRegion",str,"handleInputsinputRegion")]
    outputs = [("outputFile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    InputFile=pset(None)
    InputGenome=pset(None)
    OutputFile=pset(None)
    InputRegion=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"PEPPER-Margin-Deepvariant")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputGenome(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputGenome", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputRegion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputRegion", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
