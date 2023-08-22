"""#Changed spreadsheet

##load in changed spreadsheet
"""

import pandas as pd

changedSetsWithFeatsDF = pd.read_csv('changedGeneratedSetsWithFeats.csv')
changedSetsWithFeatsDF.head()

"""##Fix assignment order"""

originalAssignmentOrder = list(changedSetsWithFeatsDF['Assignment'])

del changedSetsWithFeatsDF['Assignment']
changedSetsWithFeatsDF.head()

#sorted by Set #
changedSetsWithFeatsDF = changedSetsWithFeatsDF.sort_values('Set #')
changedSetsWithFeatsDF.head()

#bring bank assignment column
changedSetsWithFeatsDF.insert(0, "Assignment", originalAssignmentOrder)

changedSetsWithFeatsDF

"""##split into 5"""

splitGeneratedSetsDf = np.array_split(changedSetsWithFeatsDF, 8) # THIS LINE IS VERY IMPORANT, changedSetsWithFeatsDF instead of generatedSetsDF
len(splitGeneratedSetsDf)

for generatedSet in splitGeneratedSetsDf:
    print(type(generatedSet))

splitGeneratedSetsDf[0]

splitGeneratedSetsDf[7]

"""#t-tests

##Within Spanish
"""

from scipy import stats

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

ttest_feature('Espal_CON')

ttest_feature('Espal_NSYL')

len(ttest_feature("Espal_NLET"))

cols = ['Espal_NSYL','Espal_NLET','ClearpondFrequency_PerMil_Esp',"Coca_word Freq (Total) - Web/Dialects"]

ttestData = np.array([ttest_feature(col) for col in cols])

ttestDF = pd.DataFrame(ttestData.T, columns = cols)
ttestDF.head()

ttestDF.insert(0, "Ttests Within Languages_Spanish", descriptors)

ttestDF.head()

ttestDF.tail()

ttestDF.fillna('Invalid',inplace=True)

ttestDF.to_csv(outputDirectory  + 'ttestWithinSpanish.csv', index=False)

"""##Within Catalan"""


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

ttest_feature('CAT_SUBTLEX_NSYL')

ttest_feature('NIM_NLET')

ttest_feature('NIM_WordFreq_Relativa')

ttest_feature('NIM_WordFreq_Total_Absoluta')

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

ttest_feature_across_lang('Espal_NLET','MRC N_of_Letters')

ttest_feature_across_lang('ClearpondFrequency_PerMil_Esp','Clearpond_Lexical_Frequency_Eng')

ttest_feature_across_lang('Coca_word Freq (Total) - Web/Dialects','COCA_full freq Eng')



ttestData = np.array([ttest_feature_across_lang('Espal_NLET','MRC N_of_Letters'), ttest_feature_across_lang('ClearpondFrequency_PerMil_Esp','Clearpond_Lexical_Frequency_Eng'),ttest_feature_across_lang('Coca_word Freq (Total) - Web/Dialects','COCA_full freq Eng')])

# Create the pandas DataFrame
ttestDF = pd.DataFrame(ttestData.T, columns = ['Number of letters', 'Clearpond_Frequency across languages', 'Freq_COCA'])

# print dataframe.
ttestDF.head()

ttestDF.insert(0, "Ttests: Across Languages- Eng vs. Spanish", descriptors)

ttestDF.head()

ttestDF.tail()

ttestDF.to_csv(outputDirectory  + 'ttestAcrossEnglishAndSpanish.csv', index=False)

"""#Download generated sets with feats"""

changedSetsWithFeatsDF.fillna('NaN', inplace=True)
changedSetsWithFeatsDF.to_csv(outputDirectory  + 'changedSetsWithFeats.csv', index=False)

"""# Assigning Part 2"""

assignmentOrder

trainedSpanishDFIndexes = [i for i, string in enumerate(assignmentOrder) if string == 'Trained in Spanish']
trainedCatalanDFIndexes = [i for i, string in enumerate(assignmentOrder) if string == 'Trained in Catalan']
untrainedIndexes = [i for i, string in enumerate(assignmentOrder) if string == 'Untrained']

splitGeneratedSetsDf



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

