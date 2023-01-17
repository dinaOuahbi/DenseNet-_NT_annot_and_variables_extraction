
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats as st

################################################ DenseNet Stroma VS Other
'''
model = 'StromaVSautre_densenet/'
snn = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/'
myFiles = os.listdir(f'{snn}Features/{model}')
myTable_sum,myTable_mean,myTable_max,patient = [[] for i in range(4)]
for i in (range(len(myFiles))):
    print(i)
    nom_patient = myFiles[i].split('_',1)[1]
    prediction = pd.read_csv(f"{snn}{model.split('_')[0]}/{nom_patient}", header=None)
    prediction['pred_class'] = None
    for j, val in enumerate(prediction['pred_class']):
        if prediction[1][j]>0.5:
            prediction.loc[j, 'pred_class'] = 'Duodenum'

        elif prediction[2][j]>0.5:
            prediction.loc[j, 'pred_class'] = 'N_T'

        elif prediction[3][j]>0.5:
            prediction.loc[j, 'pred_class'] = 'Stroma'
        else:
            prediction.loc[j, 'pred_class'] = np.nan

    nom_patient = nom_patient.split('.')[0]
    patient.append(nom_patient)
    myTable = pd.read_csv(f'{snn}Features/{model}{myFiles[i]}', header=None)
    c1 = prediction[prediction['pred_class']=='N_T']
    c2 = c1[c1[2] > 0.95]
    myTable = pd.merge(c2[[0]], myTable, on = 0)
    ##################
    print(f'shape = {myTable.shape}')
    myTable.dropna(inplace=True)
    myTable_sum.append(myTable.iloc[:,1:].sum(axis=0))
    myTable_max.append(myTable.iloc[:,1:].max(axis=0))
    myTable_mean.append(myTable.iloc[:,1:].mean(axis=0))

    pd.DataFrame(myTable_sum, index=patient).to_csv(f'{snn}patient_feature_sVSo/df_sum.csv', index=True)
    pd.DataFrame(myTable_mean, index=patient).to_csv(f'{snn}patient_feature_sVSo/df_mean.csv', index=True)
    pd.DataFrame(myTable_max, index=patient).to_csv(f'{snn}patient_feature_sVSo/df_max.csv', index=True)

'''
########################################## DenseNet Normal VS Tumor

model = 'NvsT_densenet/'
snn = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/'
myFiles = os.listdir(f'{snn}Features/{model}')
myTable_sum,myTable_mean,myTable_max,patient = [[] for i in range(4)]
for i in (range(len(myFiles))):
    print(i)
    nom_patient = myFiles[i].split('_',1)[1]
    prediction = pd.read_csv(f"{snn}TumorVSNormal/{nom_patient}", header=None)
    prediction['pred_class'] = None
    for j, val in enumerate(prediction['pred_class']):
        if prediction[1][j]>0.5:
            prediction.loc[j, 'pred_class'] = 'Normal'
        else:
            prediction.loc[j, 'pred_class'] = 'Tumor'

    nom_patient = nom_patient.split('.')[0]

    patient.append(nom_patient)
    myTable = pd.read_csv(f'{snn}Features/{model}{myFiles[i]}', header=None)
    c1 = prediction[prediction['pred_class']=='Tumor']
    c2 = c1[c1[2] > 0.95]
    myTable = pd.merge(c2[[0]], myTable, on = 0)
    ##################
    print(f'shape = {myTable.shape}')
    myTable.dropna(inplace=True)
    myTable_sum.append(myTable.iloc[:,1:].sum(axis=0))
    myTable_max.append(myTable.iloc[:,1:].max(axis=0))
    myTable_mean.append(myTable.iloc[:,1:].mean(axis=0))

    pd.DataFrame(myTable_sum, index=patient).to_csv(f'{snn}patient_feature_NvsT/df_sum.csv', index=True)
    pd.DataFrame(myTable_mean, index=patient).to_csv(f'{snn}patient_feature_NvsT/df_mean.csv', index=True)
    pd.DataFrame(myTable_max, index=patient).to_csv(f'{snn}patient_feature_NvsT/df_max.csv', index=True)
