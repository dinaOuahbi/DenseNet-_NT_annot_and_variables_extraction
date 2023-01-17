#!/usr/bin/env python3.7

"""
# ---------------------------------------------
# Programme: DenseNet.py
# Auteur EB
# Date 15/11/2021
#
# Prediction a partir du CNN permettant la classification
# des tuiles Tumorales vs Autres
# -------------------------------------------------------------
"""

# On importe tous les modules dont on a besoin
import warnings
import PIL
import time
import tensorflow as tf
import progressbar
from tensorflow.keras import datasets, layers, models
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
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
from datetime import datetime

#####################################################################
slide = sys.argv[1]  # recuperer l'option 1

SCNN = "/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/"
OUTPUT = f"{SCNN}TumorVSNormal/"

"""if f'{slide}.csv' in os.listdir(OUTPUT):
    print('DONE !')
    sys.exit()
else:
    #slide=slide.split('_', 1)[1].split('.')[0]
    print(f'New ARGUMENTS : {slide}\n lets do the prediction !')"""

INPUT = f"{SCNN}N_Tselect/"
feature_path = f"{SCNN}Features/"
NvsT_densenet = tf.keras.models.load_model(
    "/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/NvsT_densenet",
    compile=False,
)
StromaVSautre_densenet = tf.keras.models.load_model(
    "/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/StromaVSautre_densenet",
    compile=False,
)
test_datagen = ImageDataGenerator()
batch_size = 32


"""try:
    os.mkdir(OUTPUT)
except FileExistsError as err:
    print(err)
    pass

try:
    os.mkdir(feature_path)
except FileExistsError as err:
    print(err)
    pass"""


def predict(slide, model):
    """
    predictions (normal vs tumor)
    """
    print(f"slide prediction  .............: {slide}")  #
    # Générateurs
    BSC_generator = test_datagen.flow_from_directory(
        directory=INPUT,
        classes=[slide],
        target_size=(402, 402),
        batch_size=batch_size,
        shuffle=False,
        seed=42,
    )
    tile_names = (
        BSC_generator.filenames
    )  # out e.g : Found 21330 images belonging to 1 classes

    # On va enregistrer la matrice qui contient les probabilités

    test_predictions_baseline = model.predict(BSC_generator)
    myPrediction = test_predictions_baseline
    myPrediction = pd.DataFrame(myPrediction, index=tile_names)
    myPrediction.to_csv(
        f"{OUTPUT}{slide}.csv", sep=",", encoding="utf-8", index=True, header=None
    )

    ###############


# Main
if __name__ == "__main__":
    predict(slide=slide, model=NvsT_densenet)
    # predict(slide=slide, model = NvsT_densenet, model_list=[StromaVSautre_densenet], name_l=['StromaVSautre_densenet'])
