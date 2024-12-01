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

class OWPEPPER(OWBwBWidget):
    name = "PEPPER"
    description = "PEPPER-Margin-Deepvariant"
    priority = 6
    icon = getIconName(__file__,"pepper.png")
    want_main_area = False
    docker_image_name = "kishwars/pepper_deepvariant"
    docker_image_tag = "r0.8-gpu"
    inputs = [("inputBam",str,"handleInputsinputBam"),("inputRef",str,"handleInputsinputRef"),("threads",str,"handleInputsthreads"),("trigger",str,"handleInputstrigger")]
    outputs = [("outputDir",str),("outputPrefix",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputBam=pset(None)
    inputRef=pset(None)
    threads=pset(None)
    outputDir=pset(None)
    outputPrefix=pset(None)
    useGPU=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"PEPPER")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputBam(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputBam", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputRef(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputRef", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsthreads(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("threads", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue="/data"
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
        outputValue="/data"
        if hasattr(self,"outputPrefix"):
            outputValue=getattr(self,"outputPrefix")
        self.send("outputPrefix", outputValue)
