import sys
import CWTCHFunctions as cf
import os
import pandas as pd


## These variables need editing before running the script: 
expectedNoSubjects = 5
jsonDataPath = "/Users/mattjones/Downloads/data.json"
outputFolder = "/Users/mattjones/Downloads/output/"

## NOTHING BELOW NEEDS EDITING!!
# Load data
jsonData = cf.loadData(jsonDataPath)

# Remove blank entries and check size matches
jsonData = [x for x in jsonData if x]

if len(jsonData) != expectedNoSubjects:
    sys.exit("number of loaded subjects does not match the number of expected subjects")
    

# Create an empty list to store all data for each task
allOddityData = []
allSpatialData = []
allPalData = []
errors = []


#%% Start loop to analyse each participant
for index, participantData in enumerate(jsonData):
    
    # get task data
    oddityData = cf.getTaskData(participantData, 'oddity')
    spatialData = cf.getTaskData(participantData, 'spatial')
    palData = cf.getTaskData(participantData, 'pal')
    
    # Oddity Data
    if oddityData is 'None':
        errors.append('No Oddity data for participant - %s' % (participantData[0]['panelId']))
    else:        
        # Oddity data processing
        if oddityData["state"] == "completed":
            subjectAllOddityData = cf.processData(oddityData)
            allOddityData.append(subjectAllOddityData)
            
    # Spatial Data
    if spatialData is 'None':
        errors.append('No Spatial data for participant - %s' % (participantData[0]['panelId']))
    else:        
        # Oddity data processing
        if spatialData["state"] == "completed":
            subjectAllSpatialData = cf.processData(spatialData)
            allSpatialData.append(subjectAllSpatialData)
            
            
    # PAL Data
    if palData is 'None':
        errors.append('No PAL data for participant - %s' % (participantData[0]['panelId']))
    else:        
    # PAL data processing
        if palData["state"] == "completed":
            subjectAllPalData = cf.processData(palData)
            allPalData.append(subjectAllPalData)
       
    print('Participant',index+1, 'done')
    
# Flatten Data

finalOddity = cf.flattenData(allOddityData)
finalSpatial = cf.flattenData(allSpatialData)
finalPal = cf.flattenData(allPalData)

# Create Output Folder
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
# Output to CSV
finalOddity.to_csv("%sallOddity.csv" % (outputFolder))
finalSpatial.to_csv("%sallSpatial.csv" % (outputFolder))
finalPal.to_csv("%sallPal.csv" % (outputFolder))

# Output errors
errors = pd.DataFrame(errors)
errors.to_csv("%serrors.csv" % (outputFolder))