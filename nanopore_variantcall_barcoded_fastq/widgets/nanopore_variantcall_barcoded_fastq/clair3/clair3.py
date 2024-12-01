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

class OWclair3(OWBwBWidget):
    name = "clair3"
    description = "Clair3 long-read germline variant caller"
    priority = 10
    icon = getIconName(__file__,"clair3_logo.png")
    want_main_area = False
    docker_image_name = "biodepot/clair3"
    docker_image_tag = "v1.0.8"
    inputs = [("bamFile",str,"handleInputsbamFile"),("reference",str,"handleInputsreference"),("model",str,"handleInputsmodel"),("outputDir",str,"handleInputsoutputDir")]
    outputs = [("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    bamFile=pset([])
    reference=pset(None)
    model=pset(None)
    threads=pset(None)
    platform=pset("ont")
    outputDir=pset([])
    rerioModel=pset(False)
    bedFile=pset(None)
    ctgName=pset(None)
    snpMinAf=pset(None)
    indelMinAf=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"clair3")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsbamFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bamFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmodel(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("model", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
