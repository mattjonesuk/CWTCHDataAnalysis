#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun May  14 15:31:31 2017

@authors: mattjones, rikkilissaman
"""

#%% THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:

# This is the path of the downloaded data file - it is advised that this should 
# be renamed to something unique for that dataset. 
jsonDataPath = 'insert/path/to/json/here/file.json'

# This is the name of the directory for the output to be saved into. It does 
# not need to be created in advance, as the script will create it.
outputFolder = 'insert/path/to/new/output/directory/here/'

#%% Import data and create lists/dictionaries

import CWTCHFunctions as cf
import os
import pandas as pd

# Load data
jsonData = cf.loadData(jsonDataPath)

# Remove blank entries
jsonData = [x for x in jsonData if x]    

# Create an empty list to store data from both tasks
allOddityData = []
allSpatialData = []

# Create an empty dictionary to store errors from both tasks
errorsOddity = {'participantID': [], 'missing': [], 'aborted': [],
                'abandoned': [], 'prestart': []}
errorsSpatial = {'participantID': [], 'missing': [], 'aborted': [],
                 'abandoned': [], 'prestart': []}

#%% Analyse data 

# Start loop to analyse each participant
for index, participantData in enumerate(jsonData):
    
    # If the list containing participant data has more than 2 elements, remove
    # any element containing incomplete data
    if len(participantData) > 2:
        participantData = [item for item in participantData if item['state'] == 'completed']
        
    # If the list containing participant data has exactly 2 elements
    if len(participantData) == 2:
        # If the first and second element contain spatial data
        if participantData[0]['taskId'] == 'spatial' and participantData[1]['taskId'] == 'spatial':
            # If the first spatial run was prestarted
            if participantData[0]['state'] == 'prestart':
                # Remove the first element
                participantData.remove(participantData[0])
        
    # Get task data
    oddityData = cf.getTaskData(participantData, 'oddity')
    spatialData = cf.getTaskData(participantData, 'spatial')
    
    # If oddity data is missing (i.e. 'None'), append ID and Y/N to dictionary
    if oddityData == 'None':
       errorsOddity['participantID'].append(participantData[0]['panelId'])
       errorsOddity['missing'].append('Yes')
       errorsOddity['aborted'].append('No')
       errorsOddity['abandoned'].append('No')
       errorsOddity['prestart'].append('No')
    # If oddity was not completed, append ID to dictionary then check why
    elif oddityData['state'] != 'completed':
        errorsOddity['participantID'].append(participantData[0]['panelId'])
        # If oddity was aborted, append Y/N to dictionary
        if oddityData['state'] == 'aborted':
            errorsOddity['missing'].append('No')
            errorsOddity['aborted'].append('Yes')
            errorsOddity['abandoned'].append('No')
            errorsOddity['prestart'].append('No')
        # If oddity was abandoned, append Y/N to dictionary
        elif oddityData['state'] == 'abandoned':
            errorsOddity['missing'].append('No')
            errorsOddity['aborted'].append('No')
            errorsOddity['abandoned'].append('Yes')
            errorsOddity['prestart'].append('No')
        # If oddity was prestarted, append Y/N to dictionary
        elif oddityData['state'] == 'prestart':
            errorsOddity['missing'].append('No')
            errorsOddity['aborted'].append('No')
            errorsOddity['abandoned'].append('No')
            errorsOddity['prestart'].append('Yes')
    # If oddity was completed, process the data 
    elif oddityData['state'] == 'completed':
        subjectAllOddityData = cf.processData(oddityData)
        allOddityData.append(subjectAllOddityData)
    
    # If spatial data is missing (i.e. 'None'), append ID and Y/N to dictionary
    if spatialData == 'None':
        errorsSpatial['participantID'].append(participantData[0]['panelId'])
        errorsSpatial['missing'].append('Yes')
        errorsSpatial['aborted'].append('No')
        errorsSpatial['abandoned'].append('No')
        errorsSpatial['prestart'].append('No')
    # If spatial was not completed, append ID to dictionary then check why
    elif spatialData['state'] != 'completed':
        errorsSpatial['participantID'].append(participantData[0]['panelId'])
        # If spatial was aborted, append Y/N to dictionary
        if spatialData['state'] == 'aborted':
            errorsSpatial['missing'].append('No')
            errorsSpatial['aborted'].append('Yes')
            errorsSpatial['abandoned'].append('No')
            errorsSpatial['prestart'].append('No')
        # If spatial was abandoned, append Y/N to dictionary
        elif spatialData['state'] == 'abandoned':
            errorsSpatial['missing'].append('No')
            errorsSpatial['aborted'].append('No')
            errorsSpatial['abandoned'].append('Yes')
            errorsSpatial['prestart'].append('No')
        # If spatial was prestarted, append Y/N to dictionary
        elif spatialData['state'] == 'prestart':
            errorsSpatial['missing'].append('No')
            errorsSpatial['aborted'].append('No')
            errorsSpatial['abandoned'].append('No')
            errorsSpatial['prestart'].append('Yes')
    # If spatial was completed, process the data
    elif spatialData['state'] == 'completed':
        subjectAllSpatialData = cf.processData(spatialData)
        allSpatialData.append(subjectAllSpatialData)
        
    # Print message to console
    print('Participant',index+1, 'done')
        
#%% Format and export data

# Flatten task data
finalOddity = cf.flattenData(allOddityData)
finalSpatial = cf.flattenData(allSpatialData)

# Create output folder
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
# Output task data to CSV
finalOddity.to_csv('%sallOddity.csv' % (outputFolder))
finalSpatial.to_csv('%sallSpatial.csv' % (outputFolder))

# Convert errors to data frame
errorsOddity = pd.DataFrame(errorsOddity)
errorsSpatial = pd.DataFrame(errorsSpatial)

# Output errors to CSV
errorsOddity.to_csv('%serrorsOddity.csv' % (outputFolder))
errorsSpatial.to_csv('%serrorsSpatial.csv' % (outputFolder))
