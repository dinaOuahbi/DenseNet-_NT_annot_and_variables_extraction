# python 3
# DO
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats as st
import sys

N_T_preds = '/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/LamesCompletes/Normal_Tumeur/'
features_path = '/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/LamesCompletes/Features/'
out = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/Features/TCGA_pooling_features/'
###################################################### functions
def df_operation(df, operation):
    if operation == 'sum':
        res = [df[i].sum() for i in df.set_index(0)]
    elif operation == 'mean':
        res = [df[i].mean() for i in df.set_index(0)]
    elif operation == 'max':
        res = [df[i].max() for i in df.set_index(0)]
    return res

# LOAD PRED CNN2
def select_tiles(arg):
    preds = pd.read_csv(f'{N_T_preds}{arg}.csv').T.reset_index(drop=True).T.set_index(0)
    print(f'BEFORE SELECT ==> {preds.shape}')
    res = list()
    for i in preds.index:
        if np.argmax(preds.loc[i,:]) == 0:
            res.append('Normal')
        elif np.argmax(preds.loc[i,:]) == 1:
            res.append('Tumor')
    preds['pred_class'] = res
    # SELECT ONLY TUMOR TILES
    predsT = preds[preds['pred_class'] == 'Tumor']
    # SELECT ONLY TUMOR WITH PROBA SUP 80
    predsT_80 = predsT[predsT[2]>0.80]
    print(f'AFTER SELECT ==> {predsT_80.shape}')
    # reset index to merge after
    predsT_80.reset_index(inplace=True)
    # LOAD FEATURE
    arg = arg.split('_')[1]
    features = pd.read_csv(f'{features_path}Features_{arg}.csv').T.reset_index(drop=True).T
    #MERGE
    my_Table = pd.merge(predsT_80[[0]], features, on = 0)
    return my_Table


#" MAIN "
if __name__ == '__main__':
    path = sys.argv[1] # get a path of slides folder
    choice = sys.argv[2] # get choice ['all' | 'select']
    my_args = [os.path.splitext(i)[0] for i in os.listdir(path)] #enlever les extension
    # OPERATION ON ENTIRE TILES
    if choice == 'all':
        sum_tiles, mean_tiles, max_tiles = [pd.DataFrame() for i in range(3)]
        for arg in my_args:
            print(f'=====> {arg} <=====')
            df = pd.read_csv(f'{features_path}Features_{arg}.csv').T.reset_index(drop=True).T
            sum_tiles[arg] = df_operation(df, 'sum')
            mean_tiles[arg] = df_operation(df, 'mean')
            max_tiles[arg] = df_operation(df, 'max')
        sum_tiles.T.to_csv(f'{out}sum_variable_tiles.csv')
        mean_tiles.T.to_csv(f'{out}mean_variable_tiles.csv')
        max_tiles.T.to_csv(f'{out}max_variable_tiles.csv')

    # OPERATION ON SELECTED TILES
    if choice == 'select':
        sum_tiles_80, mean_tiles_80, max_tiles_80 = [pd.DataFrame() for i in range(3)]
        for arg in my_args:
            print(f'=====> {arg} <=====')
            df = select_tiles(arg)
            sum_tiles_80[arg] = df_operation(df, 'sum')
            mean_tiles_80[arg] = df_operation(df, 'mean')
            max_tiles_80[arg] = df_operation(df, 'max')
        sum_tiles_80.T.to_csv(f'{out}sum_variable_tiles_T80.csv')
        mean_tiles_80.T.to_csv(f'{out}mean_variable_tiles_T80.csv')
        max_tiles_80.T.to_csv(f'{out}max_variable_tiles_T80.csv')
