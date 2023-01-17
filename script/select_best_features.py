#!/usr/bin/env python3.7

"""
# ---------------------------------------------
# Programme: DenseNet.py
# Auteur OD
# Date 15/11/2021
#
# Prediction a partir du CNN permettant la classification
# des tuiles Tumorales vs Autres
# -------------------------------------------------------------
"""

# On importe tous les modules dont on a besoin
import warnings
import time
import tensorflow as tf
import progressbar
from tensorflow.keras import datasets, layers, models
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from keras import optimizers
from tensorflow.keras.utils import to_categorical
import keras.backend as K
import numpy as np
import os
import pandas as pd
import sys
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
import math
from keras.callbacks import ReduceLROnPlateau
from keras.applications.inception_v3 import InceptionV3
from sklearn.utils import class_weight
import pathlib
import functools
from keras.utils import np_utils
from tensorflow.keras.losses import CategoricalCrossentropy
from keras.preprocessing.image import ImageDataGenerator
import time
import sys
from datetime import datetime
#####################################################################


slide = sys.argv[1] # recuperer l'option 1

SCNN = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/'
OUTPUT = f'{SCNN}Features/NvsT_densenet/' # to CHANGE
INPUT=f'{SCNN}N_Tselect/'

if f'Features_{slide}.csv' in os.listdir(OUTPUT):
    os.exit()

#MODELS
NvsT_densenet = tf.keras.models.load_model('/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/NvsT_densenet', compile = False)
StromaVSautre_densenet = tf.keras.models.load_model('/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/StromaVSautre_densenet', compile = False)
test_datagen = ImageDataGenerator()
batch_size = 32

# MODEL TO SPECIFY
myModel = NvsT_densenet   #to CHANGE

def select_features(slide):
    BSC_generator = test_datagen.flow_from_directory(
        directory=INPUT, classes = [slide],
        target_size =(402, 402),
        batch_size=batch_size,
        shuffle=False,
        seed=42
    )
    tile_names = BSC_generator.filenames # out e.g : Found 21330 images belonging to 1 classes

    intermediate_layer_model = Model(inputs = myModel.input, outputs = myModel.get_layer("global_average_pooling2d").output)
    intermediate_output = intermediate_layer_model.predict(BSC_generator)
    myPrediction = intermediate_output
    myPrediction = pd.DataFrame(myPrediction, index = tile_names)
    myPrediction.to_csv(f'{OUTPUT}/Features_{slide}.csv', sep=',', encoding='utf-8',index=True, header = None)

# Main
if __name__ == '__main__':
    print(f'New ARGUMENTS : {slide}')
    select_features(slide)
