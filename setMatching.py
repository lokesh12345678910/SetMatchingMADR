
import sys
inputSpreadSheet = sys.argv[1]#'FINAL_R01_LRT_PreTx_Probing_DataSheet.csv'
outputDirectory = sys.argv[2]
assert outputDirectory[-1] == '/', print("output directory must end with /")
setMatchingDirectory = "/work/09424/smgrasso1/ls6/SetMatching/" #sys.argv[3] 



"""##Setup Espal"""

from scipy import stats

import numpy as np

import pandas as pd

spanishLingFeatDirectory = 'SpanishLingFeatData/'

espalDF = pd.read_csv(spanishLingFeatDirectory + 'espal.csv')

espalDF = espalDF.fillna("\\N")

espalDF.head()





"""#Table w/ words in Eng, Spa, Cat"""



allWordsDF = pd.read_csv(setMatchingDirectory + inputSpreadSheet)
allWordsDF = allWordsDF.dropna()
allWordsDF.head()

"""#Generating 8 sets of 5 words each"""

generatedSetsDF = allWordsDF.sample(40)
generatedSetsDF.head()


"""#DF for other words not in above"""

# Create a new dataframe with the rows not present in the smaller dataframe
smaller_indices = generatedSetsDF.index

otherWordsDF = allWordsDF[~allWordsDF.index.isin(smaller_indices)]
otherWordsDF.head()

len(otherWordsDF)

"""#Espal_NSYL"""

import warnings


from syltippy import syllabize
#syllables, stress = syllabize(u'supercalifragilísticoespialidoso')
#print(u'-'.join(s if stress != i else s.upper() for (i, s) in enumerate(syllables)))

def espalColumns(df,mapping):
  output = []
  for word in list(df['Palabra en Castellano']):
    if '/' not in word:
      wordOutput = mapping.get(word)
      if wordOutput != None and wordOutput != '\\N':
        output.append(wordOutput)
      else:
        from syltippy import syllabize
        syllables = syllabize(word)
        output.append(len(syllables))
    else:
      possibleWords = word.split('/')
      possibleWordsOutput = []
      for splitWord in possibleWords:
        splitWordOutput = mapping.get(splitWord)
        if splitWordOutput != None and splitWordOutput != '\\N':
          possibleWordsOutput.append(splitWordOutput)
        else:
          from syltippy import syllabize
          possibleWordsOutput.append(len(syllabize(splitWord)))
      warnings.filterwarnings(action='ignore', message='Mean of empty slice')
      output.append(np.nanmean(possibleWordsOutput)) #returns np.nan if possbileWordsOutput is all
  return output

wordNumSyllablesMapping = dict(zip(list(espalDF['word']), list(espalDF['es_num_syll'])))

generatedSetsDF["Espal_NSYL"] = espalColumns(generatedSetsDF,wordNumSyllablesMapping)

otherWordsDF["Espal_NSYL"] = espalColumns(otherWordsDF, wordNumSyllablesMapping)

import collections

collections.Counter(generatedSetsDF["Espal_NSYL"])

collections.Counter(otherWordsDF["Espal_NSYL"])


"""#ESPAL_IMG"""

wordImageabilityMapping = dict(zip(list(espalDF['word']), list(espalDF['imageability'])))

generatedSetsDF["Espal_IMG"] = espalColumns(generatedSetsDF,wordImageabilityMapping)

otherWordsDF["Espal_IMG"] = espalColumns(otherWordsDF, wordImageabilityMapping)

"""#ESPAL_NLET"""

wordNumLettersMapping = dict(zip(list(espalDF['word']), list(espalDF['num_letters'])))

spanishNumLetters = []
for word in generatedSetsDF['Palabra en Castellano']:
  if '/' not in word:
    numLetters = wordNumLettersMapping.get(word)
    if numLetters != None:
      spanishNumLetters.append(numLetters)
    else:
      spanishNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    spanishNumLetters.append(np.nanmean([wordNumLettersMapping.get(word) if wordNumLettersMapping.get(word) != None else len(word) for word in possibleWords]))
generatedSetsDF["Espal_NLET"] = spanishNumLetters

spanishNumLetters = []
for word in otherWordsDF['Palabra en Castellano']:
  if '/' not in word:
    numLetters = wordNumLettersMapping.get(word)
    if numLetters != None:
      spanishNumLetters.append(numLetters)
    else:
      spanishNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    spanishNumLetters.append(np.nanmean([wordNumLettersMapping.get(word) if wordNumLettersMapping.get(word) != None else len(word) for word in possibleWords]))
otherWordsDF["Espal_NLET"] = spanishNumLetters

"""#ESPAL_CON"""


wordConcretenessMapping = dict(zip(list(espalDF['word']), list(espalDF['concreteness'])))

generatedSetsDF["Espal_CON"] = espalColumns(generatedSetsDF,wordConcretenessMapping)

otherWordsDF["Espal_CON"] = espalColumns(otherWordsDF,wordConcretenessMapping)

"""#ESPAL_FAM"""

wordFamiliarityMapping = dict(zip(list(espalDF['word']), list(espalDF['familiarity'])))

generatedSetsDF["Espal_FAM"] = espalColumns(generatedSetsDF,wordConcretenessMapping)

