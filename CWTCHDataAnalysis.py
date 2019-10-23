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
if not len(dataFiles) == 3:
    sys.exit("number of files does not equal 3. There should be four files - errorsComplete.csv, oddityComplete.csv, and spatialComplete.csv")


#%% Oddity analysis

oddityComplete = pd.read_csv(os.path.join(dataFolder,'oddityComplete.csv'))

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

spatialComplete = pd.read_csv(os.path.join(dataFolder,'spatialComplete.csv'))

# Remove practice data
spatialTestData = spatialComplete[spatialComplete['phase'] != 'practice']

# Create separate dataframes for accuracy and reaction times 
spatialTestDataAccuracy = spatialTestData[['participantID', 'condition', 'response1', 'response2', 'totalFalseAlarms']]
spatialTestDataRT = spatialTestData[['participantID', 'condition', 'rt1', 'rt2']]

# Reshape the dataframes to make it easier to perform calculations
spatialTestDataAccuracy = spatialTestDataAccuracy.melt(id_vars = ['participantID', 'condition', 'totalFalseAlarms'])
spatialTestDataRT = spatialTestDataRT.melt(id_vars = ['participantID', 'condition'])

# Remove rows in the accuracy dataframe where the 'value' column is nan
spatialTestDataAccuracy = spatialTestDataAccuracy[pd.notnull(spatialTestDataAccuracy['value'])]

# Change 'value' column in the accuracy dataframes so that True = 1 and False = 0 
spatialTestDataAccuracy.value = spatialTestDataAccuracy.value.astype(int) 

# Collapse repeated-measures data
spatialGroupedDataAccuracy = spatialTestDataAccuracy.groupby(by = ['participantID', 'condition'], as_index = False)['value', 'totalFalseAlarms'].sum()
spatialGroupedDataRT = spatialTestDataRT.groupby(by = ['participantID', 'condition'], as_index = False)['value'].mean()

# Rename the 'value' columns in both dataframes to reflect its actual meaning
spatialGroupedDataAccuracy = spatialGroupedDataAccuracy.rename(columns = {'value':'totalHits'})
spatialGroupedDataRT = spatialGroupedDataRT.rename(columns = {'value':'meanRT'})

# Export data
spatialGroupedDataAccuracy.to_csv("%s/spatialFinalDataAccuracy.csv" % (figsFolder))
spatialGroupedDataRT.to_csv("%s/spatialFinalDataRT.csv" % (figsFolder))
