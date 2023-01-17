# Python 3.7.9 :: Intel Corporation
# DO
# 2022
# scipt : load coordination XY of tiles ==> compute centroide of tile ==> filter those tiles inside border

# whene centroids are computed, you have to generate contains (before filtring) with R script : /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/script/rm_slide_board.R

# importations
import pandas as pd
import os
import numpy as np
slides = os.listdir('/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/') # list of slides
len(slides) # check how much slides
def centroid(*points):
    '''
    inpurt : x, y of each point of tile (4 in total)
    output : centroid
    '''
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]

for arg in slides:
    print(arg)
    inp = f'/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/{arg}/'
    coord = f'{inp}{arg}_tileXY.txt'
    try:
        read_file = pd.read_csv (coord)
    except FileNotFoundError:
        print(f'no such file {arg}')
        pass
    # convert txt to csv
    read_file.to_csv (f'{inp}{arg}_tileXY.csv', index=None)

    co = pd.read_csv(f'{inp}{arg}_tileXY.csv', sep='\t')

    x = co['x'].to_list()
    y = co['y'].to_list()

    temp = []
    for row in co['Tile-Point']:
        temp.append(row.split(' ')[0])
    my_tiles = list(dict.fromkeys(temp))
    c_df = pd.DataFrame(index = my_tiles, columns=['c_x', 'c_y'])

    c_x_list, c_y_list = [], []
    i = 0
    while i<=co.shape[0]-4:
        temp = []
        temp = centroid((x[i], y[i]), (x[i+1], y[i+1]), (x[i+2], y[i+2]), (x[i+3], y[i+3]))
        i = i+4
        c_x_list.append(temp[0])
        c_y_list.append(temp[1])
    c_df['c_x'] = c_x_list
    c_df['c_y'] = c_y_list

    c_df.to_csv(f'{inp}{arg}_centroid.csv')


## R script to generate contains of polygone
        ## /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/script/rm_slide_board.R

### classify tile depending on if it's belongue polygon (boarder) or not
output = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/CombModels_BSC_prediction_without_border/'
for arg in slides:
    print(arg)
    inp = f'/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/{arg}/'
    contains = pd.read_csv(f'{inp}{arg}_contains.csv')
    contains.rename(columns={'Unnamed: 0':'tuile', 'p1':'if_board'}, inplace=True)
    temp = []
    for i in contains['tuile']:
        temp.append(f'{arg}_{i}')
    contains['tuile'] = temp
    try:
        annot = pd.read_csv(f'/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/CombModels_BSC_prediction/{arg}.csv')
    except FileNotFoundError:
        print(f'no such file {arg}')
        pass
    merge_df = pd.merge(contains, annot, on='tuile')
    for i in range(merge_df.shape[0]):
        if merge_df.loc[i, 'if_board']:
            merge_df.iloc[i, 2] = 'nan'
    merge_df.drop('if_board', axis=1, inplace=True)
    merge_df.fillna('nan', inplace=True)
    merge_df.to_csv(f'{output}{arg}.csv', index=False)