otherWordsDF["Espal_FAM"] = espalColumns(otherWordsDF,wordConcretenessMapping)

"""#Clearpond_Frequency_Spanish"""

textFileAddress = spanishLingFeatDirectory + "spanishCPdatabase2.txt"
textFileAddress


cols  = 'Word Phono Length_Letters Length_Phonomes Frequency sOTAN sOTAF sOTAW sOTHN sOTHF sOTHW sOSAN sOSAF sOSAW sOSHN sOSHF sOSHW sODAN sODAF sODAW sODHN sODHF sODHW sOAAN sOAAF sOAAW sOAHN sOAHF sOAHW sPTAN sPTAF sPTAW sPTHN sPTHF sPTHW sPSAN sPSAF sPSAW sPSHN sPSHF sPSHW sPDAN sPDAF sPDAW sPDHN sPDHF sPDHW sPAAN sPAAF sPAAW sPAHN sPAHF sPAHW dOTAN dOTAF dOTAW dOTHN dOTHF dOTHW dOSAN dOSAF dOSAW dOSHN dOSHF dOSHW dODAN dODAF dODAW dODHN dODHF dODHW dOAAN dOAAF dOAAW dOAHN dOAHF dOAHW dPTAN dPTAF dPTAW dPTHN dPTHF dPTHW dPSAN dPSAF dPSAW dPSHN dPSHF dPSHW dPDAN dPDAF dPDAW dPDHN dPDHF dPDHW dPAAN dPAAF dPAAW dPAHN dPAHF dPAHW eOTAN eOTAF eOTAW eOTHN eOTHF eOTHW eOSAN eOSAF eOSAW eOSHN eOSHF eOSHW eODAN eODAF eODAW eODHN eODHF eODHW eOAAN eOAAF eOAAW eOAHN eOAHF eOAHW ePTAN ePTAF ePTAW ePTHN ePTHF ePTHW ePSAN ePSAF ePSAW ePSHN ePSHF ePSHW ePDAN ePDAF ePDAW ePDHN ePDHF ePDHW ePAAN ePAAF ePAAW ePAHN ePAHF ePAHW fOTAN fOTAF fOTAW fOTHN fOTHF fOTHW fOSAN fOSAF fOSAW fOSHN fOSHF fOSHW fODAN fODAF fODAW fODHN fODHF fODHW fOAAN fOAAF fOAAW fOAHN fOAHF fOAHW fPTAN fPTAF fPTAW fPTHN fPTHF fPTHW fPSAN fPSAF fPSAW fPSHN fPSHF fPSHW fPDAN fPDAF fPDAW fPDHN fPDHF fPDHW fPAAN fPAAF fPAAW fPAHN fPAHF fPAHW gOTAN gOTAF gOTAW gOTHN gOTHF gOTHW gOSAN gOSAF gOSAW gOSHN gOSHF gOSHW gODAN gODAF gODAW gODHN gODHF gODHW gOAAN gOAAF gOAAW gOAHN gOAHF gOAHW gPTAN gPTAF gPTAW gPTHN gPTHF gPTHW gPSAN gPSAF gPSAW gPSHN gPSHF gPSHW gPDAN gPDAF gPDAW gPDHN gPDHF gPDHW gPAAN gPAAF gPAAW gPAHN gPAHF gPAHW'

cols =cols.split()

clearPondDF = pd.read_csv(textFileAddress,delim_whitespace=True, encoding='latin-1', on_bad_lines='skip',names=cols)
clearPondDF.head()

wordFrequencyMapping = dict(zip(list(clearPondDF['Word']), list(clearPondDF['Frequency'])))
wordFrequencyMapping

