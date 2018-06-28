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

#%% PAL analysis

palComplete = pd.DataFrame.from_csv(os.path.join(dataFolder,'palComplete.csv'))

# Select only test trials (not probes)
palTestData = palComplete[palComplete['kind'] == 'dpal'] 

# Group together trials into six bins of 16 trials
palFlattenedData = pd.DataFrame(columns=['participantID', 'bin', 'correct', 'rt'])
for index, iParticipant in enumerate(set(palTestData['participantID'])):
    participantPalData = palTestData[palTestData['participantID']==iParticipant]
    participantPalBinArray = pd.DataFrame(columns=['participantID', 'bin', 'correct', 'rt'],index=range(1,7))
    for bin in range(1,7):
        if bin == 1:
            binCorrect = participantPalData['correct'].iloc[range(0,16)].mean()
            binRT = participantPalData['rt'].iloc[range(0,16)].mean()
        elif bin == 2:
            binCorrect = participantPalData['correct'].iloc[range(16,32)].mean()
            binRT = participantPalData['rt'].iloc[range(16,32)].mean()  
        elif bin == 3:
            binCorrect = participantPalData['correct'].iloc[range(32,48)].mean()
            binRT = participantPalData['rt'].iloc[range(32,48)].mean() 
        elif bin == 4:
            binCorrect = participantPalData['correct'].iloc[range(48,64)].mean()
            binRT = participantPalData['rt'].iloc[range(48,64)].mean()
        elif bin == 5:
            binCorrect = participantPalData['correct'].iloc[range(64,80)].mean()
            binRT = participantPalData['rt'].iloc[range(64,80)].mean()  
        elif bin == 6:
            binCorrect = participantPalData['correct'].iloc[range(80,96)].mean()
            binRT = participantPalData['rt'].iloc[range(80,96)].mean() 
            
        participantPalBinArray.set_value(bin,'participantID',iParticipant)
        participantPalBinArray.set_value(bin,'bin',bin)
        participantPalBinArray.set_value(bin,'correct',binCorrect)
        participantPalBinArray.set_value(bin,'rt',binRT)
    palFlattenedData = palFlattenedData.append(participantPalBinArray, ignore_index='true')
    palFlattenedData['bin'] = palFlattenedData['bin'].astype('category')

# Export Data
palFlattenedData.to_csv("%s/palFinalData.csv" % (figsFolder))

#%% Spatial analysis

spatialComplete = pd.DataFrame.from_csv(os.path.join(dataFolder,'spatialComplete.csv'))

# Select only test trials (not probes)
spatialTestData = spatialComplete[spatialComplete['phase'] != 'practice']

# Export Data
spatialTestData.to_csv("%s/spatialFinalData.csv" % (figsFolder))