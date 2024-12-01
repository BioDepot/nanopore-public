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

class OWcutesv(OWBwBWidget):
    name = "cutesv"
    description = "cuteSV"
    priority = 10
    icon = getIconName(__file__,"cutesv.png")
    want_main_area = False
    docker_image_name = "tuannguyen90/cutesv"
    docker_image_tag = "2.0.3"
    inputs = [("inputFile",str,"handleInputsinputFile"),("reference",str,"handleInputsreference"),("vcfOutput",str,"handleInputsvcfOutput"),("workDir",str,"handleInputsworkDir"),("trigger",str,"handleInputstrigger")]
    outputs = [("File",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputFile=pset(None)
    reference=pset(None)
    vcfOutput=pset(None)
    workDir=pset(None)
    nThreads=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"cutesv")) as f:
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
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsvcfOutput(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("vcfOutput", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsworkDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("workDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"File"):
            outputValue=getattr(self,"File")
        self.send("File", outputValue)
