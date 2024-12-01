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

class OWCNVkit(OWBwBWidget):
    name = "CNVkit"
    description = "Python detect copy number variants and alterations"
    priority = 10
    icon = getIconName(__file__,"cnvkit.png")
    want_main_area = False
    docker_image_name = "quay.io/biocontainers/cnvkit"
    docker_image_tag = "0.9.11--pyhdfd78af_0"
    inputs = [("tumorFile",str,"handleInputstumorFile"),("normalFile",str,"handleInputsnormalFile"),("reference",str,"handleInputsreference"),("outputDir",str,"handleInputsoutputDir")]
    outputs = [("File",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    tumorFile=pset([])
    normalFile=pset([])
    reference=pset(None)
    targetBed=pset(None)
    antitargetBed=pset(None)
    outputDir=pset(None)
    seqMethod=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"CNVkit")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputstumorFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("tumorFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsnormalFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("normalFile", value, args[0][0], test=args[0][3])
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
        if hasattr(self,"File"):
            outputValue=getattr(self,"File")
        self.send("File", outputValue)
