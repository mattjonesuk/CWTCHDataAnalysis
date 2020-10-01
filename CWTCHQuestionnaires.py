#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:34:18 2019

@author: rikkilissaman
"""

#%% THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:

# This is the path to the questionnaire data file
questDataPath = 'insert/path/to/json/here/file.json'

# This is the name of the directory for the output to be saved into. It does 
# not need to be created in advance, as the script will create it.
questDataFolder = 'insert/path/to/new/output/directory/here/'

#%% Import questionnaire data

# Import libraries
import pandas as pd
import os
import CWTCHFunctions as cf

# Load JSON file containing questionnaire data 
questData = cf.loadData(questDataPath)

# Remove blank entries 
questData = [x for x in questData if x]

# Create empty dictionaries to store data for each of the five questionnaires
allDOBData = {'id': [], 'month': [], 'day': []}
allPostTestData = {'id': [], 'q1': [], 'q2': [], 'q3': [], 'q4': [], 'q5': [], 
                   'q6': [], 'q7': [], 'q8': [], 'q9': []}
allLonelyData = {'id': [], 'q1': [], 'q2': [], 'q3': []}
allStressData = {'id': [], 'q1': [], 'q2': [], 'q3': [], 'q4': [], 'q5': [], 
                 'q6': [], 'q7': [], 'q8': [], 'q9': [], 'q10': [], 'q11': [], 
                 'q12': [], 'q13': [], 'q14': [], 'q15': [], 'q16': [], 'q17': [], 
                 'q18': [], 'q19': [], 'q20': [], 'q21': [], 'q22': [], 'q23': []}
allFamHistData = {'id': [], 'parent': [], 'sibling': []}

#%% Analyse data

# Start loop to analyse each participant
for index, participant in enumerate(questData):
    
    # If the dictionary contains 3 elements...
    if len(participant[0]) == 3:
    
        # If the number of questionnaires equals 5...
        if len(participant[0]['questionnaire']) == 5:
            
            # If the first questionnaire is the DOB confirmation...
            if participant[0]['questionnaire'][0]['name'] == 'Month and Day of Birth':
                
                # If the questionnaire is valid...
                if participant[0]['questionnaire'][0]['valid'] == True:
                    
                    # Append data to dictionary
                    allDOBData['id'].append(participant[0]['pid'])
                    allDOBData['month'].append(participant[0]['questionnaire'][0]['responses'][0]['response'])
                    
                    # If the number of responses was 3...
                    if len(participant[0]['questionnaire'][0]['responses'][1]) == 2:
                        
                        # Append data to dictionary
                        allDOBData['day'].append(participant[0]['questionnaire'][0]['responses'][1]['responseText'])
            
            # If the second questionnaire is is the post-test questionnaire...
            if participant[0]['questionnaire'][1]['name'] == 'Post-Test Questionnaire (Version 3, 19/08/2019)':
                
                # If the questionnaire is valid...
                if participant[0]['questionnaire'][1]['valid'] == True:
                    
                    # Append data to dictionary
                    allPostTestData['id'].append(participant[0]['pid'])
                    allPostTestData['q1'].append(participant[0]['questionnaire'][1]['responses'][0]['response'])
                    allPostTestData['q2'].append(participant[0]['questionnaire'][1]['responses'][1]['response'])
                    allPostTestData['q3'].append(participant[0]['questionnaire'][1]['responses'][2]['response'])
                    allPostTestData['q4'].append(participant[0]['questionnaire'][1]['responses'][3]['response'])
                    allPostTestData['q5'].append(participant[0]['questionnaire'][1]['responses'][4]['response'])
                    allPostTestData['q6'].append(participant[0]['questionnaire'][1]['responses'][5]['response'])
                    allPostTestData['q7'].append(participant[0]['questionnaire'][1]['responses'][6]['response'])
                    allPostTestData['q8'].append(participant[0]['questionnaire'][1]['responses'][7]['response'])
                    allPostTestData['q9'].append(participant[0]['questionnaire'][1]['responses'][8]['response'])
                    
            # If the third questionnaire is the loneliness questionnaire...
            if participant[0]['questionnaire'][2]['name'] == 'Loneliness Measurement Tool (Version 3, 19/08/2019)':
                
                # If the questionnaire is valid...
                if participant[0]['questionnaire'][2]['valid'] == True:
                    
                    # Append data to dictionary
                    allLonelyData['id'].append(participant[0]['pid'])
                    allLonelyData['q1'].append(participant[0]['questionnaire'][2]['responses'][0]['response'])
                    allLonelyData['q2'].append(participant[0]['questionnaire'][2]['responses'][1]['response'])
                    allLonelyData['q3'].append(participant[0]['questionnaire'][2]['responses'][2]['response'])
                    
            # If the fourth questionnaire is the perceived stress questionnaire...
            if participant[0]['questionnaire'][3]['name'] == 'Perceived Stress Reactivity Scale (Version 2, 28/08/2018)':
                
                # If the questionnaire is valid...
                if participant[0]['questionnaire'][3]['valid'] == True:
                    
                    # Append data to dictionary
                    allStressData['id'].append(participant[0]['pid'])
                    allStressData['q1'].append(participant[0]['questionnaire'][3]['responses'][0]['response'])
                    allStressData['q2'].append(participant[0]['questionnaire'][3]['responses'][1]['response'])
                    allStressData['q3'].append(participant[0]['questionnaire'][3]['responses'][2]['response'])
                    allStressData['q4'].append(participant[0]['questionnaire'][3]['responses'][3]['response'])
                    allStressData['q5'].append(participant[0]['questionnaire'][3]['responses'][4]['response'])
                    allStressData['q6'].append(participant[0]['questionnaire'][3]['responses'][5]['response'])
                    allStressData['q7'].append(participant[0]['questionnaire'][3]['responses'][6]['response'])
                    allStressData['q8'].append(participant[0]['questionnaire'][3]['responses'][7]['response'])
                    allStressData['q9'].append(participant[0]['questionnaire'][3]['responses'][8]['response'])
                    allStressData['q10'].append(participant[0]['questionnaire'][3]['responses'][9]['response'])
                    allStressData['q11'].append(participant[0]['questionnaire'][3]['responses'][10]['response'])
                    allStressData['q12'].append(participant[0]['questionnaire'][3]['responses'][11]['response'])
                    allStressData['q13'].append(participant[0]['questionnaire'][3]['responses'][12]['response'])
                    allStressData['q14'].append(participant[0]['questionnaire'][3]['responses'][13]['response'])
                    allStressData['q15'].append(participant[0]['questionnaire'][3]['responses'][14]['response'])
                    allStressData['q16'].append(participant[0]['questionnaire'][3]['responses'][15]['response'])
                    allStressData['q17'].append(participant[0]['questionnaire'][3]['responses'][16]['response'])
                    allStressData['q18'].append(participant[0]['questionnaire'][3]['responses'][17]['response'])
                    allStressData['q19'].append(participant[0]['questionnaire'][3]['responses'][18]['response'])
                    allStressData['q20'].append(participant[0]['questionnaire'][3]['responses'][19]['response'])
                    allStressData['q21'].append(participant[0]['questionnaire'][3]['responses'][20]['response'])
                    allStressData['q22'].append(participant[0]['questionnaire'][3]['responses'][21]['response'])
                    allStressData['q23'].append(participant[0]['questionnaire'][3]['responses'][22]['response'])
                    
            # If the fifth questionnaire is the family history of dementia questionnaire...
            if participant[0]['questionnaire'][4]['name'] == 'Family History of Dementia Questionnaire (Version 1, 19/08/2019)':
                
                # If the questionnaire is valid...
                if participant[0]['questionnaire'][4]['valid'] == True:
                    
                    # Append data to dictionary...
                    allFamHistData['id'].append(participant[0]['pid'])
                    allFamHistData['parent'].append(participant[0]['questionnaire'][4]['responses'][0]['response'])
                    allFamHistData['sibling'].append(participant[0]['questionnaire'][4]['responses'][1]['response'])
                
        
#%% Convert the dictionaries to data frames and export

# Convert dictionaries to data frames
dobData = pd.DataFrame.from_dict(allDOBData, orient = 'index')
dobData = dobData.transpose()
postTestData = pd.DataFrame(allPostTestData)
lonelyData = pd.DataFrame(allLonelyData)
stressData = pd.DataFrame(allStressData)
famHistData = pd.DataFrame(allFamHistData)

# Create output folder
if not os.path.exists(questDataFolder):
    os.makedirs(questDataFolder)
    
# Output questionnaire data to CSV
dobData.to_csv('%sdobData.csv' % (questDataFolder))
postTestData.to_csv('%spostTestData.csv' % (questDataFolder))
lonelyData.to_csv('%slonelyData.csv' % (questDataFolder))
stressData.to_csv('%sstressData.csv' % (questDataFolder))
famHistData.to_csv('%sfamHistData.csv' % (questDataFolder))
