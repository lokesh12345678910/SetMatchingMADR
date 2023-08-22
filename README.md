Setting up conda environment
- conda create --name setMatching
- conda activate setMatching
- conda install pip
- pip install syltippy
- pip install syllables
- conda install -c anaconda scipy
- conda install -c anaconda pandas

General command (run from SetMatchingMADR/):
python setMatching.py inputSpreadsheet outputDirectory

specific example (run from SetMatchingMADR/): 
- python setMatching.py FINAL_R01_LRT_PreTx_Probing_DataSheet.csv trialOutput/

Then, open trialOutput/generatedSetsWithFeats and change the Set # of some words. 

Then, to re-run everything, run the following command: 
- python setMatchingChanged.py changedGeneratedSetsWithFeats.csv trialOutput/
This will create a directory named changed_trialOutput

