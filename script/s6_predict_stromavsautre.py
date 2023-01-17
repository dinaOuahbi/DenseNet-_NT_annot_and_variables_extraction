#!/usr/bin/env python3.7
# -*-coding:Latin-1 -*

"""
# ---------------------------------------------
# Programme: predict_stromavsautre
# Auteur EB
# MODIF DO
# CREATE 15/11/2021
# EDITE 08/04/2022
# Prediction a partir du CNN permettant la classification
# des tuiles Stromales vs Normales/Tumorales
# -------------------------------------------------------------
"""

# On importe tous les modules dont on a besoin
import tensorflow as tf
import numpy as np
import os,sys,math
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator

def predict_with_densenet(slide):
    """
    this function generate test data from input slides, use 32 batch size, and return predictions of each
    tile (in format csv) using densenet model
    """
    # CREATION D'un generqteur de donnee
    test_datagen = ImageDataGenerator()

    batch_size = 32
    # Générateurs

    BSC_generator = test_datagen.flow_from_directory(
        directory=INPUT,
        classes=[slide],
        target_size=(402, 402),
        batch_size=batch_size,
        shuffle=False,
        seed=42,
    )
    # out : Found 21330 images belonging to 1 classes

    tile_names = BSC_generator.filenames
    # On va enregistrer la matrice qui contient les probabilités
    test_predictions_baseline = model.predict(BSC_generator)
    myPrediction = test_predictions_baseline
    myPrediction = pd.DataFrame(myPrediction, index=tile_names)
    myPrediction.to_csv(
        f"{OUTPUT}{slide}.csv", sep=",", encoding="utf-8", index=True, header=None
    )


if __name__ == "__main__":
    slide = sys.argv[1]
    PROJECT = "/work/shared/ptbc/CNN_Pancreas_V2/"
    OUTPUT = f"{PROJECT}results/CP/macenko_prog_rep/Predictions_normalVStumor/" # Predictions_normalVStumor #Predictions_StromaVSautre
    INPUT = f"{PROJECT}database/canceropol/NT_tiles/" #NT_tiles #macenko
    #StromaVSautre_densenet
    #NvsT_densenet
    model = tf.keras.models.load_model(
        "/work/shared/ptbc/CNN_Pancreas_V2/Analyses_stat/Resultats/StromaVSautre_DB10/NvsT_densenet",
        compile=False,
    )

    predict_with_densenet(slide)
