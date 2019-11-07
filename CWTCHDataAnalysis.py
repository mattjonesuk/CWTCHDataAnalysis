#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:31:31 2017

@authors: mattjones, rikkilissaman
"""


## THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:
    
# This is the path for the directory containing the data to be used
dataFolder = 'insert/path/to/directory/containing/csv/files/'

# This is the name of the directory for the final output to be saved into. It
# needs to be created in advance, as the script does not create it.
figsFolder = '/insert/path/to/pre-created/output/directory/'

#%% Import data and check

import sys
import os
import pandas as pd


# Load data and check contents
dataFiles = os.listdir(dataFolder)
if not len(dataFiles) == 4:
    sys.exit('number of files does not equal 4. There should be four files - errorsOddityComplete.csv, , errorsSpatialComplete.csv, oddityComplete.csv, and spatialComplete.csv')

#%% Oddity analysis

oddityComplete = pd.read_csv(os.path.join(dataFolder,'oddityComplete.csv'))

# Remove practice data
oddityTestData = oddityComplete[oddityComplete['kind'] == 'test'] 
oddityTestDataCorrOnly = oddityComplete[oddityComplete['correct'] == True]
oddityTestDataCorrOnly = oddityTestDataCorrOnly[oddityTestDataCorrOnly['kind'] == 'test'] 

# Collapse repeated-measures data
oddityGroupedData = oddityTestData.groupby(by = ['participantID', 'condition'], as_index = False)['clickedTime', 'correct'].mean()
oddityGroupedDataCorrOnly = oddityTestDataCorrOnly.groupby(by = ['participantID', 'condition'], as_index = False)['clickedTime'].mean()

# Reshape summary data from long format to wide format
oddityRTData = oddityGroupedData.pivot(index = 'participantID', columns = 'condition', values = 'clickedTime') 
oddityAccuracyData = oddityGroupedData.pivot(index = 'participantID', columns = 'condition', values = 'correct')
oddityRTCorrData = oddityGroupedDataCorrOnly.pivot(index = 'participantID', columns = 'condition', values = 'clickedTime')

# Change column names
oddityRTData.rename(columns = {'3choiceFace': '3choiceFace_RT', '3choiceScene': '3choiceScene_RT',
                    '4choiceFace': '4choiceFace_RT', '4choiceRoom': '4choiceRoom_RT'}, 
                    inplace = True)
oddityAccuracyData.rename(columns = {'3choiceFace': '3choiceFace_corr', '3choiceScene': '3choiceScene_corr',
                    '4choiceFace': '4choiceFace_corr', '4choiceRoom': '4choiceRoom_corr'}, 
                    inplace = True)
oddityRTCorrData.rename(columns = {'3choiceFace': '3choiceFace_corrRT', '3choiceScene': '3choiceScene_corrRT',
                    '4choiceFace': '4choiceFace_corrRT', '4choiceRoom': '4choiceRoom_corrRT'}, 
                    inplace = True)

# Export the data
oddityRTData.to_csv('%s/oddityRTData.csv' % (figsFolder))
oddityAccuracyData.to_csv('%s/oddityAccuracyData.csv' % (figsFolder))
oddityRTCorrData.to_csv('%s/oddityRTCorrData.csv' % (figsFolder))

#%% Spatial analysis

spatialComplete = pd.read_csv(os.path.join(dataFolder,'spatialComplete.csv'))

# Remove practice data
spatialTestData = spatialComplete[spatialComplete['phase'] != 'practice']

# Create separate dataframes for accuracy and reaction times 
spatialTestDataAccuracy = spatialTestData[['participantID', 'condition', 'response1', 'response2', 'totalFalseAlarms']]
spatialTestDataRT = spatialTestData[['participantID', 'condition', 'rt1', 'rt2']]

# Reshape the dataframes to make it easier to perform calculations
spatialTestDataAccuracy = spatialTestDataAccuracy.melt(id_vars = ['participantID', 'condition', 'totalFalseAlarms'],
                                                       value_vars = ['response1', 'response2'],
                                                       var_name = 'response',
                                                       value_name = 'correct')
spatialTestDataRT = spatialTestDataRT.melt(id_vars = ['participantID', 'condition'],
                                           value_vars = ['rt1', 'rt2'],
                                           var_name = 'response',
                                           value_name = 'rt')

# Remove rows in the accuracy dataframe where the 'correct' column is nan
spatialTestDataAccuracy = spatialTestDataAccuracy[pd.notnull(spatialTestDataAccuracy['correct'])]

# Change 'correct' column in the accuracy dataframes so that True = 1 and False = 0 
spatialTestDataAccuracy.correct = spatialTestDataAccuracy.correct.astype(int) 

# Collapse repeated-measures data
spatialGroupedDataAccuracy = spatialTestDataAccuracy.groupby(by = ['participantID', 'condition'], as_index = False)['correct', 'totalFalseAlarms'].sum()
spatialGroupedDataRT = spatialTestDataRT.groupby(by = ['participantID', 'condition'], as_index = False)['rt'].mean()

# Rename the 'value' columns in both dataframes to reflect its actual meaning
spatialGroupedDataAccuracy = spatialGroupedDataAccuracy.rename(columns = {'correct':'totalHits'})
spatialGroupedDataRT = spatialGroupedDataRT.rename(columns = {'rt':'meanRT'})

# Reshape summary data from long format to wide format
spatialRTData = spatialGroupedDataRT.pivot(index = 'participantID', columns = 'condition', values = 'meanRT') 
spatialAccuracyData = spatialGroupedDataAccuracy.pivot(index = 'participantID', columns = 'condition', values = ['totalHits', 'totalFalseAlarms'])

# Change column names - RT data
spatialRTData.rename(columns = {'b1rooms': 'oneBackRooms_RT', 'b1shapes': 'oneBackShapes_RT',
                    'b2rooms': 'twoBackRooms_RT', 'b2shapes': 'twoBackShapes_RT'}, 
                    inplace = True)

# Change column names - accuracy data
spatialAccuracyData.columns = [' '.join(col).strip() for col in spatialAccuracyData.columns.values]
spatialAccuracyData.rename(columns = {'totalHits b1rooms': 'oneBackRooms_totalHits',
                                      'totalFalseAlarms b1rooms': 'oneBackRooms_totalFalseAlarms',
                                      'totalHits b1shapes': 'oneBackShapes_totalHits',
                                      'totalFalseAlarms b1shapes': 'oneBackShapes_totalFalseAlarms',
                                      'totalHits b2rooms': 'twoBackRooms_totalHits',
                                      'totalFalseAlarms b2rooms': 'twoBackRooms_totalFalseAlarms',
                                      'totalHits b2shapes': 'twoBackShapes_totalHits',
                                      'totalFalseAlarms b2shapes': 'twoBackShapes_totalFalseAlarms'}, inplace = True)

# Export data
spatialRTData.to_csv('%s/spatialRTData.csv' % (figsFolder))
spatialAccuracyData.to_csv('%s/spatialAccuracyData.csv' % (figsFolder))
