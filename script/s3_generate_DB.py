# python 3

# DO

# obj : create database to use in modeling (trainset, testset, valset)

import pandas as pd
import numpy as np
import re
import os
import collections
import random as rd
import shutil

"""
Script permettant de creer 3 bases de données

- DB3 : 3 classes permettant d'entrainer un modele a trois classes si jamais
- DB4 : Stroma vs Normal/Tumeur permettant d'entrainer le modele emboite partie 1
- DB5 : Normal vs Tumeur permettant d'entrainer le modele emboite partie 2

Chaque base est divise en sous DB train, val et test

    INPUT
        TCGA_annot_3classes/{tumor, other, normal, duo}
    OUTPUT
        TCGA annot DB
            Train
                c1
                c2
                cn
            Test
                c1
                c2
                cn
            Val
                c1
                c2
                cn


"""

# always define input and output pathway
INPUT = "/work/shared/ptbc/CNN_Pancreas_V2/Donnees/"
OUTPUT = "/work/shared/ptbc/Dina/data/"

# remove duplications / comparing two lists
def remove_dup(mylist):
    dups = [item for item, count in collections.Counter(mylist).items() if count > 1]
    if len(dups) != 0:
        print(f"This list has {len(dups)} duplications")
        for dup in dups:
            mylist.remove(dup)
        print("DONE ! ")
    else:
        print("No dups")


def set_diff(mylist1, mylist2) -> list:
    """
    return a list of differences between two target lists
    """
    diff = []
    for s in mylist1:
        if s not in mylist2:
            diff.append(s)
    return diff


def load_class_file(class_path):
    slides = os.listdir(f"{INPUT}Annotation_TCGA/")  # input
    p, temp = [], []
    myClass = os.listdir(class_path)  # input
    myClass = pd.DataFrame(myClass).rename(columns={0: "patient_tile"})
    for i in myClass["patient_tile"]:
        p.append(i[0:16])
    myClass["patient"] = p
    print("PATIENT LENGHT : {}".format(len(myClass["patient"].unique())))
    ###
    for i in slides:
        temp.append(i.split(".")[0][0:16])
    slides = temp
    ###
    remove_dup(myClass["patient"].unique())
    remove_dup(slides)
    ###
    return myClass


def create_files(OUTPUT):
    try:
        os.mkdir(f"{OUTPUT}TCGA_annot_DB/")
        for i in ["Train", "Test", "Val"]:
            os.mkdir(f"{OUTPUT}TCGA_annot_DB/{i}")
            os.mkdir(f"{OUTPUT}TCGA_annot_DB/{i}/Tumor")
            os.mkdir(f"{OUTPUT}TCGA_annot_DB/{i}/Other")
            os.mkdir(f"{OUTPUT}TCGA_annot_DB/{i}/Normal")
            os.mkdir(f"{OUTPUT}TCGA_annot_DB/{i}/Duodenum")

    except FileExistsError as err:
        print(err)
        pass


def generat_sets(class_name, class_df):
    cpt = 0
    myDict = {"Train": train_patient, "Test": test_patient, "Val": val_patient}

    for key, val in myDict.items():
        files_patient = []
        for txt in class_df["patient_tile"]:
            for p in val:  # unique patient
                if re.search(p, txt):
                    files_patient.append(txt)

                for myfile in files_patient:
                    ORG = f"{INPUT}TCGA_annot_3classes/{class_name}/{myfile}"
                    TARGET = f"{OUTPUT}TCGA_annot_DB/{key}/{class_name}/{myfile}"
                    shutil.copyfile(ORG, TARGET)


# main
if __name__ == "__main__":
    classes_path = {
        "Tumor": f"{INPUT}TCGA_annot_3classes/Tumor",
        "Other": f"{INPUT}TCGA_annot_3classes/Other",
        "Normal": f"{INPUT}TCGA_annot_3classes/Normal",
        "Duodenum": f"{INPUT}TCGA_annot_3classes/Duodenum",
    }

    #  LOAD DATASETS
    Tumor = load_class_file(classes_path["Tumor"])
    Other = load_class_file(classes_path["Other"])
    Normal = load_class_file(classes_path["Normal"])
    Duodenum = load_class_file(classes_path["Duodenum"])

    # REPARTITION OF DATA
    train_patient = rd.sample(
        list(Tumor["patient"].unique()), len(Tumor["patient"].unique()) * 3 // 5
    )
    autre_patient = [p for p in Tumor["patient"].unique() if p not in train_patient]
    test_patient = rd.sample(autre_patient, len(autre_patient) * 1 // 2)
    val_patient = [p for p in autre_patient if p not in test_patient]

    print(len(train_patient), len(test_patient), len(val_patient))

    # CREATE FOLDERS OUTPUT
    create_files(OUTPUT)

    classes = {"Tumor": Tumor, "Other": Other, "Normal": Normal, "Duodenum": Duodenum}
    for class_name, class_df in classes.items():
        print(f"===========> {class_name} <===========")
        generat_sets(class_name, class_df)
