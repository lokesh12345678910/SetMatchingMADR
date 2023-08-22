conda create --name setMatching
conda activate setMatching
conda install pip
pip install syltippy
pip install syllables
conda install -c anaconda scipy
conda install -c anaconda pandas
cd SetMatching

General:
python setMatchingKesha.py inputSpreadsheet outputDirectory


speciifc example: python setMatching.py FINAL_R01_LRT_PreTx_Probing_DataSheet.csv trialOutput/
