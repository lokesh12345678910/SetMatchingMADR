Setting up conda environment
- conda create --name setMatching
- conda activate setMatching
- conda install pip
- pip install syltippy
- pip install syllables
- conda install -c anaconda scipy
- conda install -c anaconda pandas



General format of command: ./setMatchingWhileLoop.sh inputSpreadsheet OutputDirectory PMin
Example command: ./setMatchingWhileLoop.sh FINAL_R01_LRT_PreTx_Probing_DataSheet.csv trialOutputLoopP_0.05/ 0.05

This script will keep regenerating sets until all the p-values are > p_min. You'll see output that looks like this:
- Within English, for the feature MRC Concreteness p value between set 2 and 4 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Catalan, for the feature NIM_NLET p value between set 1 and 8 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Spanish, for the feature Espal_NLET p value between set 5 and 7 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within English, for the feature MRC N_of_Syllables p value between set 3 and 7 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within English, for the feature Clearpond_Lexical_Frequency_Eng p value between set 6 and 7 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Spanish, for the feature ClearpondFrequency_PerMil_Esp p value between set 1 and 5 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Catalan, for the feature CAT_SUBTLEX_NSYL p value between set 1 and 8 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Spanish, for the feature Espal_NSYL p value between set 5 and 7 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Spanish, for the feature Espal_NLET p value between set 1 and 4 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Within Spanish, for the feature Espal_NSYL p value between set 2 and 3 is <= 0.05
- Generated sets didn't fulfill p value requirements. Regenerating sets...
- Script executed successfully.
- Number of combinations tried out before all p values were > p_min: 10


If you don't want this loop to occur (i.e. no guarantee that all p values are > p_min), run the following:
- General format of command: python setMatching.py inputSpreadsheet outputDirectory
- Example command: python setMatching.py FINAL_R01_LRT_PreTx_Probing_DataSheet.csv trialOutput/



CHANGING OUTPUT AND RERUNNING T-test

- Open trialOutputLoopP_0.01/generatedSetsWithFeats.csv and change the Set # of some words. save this as trialOutputLoopP_0.01/changedSetsWithFeats.csv
- Then, python setMatchingChanged.py trialOutputLoopP_0.01/changedSetsWithFeats.csv  trialChangedOutput/
- This will create a directory named changed_trialOutput.