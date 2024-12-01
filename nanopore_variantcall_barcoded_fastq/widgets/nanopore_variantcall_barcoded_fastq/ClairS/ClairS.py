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

class OWClairS(OWBwBWidget):
    name = "ClairS"
    description = "Deep-learning long-read somatic small variant calling"
    priority = 10
    icon = getIconName(__file__,"clairs_icon.png")
    want_main_area = False
    docker_image_name = "hkubal/clairs"
    docker_image_tag = "v0.2.0"
    inputs = [("tumorBam",str,"handleInputstumorBam"),("normalBam",str,"handleInputsnormalBam"),("reference",str,"handleInputsreference"),("outputDir",str,"handleInputsoutputDir")]
    outputs = [("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    tumorBam=pset(None)
    normalBam=pset(None)
    reference=pset(None)
    outputDir=pset(None)
    threads=pset(None)
    platform=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"ClairS")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputstumorBam(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("tumorBam", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsnormalBam(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("normalBam", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
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
