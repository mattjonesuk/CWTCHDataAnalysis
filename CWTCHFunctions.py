#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  14 15:31:31 2017

@author: mattjones
"""

#%% The loadData function is used to load the json data file.  It can contain mulitple subjects.
def loadData( filename ):

    import json

    with open(filename) as data_file:
        jsondata = json.load(data_file)

    assert isinstance(jsondata, object)
    return jsondata

#%% The loadParticipant function is used to extract all data for a single subject.
def loadParticipant( alljsondata, participantid ):
    
    participantdata = alljsondata[participantid]
    
    return participantdata

#%% The getTaskData function is used to extract the individual tasks from the subject's data.
def getTaskData ( participantdata, taskid ):
    
    taskdata = next((item for item in participantdata if item["taskId"] == taskid), 'None')
  
    return taskdata

#%% The oddityTrialsCheck function is used to check for rare instances whereby the oddity task state is given as completed but the number of trials indicates otherwise
def oddityTrialsCheck(data):
    
    # for x in range 0 to 7 (there are 8 phases for the oddity task)
    for x in range(0, 8):
        # if the oddity task was type 3choiceFace and it was the test phases
        if data['phases'][x]['phase']['type'] == "3choiceFace" and data['phases'][x]['phase']['kind'] == "test":
            # if the length of the trials was anything other than 54
            if len(data['phases'][x]['blocks'][0]['trials']) != 54:
                # change the task state to "trials error"
                data['state'] = "lengthError"
        # if the oddity task was type 3choiceScene and it was the test phases
        if data['phases'][x]['phase']['type'] == "3choiceScene" and data['phases'][x]['phase']['kind'] == "test":
            # if the length of the trials was anything other than 54
            if len(data['phases'][x]['blocks'][0]['trials']) != 54:
                # change the task state to "trials error"
                data['state'] = "lengthError"
        # if the oddity task was type 4choiceFace and it was the test phases
        if data['phases'][x]['phase']['type'] == "4choiceFace" and data['phases'][x]['phase']['kind'] == "test":
            # if the length of the trials was anything other than 40
            if len(data['phases'][x]['blocks'][0]['trials']) != 40:
                # change the task state to "trials error"
                data['state'] = "lengthError"
        # if the oddity task was type 4choiceRoom and it was the test phases
        if data['phases'][x]['phase']['type'] == "4choiceRoom" and data['phases'][x]['phase']['kind'] == "test":
            # if the length of the trials was anything other than 40
            if len(data['phases'][x]['blocks'][0]['trials']) != 40:
                # change the task state to "trials error"
                data['state'] = "lengthError"

    return data

#%% The oddityStimCheck function is used to check for a known coding error associated with two three-choice oddity stimuli
def oddityStimCheck(data):
    
    # for x in range 0 to 7 (there are 8 phases for the oddity task)
    for x in range(0, 8):
        # if the oddity task was type 3choiceFace and it was the test phase
        if data['phases'][x]['phase']['type'] == "3choiceFace" and data['phases'][x]['phase']['kind'] == "test":
            # for y in range 0 to 53 (there are 54 trials in the three-choice oddity test phases)
            for y in range(0, 54):
                # if the stimulus is called "face-male9-3.jpg"
                if data['phases'][x]['blocks'][0]['trials'][y]['stimulus'] == 'face-male9-3.jpg':
                    # if the target was incorrectly listed as 1 (i.e. top image in three-choice oddity)
                    if data['phases'][x]['blocks'][0]['trials'][y]['location'][4] == 1:
                        # change the target location so that it is correctly listed as 3 (i.e. bottom right in three-choice oddity)
                        data['phases'][x]['blocks'][0]['trials'][y]['location'][4] = 3
                    # if the selected location was correctly given as 3 (i.e. bottom right)
                    if data['phases'][x]['blocks'][0]['trials'][y]['location'][0] == 3:
                        # make sure the Boolean is down as "True"
                        data['phases'][x]['blocks'][0]['trials'][y]['location'][3] = True
                    # If the selected location was incorrectly given as 1 or 2 (i.e. top or bottom left)
                    else:
                        # make sure the Boolean is down as "False"
                        data['phases'][x]['blocks'][0]['trials'][y]['location'][3] = False

    # for x in range 0 to 7 (there are 8 phases for the oddity task)
        for x in range(0, 8):
            # if the oddity task was type 3choiceScene and it was the test phase
            if data['phases'][x]['phase']['type'] == "3choiceScene" and data['phases'][x]['phase']['kind'] == "test":
                # for y in range 0 to 53 (there are 54 trials in the three-choice oddity test phases)
                for y in range(0, 54):
                    # if the stimulus is called "scene8-3.jpg"
                    if data['phases'][x]['blocks'][0]['trials'][y]['stimulus'] == 'scene8-3.jpg':
                        # if the target was incorrectly listed as 1 (i.e. top image in three-choice oddity)
                        if data['phases'][x]['blocks'][0]['trials'][y]['location'][4] == 1:
                            # change the target location so that it is correctly listed as 3 (i.e. bottom right in three-choice oddity)
                            data['phases'][x]['blocks'][0]['trials'][y]['location'][4] = 3
                            # if the selected location was correctly given as 3 (i.e. bottom right)
                        if data['phases'][x]['blocks'][0]['trials'][y]['location'][0] == 3:
                            # make sure the Boolean is down as "True"
                            data['phases'][x]['blocks'][0]['trials'][y]['location'][3] = True
                        # If the selected location was incorrectly given as 1 or 2 (i.e. top or bottom left)
                        else:
                            # make sure the Boolean is down as "False"
                            data['phases'][x]['blocks'][0]['trials'][y]['location'][3] = False

    return data

#%% The spatialPracticeCheck function is used to check for "empty" practice blocks and remove them
def spatialPracticeCheck(data):
    
    # for x in range 0 to N length of data
    for x in range(len(data['phases'])):
        # if it was a practice phase but the length was equal to 0
        if data['phases'][x]['phase'] == "practice" and len(data['phases'][x]['blocks']) == 0:
            # remove the practice phase
            del data['phases'][x]
            break

    return data

#%% this function processes the data trial-by-trial and produces a flattened list to return back to the main script
def processData (data):
    
    completeddata = [] # creates an empty list to store the trial data
    
    # the following if statement looks to see the task-type
    if data['taskId'] == 'oddity':
        
        phaseData = data['phases']
                
        # get general data
        participantId = data['panelId']
        datetimeStarted = data['created']
        
        # this loop runs through each phase and flattens the data
        for phaseNo, phase in enumerate(phaseData):
    
            kind = phase['phase']['kind']
            condition = phase['phase']['type']
            block = phase['blocks']
            # this if statement is added as I wasnt sure if there was always  
            # only one entry in the 'block' list just created. So its just an
            # error check.
            if len(block) == 1: 
                phaseStartTime = block[0]['startBlock']
                phaseEndTime = block[0]['endBlock']
                trials = block[0]['trials']
                # the following loop runs through and flattens the trial by 
                # trial data and then appends it to the completeddata list.
                for trialNo, trial in enumerate(trials):
                        trialStartTime = trial['startTrial']
                        trialEndTime = trial['endTrial']
                        stimulus = trial['stimulus']
                        clickedTime = trial['clicked']
                        correct = trial['location'][3]
                        # populate dictionary entry
                        entry = {}
                        entry['participantID'] = participantId
                        entry['datetimeStarted'] = datetimeStarted
                        entry['phaseNo'] = phaseNo
                        entry['kind'] = kind
                        entry['condition'] = condition
                        entry['phaseStartTime'] = phaseStartTime
                        entry['phaseEndTime'] = phaseEndTime
                        entry['trialNo'] = trialNo
                        entry['trialStartTime'] = trialStartTime
                        entry['trialEndTime'] = trialEndTime
                        entry['stimulus'] = stimulus
                        entry['clickedTime'] = clickedTime
                        entry['correct'] = correct
                        #add to list
                        completeddata.append(entry)
            else:
                exit("oddity length of block is greater than one - something wrong!")
         
    elif data['taskId'] == 'spatial':
        
        phaseData = data['phases']
                
        # get general data
        participantId = data['panelId']
        datetimeStarted = data['created']
        
        # this loop runs through each phase and flattens the data
        for phaseNo, phase in enumerate(phaseData):
    
            kind = phase['phase']
            phaseStartTime = phase['startPhase']
            trials = phase['blocks'][0]['trials']
            # the following loop runs through and flattens the trial by 
            # trial data and then appends it to the completeddata list.
            for trialNo, trial in enumerate(trials):
                scndresp = bool(0) # this resets the boolean value that tells the loop below which response it s.
                trialStartTime = trial['startTrial']
                trialEndTime = trial['endTrial']
                condition = trial['condition']
                set1 = trial['set'][0]
                set2 = trial['set'][1]
                set3 = trial['set'][2]
                stimuli = trial['stimuli']

                # the following loop and if statements runs through each each 
                # stimuli in the trial and looks to see if it is correct or not.
                # It looks a bit complicated because it needs to check whether 
                # the trial contains two possible targets or just one.
                for index, stimulus in enumerate(stimuli):
                    if set3 == 6:
                        if scndresp is bool(0):
                            if 'isTarget' in stimulus.keys():
                                targetItem1 = (index)
                                scndresp = bool(1)
                                if 'clicked' in stimulus.keys():
                                    response1 = bool(1)
                                    rt1 = stimulus['clicked']
                                else:
                                    response1 = bool(0)
                                    rt1 = float('nan')
                        elif scndresp is bool(1):
                            if 'isTarget' in stimulus.keys():
                                targetItem2 = (index)
                                if 'clicked' in stimulus.keys():
                                    response2 = bool(1)
                                    rt2 = stimulus['clicked']
                                else:
                                    response2 = bool(0)
                                    rt2 = float('nan')
                    elif set3 == 7:
                        if 'isTarget' in stimulus.keys():
                            targetItem1 = (index)
                            targetItem2 = float('nan')
                            if 'clicked' in stimulus.keys():
                                response1 = bool(1)
                                rt1 = stimulus['clicked']
                                response2 = float('nan')
                                rt2 = float('nan')
                            else:
                                response1 = bool(0)
                                rt1 = float('nan')
                                response2 = float('nan')
                                rt2 = float('nan')
                                
                # the following loop and if statements run through the stimuli
                # in each trial (regardless of whether there were 6 or 7 unique
                # items presented) and checks if the participant clicked despite
                # a target not being presented (i.e. false alarm).
                falseAlarms = [] # create an empty list to store data for false alarms
                
                for index, stimulus in enumerate(stimuli):
                    if 'clicked' in stimulus.keys():
                        if 'isTarget' not in stimulus.keys():
                            falseAlarms.append(1)
                totalFalseAlarms = sum(falseAlarms)
                        
                # populate dictionary entry
                entry = {}
                entry['participantID'] = participantId
                entry['datetimeStarted'] = datetimeStarted
                entry['phaseNo'] = phaseNo
                entry['phase'] = kind
                entry['condition'] = condition
                entry['phaseStartTime'] = phaseStartTime
                entry['trialNo'] = trialNo
                entry['trialStartTime'] = trialStartTime
                entry['trialEndTime'] = trialEndTime
                entry['set1'] = set1
                entry['set2'] = set2
                entry['set3'] = set3
                entry['stimulus'] = stimulus['item']
                entry['targetItem1'] = targetItem1
                entry['response1'] = response1
                entry['rt1'] = rt1
                entry['targetItem2'] = targetItem2
                entry['response2'] = response2
                entry['rt2'] = rt2
                entry['totalFalseAlarms'] = totalFalseAlarms
                #add to list
                completeddata.append(entry)
           
    return completeddata
 
#%% This function is used to transform and flatten the list data into a pandas dataframe
def flattenData ( data ):
    import pandas as pd
    a = pd.DataFrame()
    for participant in data:
        a = a.append(participant)
        
    return a
        
