#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:31:31 2017

@author: mattjones
"""


## THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:
    
# This is the path for the directory containing the data to be used
dataFolder = '/Users/mattjones/Downloads/testoutput/testfinaloutput'

# This is the name of the directory for the final output to be saved into. It
# needs to be created in advance, as the script does not create it.
figsFolder = '/Users/mattjones/Downloads/FinalOutput'







## NOTHING BELOW NEEDS EDITING!!

import sys
import os
import pandas as pd


# Load data and check contents
dataFiles = os.listdir(dataFolder)
if not len(dataFiles) == 4:
    sys.exit("number of files does not equal 4. There should be four files - errorsComplete.csv, oddityComplete.csv, palComplete.csv, and spatialComplete.csv")


#%% Oddity analysis

oddityComplete = pd.DataFrame.from_csv(os.path.join(dataFolder,'oddityComplete.csv'))

# Remove practice data
oddityTestData = oddityComplete[oddityComplete['kind'] == 'test'] 
oddityTestDataCorrOnly = oddityComplete[oddityComplete['correct'] == True]
oddityTestDataCorrOnly = oddityTestDataCorrOnly[oddityTestDataCorrOnly['kind'] == 'test'] 

# Collapse repeated-measures data
oddityGroupedData=oddityTestData.groupby(by=['participantID', 'condition'], as_index=False)['clickedTime', 'correct'].mean()
oddityGroupedDataCorrOnly=oddityTestDataCorrOnly.groupby(by=['participantID', 'condition'], as_index=False)['clickedTime'].mean()

# Export Data
oddityGroupedData.to_csv("%s/oddityFinalData.csv" % (figsFolder))
oddityGroupedDataCorrOnly.to_csv("%s/oddityCorrOnlyFinalData.csv" % (figsFolder))

#%% Spatial analysis

spatialComplete = pd.DataFrame.from_csv(os.path.join(dataFolder,'spatialComplete.csv'))

# Select only test trials (not probes)
spatialTestData = spatialComplete[spatialComplete['phase'] != 'practice']

# Export Data
spatialTestData.to_csv("%s/spatialFinalData.csv" % (figsFolder))
