# CWTCHDataAnalysis

## About 
The CWTCHDataAnalysis scripts import, tidy and transform cognitive data collected using the Cardiff Web Tools for Cognitive Health (CWTCH) online research platform (https://cwtch.ounce.ac/). This platform was developed by Ounce Technology (www.ouncetech.co.uk) in collaboration with researchers at Cardiff University, UK. 

## Prerequisites
In order to run the scripts successfully, you will need:
•	Python 3.6 / 3.7 
•	Project data file(s) downloaded in JSON format

We recommend that users install and use the Spyder IDE. 

If this has not yet been done, follow the steps below:
1.	Download and install Anaconda Navigator: https://docs.anaconda.com/anaconda/navigator/install/
2.	Open Anaconda Navigator and click to install Spyder
3.	Click to launch Spyder once installed

## Summary of Analysis Scripts

•	CWTCHDataCleaning.py

This script sorts through the JSON data file, removing any incomplete data and restructuring the data into a matrix-like format. This is then saved in CSV format to be then used in R (or similar statistical package). Note: Editable fields need to be amended at the top of the script.

•	CWTCHConcatData.py

This script joins together multiple output CSV files from the CWTCHDataCleaning.py script. It is used when there are multiple data files for a single project, such as when running a study with counterbalancing. It outputs a concatenated CSV file. Note: Editable fields need to be amended at the top of the script. The input directory should contain multiple sub-directories, each containing the output files from the CWTCHDataCleaning.py script.

•	CWTCHDataAnalysis.py

This script summarises the data in a more appropriate format. For the Oddity task, it generates three CSV files (one with reaction time data for all items, one with reaction time data for correct items, and one with accuracy data) in a summary format with one row per subject. For the Spatial task, it generates two CSV files (one with reaction time data for all items, and one with hits/misses data) in a summary format with one row per subject. Note: Editable fields need to be amended at the top of the script.

•	CWTCHFunctions.py

This contains code for functions that are required for each of the above scripts. It should not be run or edited, but needs to be placed in the same directory as the other scripts.
