# python v 3
# script pour calcule kappa qupath_pred vs francoi annotation
# DO


import pandas as pd
import numpy as np
import re
import os
import json
from sklearn.metrics import cohen_kappa_score
import matplotlib.pyplot as plt

annot_fr = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/lame francois/'
annot_qp = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/CombModels_BSC_prediction_without_border/'
l = os.listdir(f'{annot_fr}output_1/')

def class_wise_kappa(true, pred, n_classes=None, ignore_zero=True):
    #kp_score_all = cohen_kappa_score(true, pred,labels=None, weights=None, sample_weight=None)

    if n_classes is None:
        classes = np.unique(true)
    else:
        classes = np.arange(max(2, n_classes))
    # Ignore background class?
    if ignore_zero:
        classes = classes[np.where(classes != 0)]

    # Calculate kappa for all targets
    kappa_scores = np.empty(shape=classes.shape, dtype=np.float32)
    kappa_scores.fill(np.nan)
    dico = {}
    for idx, _class in enumerate(classes):
        s1 = true == _class
        s2 = pred == _class
        if np.any(s1) or np.any(s2):
            kappa_scores[idx] = cohen_kappa_score(s1, s2)
            dico[_class] = kappa_scores[idx]

    return dico#kappa_scores, kp_score_all


def merge_true_pred(ix):
    lame = l[ix].split('.')[0].strip()
    fr_lame = pd.read_csv(f'{annot_fr}output_1/ {lame} .txt')
    qp_lame = pd.read_csv(f'{annot_qp}{lame}.csv')
    print(f'==> qp shape : {qp_lame.shape}\n==> francois shape : {fr_lame.shape}\n==> lame : {lame}')
    temp = []
    for i in fr_lame['tile']:
        nb = i.split(' ')[1].strip()
        tile = f'{lame}_{nb}'
        temp.append(tile)
    fr_lame['tile'] = temp
    fr_lame.rename(columns={'class':'classPath_fr', 'tile':'tuile'}, inplace=True)
    fr_lame.dropna(inplace=True)
    print('shape fr_lame after preprocessing : ',fr_lame.shape)
    print(f'number of class : {fr_lame["classPath_fr"].value_counts().shape[0]}')
    #print(fr_lame['classPath_fr'].value_counts())

    merge = pd.merge(fr_lame, qp_lame, on='tuile')

    return merge

def kappa_compute(merge):
    annot_dict = {
        'classe1':'normal',
        'classe2':'normal',
        'classe3':'Stroma',
        'classe4':'Stroma',
        'classe5':'Tumor',
        'classe6':'Tumor',
        'classe7':'duodenum',
        'classe8':'duodenum',
    }
    merge['classPath']=merge['classPath'].map(annot_dict)
    annotator_fr = merge['classPath_fr'].values
    annotator_qp = merge['classPath'].values
    kappa_scores = class_wise_kappa(annotator_fr, annotator_qp, n_classes=None, ignore_zero=True)
    return kappa_scores


if __name__ == '__main__':
    kappa_result = dict()
    for i in range(len(l)):
        print(l[i])
        merge = merge_true_pred(i)
        _kappa= kappa_compute(merge)
        kappa_result[l[i]] = _kappa
        print(_kappa)
        print('-'*50)

    with open(f'{annot_fr}kappa_result.txt', 'w') as convert_file:
     convert_file.write(json.dumps(str(kappa_result)))

    result = pd.DataFrame(index=l, columns=['s', 't', 'd', 'n'])
    for ind in l:
        try:
            result.loc[ind,'s'] = kappa_result[ind]['Stroma']
        except:
            pass
        try:
            result.loc[ind,'t'] = kappa_result[ind]['Tumor']
        except:
            pass
        try:
            result.loc[ind,'d'] = kappa_result[ind]['duodenum']
        except:
            pass
        try:
            result.loc[ind,'n'] = kappa_result[ind]['normal']
        except:
            pass


    for class in result.columns:
        result[class]=result[class].astype(float)

    result.reset_index(inplace=True)

    result.to_csv(f'{annot_fr}Kappa_qupath_fr_bsc_lames.csv', index=False)


    result.plot(x='index', y=['s','t','d','n'], kind='bar', figsize=(17,7))
    plt.ylabel('$Kappa score$')
    plt.grid(True)
    plt.xticks(rotation = 45)
    plt.title('Concordance $Qupath$ _ $François$ annotations Lame Besançon')
    plt.savefig(f'{annot_fr}Kappa_qupath_fr_bsc_lames.png')



    
