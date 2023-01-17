#!/usr/bin/env python3.7
########################################################### project_kernel03_scan21000500/ ################################
########################################################### besancon slides (n=241) #######################################
import getopt
import numpy as np
import keras
import sys
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img, save_img
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image
import os
import pandas as pd
from random import *
import re
import seaborn as sns
import math
import tensorflow as tf
import shutil
import PIL

############ temp
#w = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/SCAN_reinhard/'
#a = '/archive/shared/ptbc/CNN_Pancreas_V2/zip_scan_reinhard/'
#w = os.listdir(w)
#a = os.listdir(a)
#w.extend(a)


arg = sys.argv[1] # recuperer l'option 1
'''if arg in w:
    print('DONE !')
    sys.exit()'''
# define your data folder
#myData = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/'
myData = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/CNN_REP_PROG_bscdata/'

def reinhard_normalization(arg):
    #os.mkdir(f'{myData}SCAN_reinhard/drop_{arg}')
    #os.mkdir(f'{myData}SCAN_reinhard/{arg}')
    #shutil.rmtree(f'{myData}SCAN_reinhard/{arg}'
    root_input = f'{myData}tiles/{arg}/Images_{arg}'
    for root, dirs, files in os.walk(root_input):
        print(root) # slide path
        for file in files:
            print(file) #tile
            if (file.endswith(".tif")):
                print('OK')
                # load target image
                img = load_img(f'{myData}target.tif',target_size=(402, 402))
                img = img_to_array(img)
                img = img.astype(np.uint8)
                LAB = img/255
                Mu = LAB.sum(axis=0).sum(axis=0) / (LAB.size / 3) # mean
                LAB[:, :, 0] = LAB[:, :, 0] - Mu[0]
                LAB[:, :, 1] = LAB[:, :, 1] - Mu[1]
                LAB[:, :, 2] = LAB[:, :, 2] - Mu[2]
                Sigma = ((LAB * LAB).sum(axis=0).sum(axis=0) / (LAB.size / 3 - 1)) ** 0.5 # std
                target_mu = Mu
                target_sigma = Sigma

                # On charge l'image que l'on souhaite normaliser
                img_scr = load_img(os.path.join(root_input, file),target_size=(402, 402))

                # get input image dimensions
                m = 402
                n = 402
                img_scr = img_to_array(img_scr)
                img_scr = img_scr.astype(np.uint8)
                compteur = 0

                   # Reperage des images blanches
                for i in range(402):# for each pixel col
                    for j in range(402):  # for each pixel row
                        if(img_scr[i,j,0]>210 and img_scr[i,j,1]>210 and img_scr[i,j,2]>210): # px>210 for all layer (rgb)
                            compteur += 1

                if (compteur > 2*402*402/3): #si l'image contient 2/3 de blanc (gris clair)
                    #root_output = f'{myData}SCAN_reinhard/drop/'
                    continue
                else :
                    root_output = f'{myData}SCAN_reinhard/{arg}'
                im_lab = img_scr/255

                # Normalisation
                src_mu = None
                src_sigma = None
                    # calculate src_mu if not provided
                if src_mu is None:
                    src_mu = im_lab.sum(axis=0).sum(axis=0) / (m * n)
                   # center to zero-mean
                for i in range(3):
                    im_lab[:, :, i] = im_lab[:, :, i] - src_mu[i]
                   # calculate src_sigma if not provided
                if src_sigma is None:
                    src_sigma = ((im_lab * im_lab).sum(axis=0).sum(axis=0) / (m * n - 1)) ** 0.5
                   # scale to unit variance
                for i in range(3):
                    im_lab[:, :, i] = im_lab[:, :, i] / src_sigma[i]
                   # rescale and recenter to match target statistics
                for i in range(3):
                    im_lab[:, :, i] = im_lab[:, :, i] * target_sigma[i] + target_mu[i]
                im_lab[im_lab > 1] = 1
                im_lab[im_lab < 0] = 0
                im_normalized = im_lab * 255
                   #im_normalized = im_normalized.astype(np.uint8)
                im_normalized_image = array_to_img(im_normalized)
                save_img(os.path.join(root_output, file),im_normalized_image)
                #os.remove(os.path.join(root_input, file)) # pour ne pas avoir trop de fichiers on supprime les images brutes




# MAIN
if __name__ == '__main__':
    print(f'ARGUMENTS : {arg}')
    reinhard_normalization(arg)
