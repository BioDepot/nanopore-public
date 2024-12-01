#!/bin/bash

shopt -s extglob
inputArgs=("$@")
svim alignment ${inputArgs[@]} $outputDir $inputFile $reference