generatedSetsDF["ClearpondFrequency_PerMil_Esp"] = [wordFrequencyMapping.get(word) if wordFrequencyMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en Castellano']]

otherWordsDF["ClearpondFrequency_PerMil_Esp"] = [wordFrequencyMapping.get(word) if wordFrequencyMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en Castellano']]

"""#Set Number Column"""

setNumbers = []
for i in range(8):
  for j in range(5):
    setNumbers.append(i+1)

generatedSetsDF.insert(0, "Set #", setNumbers)

generatedSetsDF.head()



"""# Assigning Language Column"""

import random
assignmentOrder =['Trained in Spanish','Trained in Spanish','Trained in Spanish','Trained in Catalan','Trained in Catalan','Trained in Catalan','Untrained', 'Untrained']
random.shuffle(assignmentOrder)
assignmentOrder

len(assignmentOrder)

assignedLanguageColumn = []
for i in range(8):
  for j in range(5):
    assignedLanguageColumn.append(assignmentOrder[i])

generatedSetsDF.insert(0, "Assignment", assignedLanguageColumn)

generatedSetsDF.head()

generatedSetsDF.shape

"""#COCA_Frequency_Spanish"""


cocaDF = pd.read_table(setMatchingDirectory + '200k_1103.txt', encoding='latin-1',header=None)
cocaDF.head()

cocaDF.columns = ['ID', 'word', 'freq', '#texts', '%caps', 'Ignore']

cocaDF.head()

cocaFrequencyMapping = dict(zip(list(cocaDF['word']), list(cocaDF['freq'])))
cocaFrequencyMapping

generatedSetsDF["Coca_word Freq (Total) - Web/Dialects"] = [cocaFrequencyMapping.get(word) if cocaFrequencyMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en Castellano']]

otherWordsDF["Coca_word Freq (Total) - Web/Dialects"] = [cocaFrequencyMapping.get(word) if cocaFrequencyMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en Castellano']]

"""#English

##COCA_Frequency_English
"""


cocaEngDF = pd.read_table(setMatchingDirectory + 'words_219k_m2684.txt', encoding='latin-1')
cocaEngDF.head()

cocaFrequencyEngMapping = dict(zip(list(cocaEngDF['word']), list(cocaEngDF['freq'])))

generatedSetsDF["COCA_full freq Eng"] = [cocaFrequencyEngMapping.get(word) if cocaFrequencyEngMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en English']]

otherWordsDF["COCA_full freq Eng"] = [cocaFrequencyEngMapping.get(word) if cocaFrequencyEngMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en English']]

"""##Clearpond_wordLength_orthographic"""

clearPondEnglishCols = 'Word Phono Length_Letters Length_Phonomes Frequency eOTAN eOTAF eOTAW eOTHN eOTHF eOTHW eOSAN eOSAF eOSAW eOSHN eOSHF eOSHW eODAN eODAF eODAW eODHN eODHF eODHW eOAAN eOAAF eOAAW eOAHN eOAHF eOAHW ePTAN ePTAF ePTAW ePTHN ePTHF ePTHW ePSAN ePSAF ePSAW ePSHN ePSHF ePSHW ePDAN ePDAF ePDAW ePDHN ePDHF ePDHW ePAAN ePAAF ePAAW ePAHN ePAHF ePAHW dOTAN dOTAF dOTAW dOTHN dOTHF dOTHW dOSAN dOSAF dOSAW dOSHN dOSHF dOSHW dODAN dODAF dODAW dODHN dODHF dODHW dOAAN dOAAF dOAAW dOAHN dOAHF dOAHW dPTAN dPTAF dPTAW dPTHN dPTHF dPTHW dPSAN dPSAF dPSAW dPSHN dPSHF dPSHW dPDAN dPDAF dPDAW dPDHN dPDHF dPDHW dPAAN dPAAF dPAAW dPAHN dPAHF dPAHW fOTAN fOTAF fOTAW fOTHN fOTHF fOTHW fOSAN fOSAF fOSAW fOSHN fOSHF fOSHW fODAN fODAF fODAW fODHN fODHF fODHW fOAAN fOAAF fOAAW fOAHN fOAHF fOAHW fPTAN fPTAF fPTAW fPTHN fPTHF fPTHW fPSAN fPSAF fPSAW fPSHN fPSHF fPSHW fPDAN fPDAF fPDAW fPDHN fPDHF fPDHW fPAAN fPAAF fPAAW fPAHN fPAHF fPAHW gOTAN gOTAF gOTAW gOTHN gOTHF gOTHW gOSAN gOSAF gOSAW gOSHN gOSHF gOSHW gODAN gODAF gODAW gODHN gODHF gODHW gOAAN gOAAF gOAAW gOAHN gOAHF gOAHW gPTAN gPTAF gPTAW gPTHN gPTHF gPTHW gPSAN gPSAF gPSAW gPSHN gPSHF gPSHW gPDAN gPDAF gPDAW gPDHN gPDHF gPDHW gPAAN gPAAF gPAAW gPAHN gPAHF gPAHW sOTAN sOTAF sOTAW sOTHN sOTHF sOTHW sOSAN sOSAF sOSAW sOSHN sOSHF sOSHW sODAN sODAF sODAW sODHN sODHF sODHW sOAAN sOAAF sOAAW sOAHN sOAHF sOAHW sPTAN sPTAF sPTAW sPTHN sPTHF sPTHW sPSAN sPSAF sPSAW sPSHN sPSHF sPSHW sPDAN sPDAF sPDAW sPDHN sPDHF sPDHW sPAAN sPAAF sPAAW sPAHN sPAHF sPAHW'

clearPondEnglishCols = clearPondEnglishCols.split()

clearPondEnglishDF = pd.read_csv(setMatchingDirectory + 'englishCPdatabase2.txt',delim_whitespace=True, encoding='latin-1', on_bad_lines='skip',header=None,names=clearPondEnglishCols)
clearPondEnglishDF.head()

wordNumLettersEngMapping = dict(zip(list(clearPondEnglishDF['Word']), list(clearPondEnglishDF['Length_Letters'])))

englishNumLetters = []
for word in generatedSetsDF['Palabra en English']:
  if '/' not in word:
    numLetters = wordNumLettersEngMapping.get(word)
    if numLetters != None:
      englishNumLetters.append(numLetters)
    else:
      englishNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    englishNumLetters.append(np.nanmean([wordNumLettersEngMapping.get(word) if wordNumLettersEngMapping.get(word) != None else len(word) for word in possibleWords]))
generatedSetsDF["Clearpond_wordLength_orthographic_Eng"] = englishNumLetters

englishNumLetters = []
for word in otherWordsDF['Palabra en English']:
  if '/' not in word:
    numLetters = wordNumLettersEngMapping.get(word)
    if numLetters != None:
      englishNumLetters.append(numLetters)
    else:
      englishNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    englishNumLetters.append(np.nanmean([wordNumLettersEngMapping.get(word) if wordNumLettersEngMapping.get(word) != None else len(word) for word in possibleWords]))
otherWordsDF["Clearpond_wordLength_orthographic_Eng"] = englishNumLetters

"""##Clearpond_Lexical_Frequency"""

wordFrequencyEngMapping = dict(zip(list(clearPondEnglishDF['Word'].str.lower()), list(clearPondEnglishDF['Frequency'])))

generatedSetsDF["Clearpond_Lexical_Frequency_Eng"] = [wordFrequencyEngMapping.get(word) if wordFrequencyEngMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en English']]

otherWordsDF["Clearpond_Lexical_Frequency_Eng"] = [wordFrequencyEngMapping.get(word) if wordFrequencyEngMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en English']]

"""#English:MRC

##setup
"""

f = open('mrc2.dct')

mrcData = f.read()

mrcData = mrcData.split('\n')

"""##deriving data for one word"""

firstMRCEntry = mrcData[0]
firstMRCEntry

beforeFirstWord = firstMRCEntry.split('||')[0].split()
beforeFirstWord

firstWord=beforeFirstWord[-1]
firstWord

if len(beforeFirstWord[-2]) > 1:
  firstWord = beforeFirstWord[-2] + ' ' +  firstWord
firstWord

firstWordFeatures = beforeFirstWord[0]
firstWordFeatures

firstWordNLet = int(beforeFirstWord[0][0:2])
firstWordNLet

"""Use len(word) as backup"""

firstWordNSyllables = int(beforeFirstWord[0][4])
if firstWordNSyllables == 0:
  firstWordNSyllables = np.nan
firstWordNSyllables

firstWordNSyllables = int(beforeFirstWord[0][4])
if firstWordNSyllables == 0:
  firstWordNSyllables = np.nan
firstWordNSyllables

"""Use English syllabifier as backup"""

firstWordFamiliarity = int(beforeFirstWord[0][25:28])
if firstWordFamiliarity == 0:
  firstWordFamiliarity = np.nan
firstWordFamiliarity

firstWordConcreteness = int(beforeFirstWord[0][28:31])
if firstWordConcreteness == 0:
  firstWordConcreteness = np.nan
firstWordConcreteness

firstWordImagability = int(beforeFirstWord[0][31:34])
if firstWordImagability == 0:
  firstWordImagability = np.nan
firstWordImagability

"""##processing data for all words"""

#each line represents data for a word
mrcRows = []
numWeirdLines = 0
for line in mrcData:
  beforeWord = line.split('|')[0].split()
  #assert len(beforeWord) > 0, print(line)
  if len(beforeWord) == 0:
    numWeirdLines +=1
    continue
  word = beforeWord[-1]
  if word[0] == 'Z' or word[0] == 'N': #looks like Z indicates plural???
    word = word[1:]
  possiblePriorWord =beforeWord[-2]
  if len(possiblePriorWord) > 1 and possiblePriorWord[0].isalpha():
    if len(possiblePriorWord) != 2:
      word = beforeWord[-2] + ' ' +  word
    elif possiblePriorWord[0] != possiblePriorWord[1]: #accounts for 'NN' and 'JJ'
      word = beforeWord[-2] + ' ' +  word
  wordFeatures = beforeWord[0]
  wordNLet = int(wordFeatures[0:2])
  if wordNLet == 0:
    wordNLet = len(word)
    if ' ' in word:
      wordNLet = wordNLet - 1
  wordNSyllables = int(wordFeatures[4])
  if wordNSyllables == 0:
    wordNSyllables = np.nan #TO DO: use english syllabifier
  wordFamiliarity = np.nan
  if len(wordFeatures) >= 28:
    mcrWordFamilarity = int(wordFeatures[25:28])
    if mcrWordFamilarity != 0:
      wordFamiliarity = mcrWordFamilarity
  wordConcreteness = np.nan
  if len(wordFeatures) >= 31:
    mcrWordConcreteness = int(wordFeatures[28:31])
    if mcrWordFamilarity != 0:
      wordConcreteness = mcrWordConcreteness
  wordImageability = np.nan
  if len(wordFeatures) >= 34:
    mcrWordImageability = int(wordFeatures[31:34])
    if mcrWordImageability != 0:
      wordImageability = mcrWordImageability
  mrcRows.append([word.lower(), wordConcreteness,wordFamiliarity,wordImageability,wordNLet,wordNSyllables])

mcrProcessedDF = pd.DataFrame(mrcRows, columns=['word', 'concreteness', 'familiarity', 'imageability', 'nlet', 'nsyllables'])
mcrProcessedDF.head()

"""##Concreteness"""



englishConcretenessMapping = dict(zip(list(mcrProcessedDF['word']), list(mcrProcessedDF['concreteness'])))
englishConcretenessMapping

generatedSetsDF["MRC Concreteness"] = [englishConcretenessMapping.get(word) if englishConcretenessMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en English']]

otherWordsDF["MRC Concreteness"] = [englishConcretenessMapping.get(word) if englishConcretenessMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en English']]

"""##Familiarity"""

englishFamiliarityMapping = dict(zip(list(mcrProcessedDF['word']), list(mcrProcessedDF['familiarity'])))
englishFamiliarityMapping

generatedSetsDF["MRC Familiarity"] = [englishFamiliarityMapping.get(word) if englishFamiliarityMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en English']]

otherWordsDF["MRC Familiarity"] = [englishFamiliarityMapping.get(word) if englishFamiliarityMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en English']]

"""##Imageability"""



englishImageabilityMapping = dict(zip(list(mcrProcessedDF['word']), list(mcrProcessedDF['imageability'])))

generatedSetsDF["MRC Imigability"] = [englishImageabilityMapping.get(word) if englishImageabilityMapping.get(word) != None else np.nan for word in generatedSetsDF['Palabra en English']]

otherWordsDF["MRC Imigability"] = [englishImageabilityMapping.get(word) if englishImageabilityMapping.get(word) != None else np.nan for word in otherWordsDF['Palabra en English']]

"""##N_of_Letters"""



englishNLettersMapping = dict(zip(list(mcrProcessedDF['word']), list(mcrProcessedDF['nlet'])))
englishNLettersMapping

englishMRCNumLetters = []
for word in generatedSetsDF['Palabra en Castellano']:
  if '/' not in word:
    numLetters = englishNLettersMapping.get(word)
    if numLetters != None:
      englishMRCNumLetters.append(numLetters)
    else:
      englishMRCNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    englishMRCNumLetters.append(np.nanmean([englishNLettersMapping.get(word) if englishNLettersMapping.get(word) != None else len(word) for word in possibleWords]))
generatedSetsDF["MRC N_of_Letters"] = englishMRCNumLetters

englishMRCNumLetters = []
for word in otherWordsDF['Palabra en Castellano']:
  if '/' not in word:
    numLetters = englishNLettersMapping.get(word)
    if numLetters != None:
      englishMRCNumLetters.append(numLetters)
    else:
      englishMRCNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    englishMRCNumLetters.append(np.nanmean([englishNLettersMapping.get(word) if englishNLettersMapping.get(word) != None else len(word) for word in possibleWords]))
otherWordsDF["MRC N_of_Letters"] = englishMRCNumLetters

"""##N_of_Syllables"""


import syllables

def syllableColumn(df,mapping):
  output = []
  for word in list(df['Palabra en English']):
    if '/' not in word:
      wordOutput = mapping.get(word)
      if wordOutput != None and wordOutput != '\\N':
        output.append(wordOutput)
      else:
        numSyllables = syllables.estimate(word)
        output.append(numSyllables)
    else:
      possibleWords = word.split('/')
      possibleWordsOutput = []
      for splitWord in possibleWords:
        splitWordOutput = mapping.get(splitWord)
        if splitWordOutput != None and splitWordOutput != '\\N':
          possibleWordsOutput.append(splitWordOutput)
        else:
          possibleWordsOutput.append(syllables.estimate(splitWord))
      warnings.filterwarnings(action='ignore', message='Mean of empty slice')
      output.append(np.nanmean(possibleWordsOutput)) #returns np.nan if possbileWordsOutput is all
  return output

mrcSyllablesMapping = dict(zip(list(mcrProcessedDF['word']), list(mcrProcessedDF['nsyllables'])))

generatedSetsDF["MRC N_of_Syllables"] = syllableColumn(generatedSetsDF,mrcSyllablesMapping)

otherWordsDF["MRC N_of_Syllables"] = syllableColumn(otherWordsDF,mrcSyllablesMapping)



"""#Catalan"""

nimDF = pd.read_table(setMatchingDirectory + 'ctilc.csv')
nimDF.head()

"""##NIM_NSYL (using subtlex for now)

backup online calculator: https://www.softcatala.org/sillabes/
"""

subtlexCatDF = pd.read_csv("CatalanLingFeatData/SUBTLEX-CAT.csv")
subtlexCatDF.head()

catalanNumSyllablesMapping = dict(zip(list(subtlexCatDF['Words']), list(subtlexCatDF['Num_Syl'])))

generatedSetsDF["CAT_SUBTLEX_NSYL"] = [catalanNumSyllablesMapping.get(word) if catalanNumSyllablesMapping.get(word) != None else np.nan for word in generatedSetsDF['Paraula en Català']]

otherWordsDF["CAT_SUBTLEX_NSYL"] = [catalanNumSyllablesMapping.get(word) if catalanNumSyllablesMapping.get(word) != None else np.nan for word in otherWordsDF['Paraula en Català']]

"""##NIM_NLET"""



wordNumLettersCatalanMapping = dict(zip(list(nimDF['paraula']), list(nimDF['lletres'])))

generatedSetsDF.columns

catalanNumLetters = []
for word in generatedSetsDF['Paraula en Català']:
  if '/' not in word:
    numLetters = wordNumLettersCatalanMapping.get(word)
    if numLetters != None:
      catalanNumLetters.append(numLetters)
    else:
      catalanNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    catalanNumLetters.append(np.nanmean([wordNumLettersCatalanMapping.get(word) if wordNumLettersCatalanMapping.get(word) != None else len(word) for word in possibleWords]))
generatedSetsDF["NIM_NLET"] = catalanNumLetters

catalanNumLetters = []
for word in otherWordsDF['Paraula en Català']:
  if '/' not in word:
    numLetters = wordNumLettersCatalanMapping.get(word)
    if numLetters != None:
      catalanNumLetters.append(numLetters)
    else:
      catalanNumLetters.append(len(word))
  else:
    possibleWords = word.split('/')
    catalanNumLetters.append(np.nanmean([wordNumLettersCatalanMapping.get(word) if wordNumLettersCatalanMapping.get(word) != None else len(word) for word in possibleWords]))
otherWordsDF["NIM_NLET"] = catalanNumLetters

"""##NIM_WordFreq (per million)"""

nimDF.head()

wordFreqRelativaMapping = dict(zip(list(nimDF['paraula']), list(nimDF['f_relativa'])))

generatedSetsDF["NIM_WordFreq_Relativa"] = [wordFreqRelativaMapping.get(word) if wordFreqRelativaMapping.get(word) != None else np.nan for word in generatedSetsDF['Paraula en Català']]

otherWordsDF["NIM_WordFreq_Relativa"] = [wordFreqRelativaMapping.get(word) if wordFreqRelativaMapping.get(word) != None else np.nan for word in otherWordsDF['Paraula en Català']]

"""##NIM_WordFreq (Total)"""

wordFreqTotalCatalanMapping = dict(zip(list(nimDF['paraula']), list(nimDF['f_absoluta'])))

generatedSetsDF["NIM_WordFreq_Total_Absoluta"] = [wordFreqTotalCatalanMapping.get(word) if wordFreqTotalCatalanMapping.get(word) != None else np.nan for word in generatedSetsDF['Paraula en Català']]

otherWordsDF["NIM_WordFreq_Total_Absoluta"] = [wordFreqTotalCatalanMapping.get(word) if wordFreqTotalCatalanMapping.get(word) != None else np.nan for word in otherWordsDF['Paraula en Català']]

"""##

#Save otherWordsDF
"""

otherWordsDF.head()

otherWordsDF.fillna('NA', inplace=True)
otherWordsDF.to_csv(outputDirectory + 'otherWordsWithFeats.csv', index=False)

"""#COSP (TBC)

#split into 5
"""

generatedSetsDF.head()



splitGeneratedSetsDf = np.array_split(generatedSetsDF, 8)
len(splitGeneratedSetsDf)

for generatedSet in splitGeneratedSetsDf:
    print(type(generatedSet))


"""#t-tests

##Within Spanish
"""


descriptors = []
for i in range(8):
  for j in range(8):
    if i == j:
      continue
    descriptors.append("S" + str(i+1) + "," + str(j+1))
print(descriptors)

def ttest_feature(feature,p_condition=0.01):
  p_vals = []
  for i in range(8):
    for j in range(8):
      if i == j:
        #p_vals.append(np.nan)
        continue
      list1 = splitGeneratedSetsDf[i][feature].dropna()
      list2 = splitGeneratedSetsDf[j][feature].dropna()
      if len(list1) <= 2:
        p_vals.append(np.nan)
        continue
      if len(list2) <= 2:
        p_vals.append(np.nan)
        continue
      _, p_value = stats.ttest_ind(list1, list2)
      #assert p_value > p_condition, print("For the feature", feature, "p value between set", str(i+1), "and", str(j+1), "is <=", str(p_condition))
      p_vals.append(p_value)
  return p_vals


cols = ['Espal_NSYL','Espal_NLET','ClearpondFrequency_PerMil_Esp',"Coca_word Freq (Total) - Web/Dialects"]

ttestData = np.array([ttest_feature(col) for col in cols])

ttestDF = pd.DataFrame(ttestData.T, columns = cols)
ttestDF.head()

ttestDF.insert(0, "Ttests Within Languages_Spanish", descriptors)

ttestDF.head()

ttestDF.tail()

ttestDF.fillna('Invalid',inplace=True)

ttestDF.to_csv(outputDirectory + 'ttestWithinSpanish.csv', index=False)

"""##Within Catalan"""

from scipy import stats

def ttest_feature(feature,p_condition=0.01):
  p_vals = []
  for i in range(8):
    for j in range(8):
      if i == j:
        #p_vals.append(np.nan)
        continue
      list1 = splitGeneratedSetsDf[i][feature].dropna()
      list2 = splitGeneratedSetsDf[j][feature].dropna()
      if len(list1) <= 2:
        p_vals.append(np.nan)
        continue
      if len(list2) <= 2:
        p_vals.append(np.nan)
        continue
      _, p_value = stats.ttest_ind(list1, list2)
      #assert p_value > p_condition, print("For the feature", feature, "p value between set", str(i+1), "and", str(j+1), "is <=", str(p_condition))
      p_vals.append(p_value)
  return p_vals


cols = ['CAT_SUBTLEX_NSYL','NIM_NLET','NIM_WordFreq_Relativa',"NIM_WordFreq_Total_Absoluta"]

ttestData = np.array([ttest_feature(col) for col in cols])

ttestDF = pd.DataFrame(ttestData.T, columns = cols)
ttestDF.head()

ttestDF.insert(0, "Ttests Within Languages_Catalan", descriptors)

ttestDF.head()

ttestDF.tail()

#ttestDF.fillna('Invalid',inplace=True)

ttestDF.to_csv(outputDirectory + 'ttestWithinCatalan.csv', index=False)

"""##Within English"""



from scipy import stats

def ttest_feature(feature,p_condition=0.01):
  p_vals = []
  for i in range(8):
    for j in range(8):
      if i == j:
        #p_vals.append(np.nan)
        continue
      list1 = splitGeneratedSetsDf[i][feature].dropna()
      list2 = splitGeneratedSetsDf[j][feature].dropna()
      if len(list1) <= 2:
        p_vals.append(np.nan)
        continue
      if len(list2) <= 2:
        p_vals.append(np.nan)
        continue
      _, p_value = stats.ttest_ind(list1, list2)
      #assert p_value > p_condition, print("For the feature", feature, "p value between set", str(i+1), "and", str(j+1), "is <=", str(p_condition))
      p_vals.append(p_value)
  return p_vals

generatedSetsDF.columns



cols = ['MRC Imigability','MRC Concreteness',
       'MRC Familiarity', 'MRC N_of_Letters',
       'MRC N_of_Syllables','Clearpond_Lexical_Frequency_Eng']

ttestData = np.array([ttest_feature(col) for col in cols])

# Create the pandas DataFrame
ttestDF = pd.DataFrame(ttestData.T, columns = ['MRC Imageability', 'MRC Concretness', 'MRC Familiarity', 'MRC N_of_Letters', 'MRC_Number of Syllables', 'Clearpond lexical frequency'])

# print dataframe.
ttestDF.head()

ttestDF.insert(0, "Ttests Within Languages_English", descriptors)

ttestDF.head()

ttestDF.tail()

#ttestDF.fillna('Invalid',inplace=True)

ttestDF.to_csv(outputDirectory + 'ttestWithinEnglish.csv', index=False)


"""##English vs Spanish"""

generatedSetsDF.columns

def ttest_feature_across_lang(featureLang1, featureLang2,p_condition=0.01):
  p_vals = []
  for i in range(8):
    for j in range(8):
      if i == j:
        #p_vals.append(np.nan)
        continue
      list1 = splitGeneratedSetsDf[i][featureLang1].dropna()
      list2 = splitGeneratedSetsDf[j][featureLang2].dropna()
      if len(list1) <= 2:
        p_vals.append(np.nan)
        continue
      if len(list2) <= 2:
        p_vals.append(np.nan)
        continue
      _, p_value = stats.ttest_ind(list1, list2)
      #assert p_value > p_condition, print("For the feature", feature, "p value between set", str(i+1), "and", str(j+1), "is <=", str(p_condition))
      p_vals.append(p_value)
  return p_vals




ttestData = np.array([ttest_feature_across_lang('Espal_NLET','MRC N_of_Letters'), ttest_feature_across_lang('ClearpondFrequency_PerMil_Esp','Clearpond_Lexical_Frequency_Eng'),ttest_feature_across_lang('Coca_word Freq (Total) - Web/Dialects','COCA_full freq Eng')])

# Create the pandas DataFrame
ttestDF = pd.DataFrame(ttestData.T, columns = ['Number of letters', 'Clearpond_Frequency across languages', 'Freq_COCA'])

# print dataframe.
ttestDF.head()

ttestDF.insert(0, "Ttests: Across Languages- Eng vs. Spanish", descriptors)

ttestDF.head()

ttestDF.tail()

ttestDF.to_csv(outputDirectory + 'ttestAcrossEnglishAndSpanish.csv', index=False)

"""#Download generated sets with feats"""

generatedSetsDF.fillna('NaN', inplace=True)
generatedSetsDF.to_csv(outputDirectory + 'generatedSetsWithFeats.csv', index=False)

"""# Assigning Part 2"""

trainedSpanishDFIndexes = [i for i, string in enumerate(assignmentOrder) if string == 'Trained in Spanish']
trainedCatalanDFIndexes = [i for i, string in enumerate(assignmentOrder) if string == 'Trained in Catalan']
untrainedIndexes = [i for i, string in enumerate(assignmentOrder) if string == 'Untrained']

trainedSpanishDFs = [splitGeneratedSetsDf[i] for i in trainedSpanishDFIndexes]
trainedCatalanDFs = [splitGeneratedSetsDf[i] for i in trainedCatalanDFIndexes]
untrainedDFs = [splitGeneratedSetsDf[i] for i in untrainedIndexes]

trainedSpanishDFIndexes

allTrainedSpanishDF = pd.concat(trainedSpanishDFs)
allTrainedSpanishDF.head()

allTrainedCatalanDF = pd.concat(trainedCatalanDFs)
allTrainedCatalanDF.head()

"""#Across languages t-tests

##Trained Spanish vs Trained Catalan
"""



pVals_trainedSpanishVsTrainedCatalan = []
_, p_nsyl = stats.ttest_ind(allTrainedSpanishDF['Espal_NSYL'].dropna(), allTrainedCatalanDF['CAT_SUBTLEX_NSYL'].dropna())
_, p_nlet = stats.ttest_ind(allTrainedSpanishDF['Espal_NLET'].dropna(), allTrainedCatalanDF['NIM_NLET'].dropna())
_, p_wordFreq = stats.ttest_ind(allTrainedSpanishDF['Coca_word Freq (Total) - Web/Dialects'].dropna(), allTrainedCatalanDF['NIM_WordFreq_Relativa'].dropna())
pVals_trainedSpanishVsTrainedCatalan = [p_nsyl,p_nlet,p_wordFreq]

print(pVals_trainedSpanishVsTrainedCatalan)

"""##Trained Catalan vs Untrained Catalan"""

allUntrainedDFs = pd.concat(untrainedDFs)
allUntrainedDFs.head()

pVals_trainedCatalanVsUntrainedCatalan = []
_, p_nsyl = stats.ttest_ind(allTrainedCatalanDF['CAT_SUBTLEX_NSYL'].dropna(), allUntrainedDFs['CAT_SUBTLEX_NSYL'].dropna())
_, p_nlet = stats.ttest_ind(allTrainedCatalanDF['NIM_NLET'].dropna(), allUntrainedDFs['NIM_NLET'].dropna())
_, p_wordFreq = stats.ttest_ind(allTrainedCatalanDF['NIM_WordFreq_Relativa'].dropna(), allUntrainedDFs['NIM_WordFreq_Relativa'].dropna())
pVals_trainedCatalanVsUntrainedCatalan = [p_nsyl,p_nlet,p_wordFreq]
print(pVals_trainedCatalanVsUntrainedCatalan)

"""##Trained Spanish Vs Untrained Catalan"""

pVals_trainedSpanishVsUntrainedCatalan = []
_, p_nsyl = stats.ttest_ind(allTrainedSpanishDF['Espal_NSYL'].dropna(), allUntrainedDFs['CAT_SUBTLEX_NSYL'].dropna())
_, p_nlet = stats.ttest_ind(allTrainedSpanishDF['Espal_NLET'].dropna(), allUntrainedDFs['NIM_NLET'].dropna())
_, p_wordFreq = stats.ttest_ind(allTrainedSpanishDF['Coca_word Freq (Total) - Web/Dialects'].dropna(), allUntrainedDFs['NIM_WordFreq_Relativa'].dropna())
pVals_trainedSpanishVsUntrainedCatalan = [p_nsyl,p_nlet,p_wordFreq]
print(pVals_trainedSpanishVsUntrainedCatalan)

"""##Trained Spanish Vs Untrained Spanish"""

pVals_trainedSpanishVsUntrainedSpanish = []
_, p_nsyl = stats.ttest_ind(allTrainedSpanishDF['Espal_NSYL'].dropna(), allUntrainedDFs['Espal_NSYL'].dropna())
_, p_nlet = stats.ttest_ind(allTrainedSpanishDF['Espal_NLET'].dropna(), allUntrainedDFs['Espal_NLET'].dropna())
_, p_wordFreq = stats.ttest_ind(allTrainedSpanishDF['Coca_word Freq (Total) - Web/Dialects'].dropna(), allUntrainedDFs['Coca_word Freq (Total) - Web/Dialects'].dropna())
pVals_trainedSpanishVsUntrainedSpanish = [p_nsyl,p_nlet,p_wordFreq]
print(pVals_trainedSpanishVsUntrainedSpanish)

"""##Trained Catalan Vs Untrained Spanish"""

pVals_trainedCatalanVsUntrainedSpanish = []
_, p_nsyl = stats.ttest_ind(allTrainedCatalanDF['CAT_SUBTLEX_NSYL'].dropna(), allUntrainedDFs['Espal_NSYL'].dropna())
_, p_nlet = stats.ttest_ind(allTrainedCatalanDF['NIM_NLET'].dropna(), allUntrainedDFs['Espal_NLET'].dropna())
_, p_wordFreq = stats.ttest_ind(allTrainedCatalanDF['NIM_WordFreq_Relativa'].dropna(), allUntrainedDFs['Coca_word Freq (Total) - Web/Dialects'].dropna())
pVals_trainedCatalanVsUntrainedSpanish = [p_nsyl,p_nlet,p_wordFreq]
print(pVals_trainedCatalanVsUntrainedSpanish)

"""Summarize and output"""

acrossLanguageTestPVals = [pVals_trainedSpanishVsTrainedCatalan,pVals_trainedCatalanVsUntrainedCatalan,pVals_trainedSpanishVsUntrainedCatalan,pVals_trainedSpanishVsUntrainedSpanish,pVals_trainedCatalanVsUntrainedSpanish]

acrossLanguageTestDFs = pd.DataFrame(acrossLanguageTestPVals, columns = ['N_SYL', 'NLET', 'WordFreq'])
acrossLanguageTestDFs.head()

descriptors = ['TrainedSpanishVsTrainedCatalan', 'TrainedCatalanVsUntrainedCatalan', 'TrainedSpanishVsUntrainedCatalan','TrainedSpanishVsUntrainedSpanish','TrainedCatalanVsUntrainedSpanish' ]

acrossLanguageTestDFs.insert(0,'Descriptor',descriptors)
acrossLanguageTestDFs.head()

acrossLanguageTestDFs.to_csv(outputDirectory + 'acrossLanguageTTests.csv', index=False)

