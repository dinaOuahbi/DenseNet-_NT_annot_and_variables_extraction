# python3

# DO

import pandas as pd
import os
import re
import numpy as np
from shapely.geometry import Polygon, Point
from PIL import Image

# read slides
myData = "/work/shared/ptbc/Dina/test_project/datas/"  # to change
mySlide = os.listdir(f"{myData}Annotation_TCGA/")


def select_tiles_3classes(slide_num):
    # read annotations
    list_files = os.listdir(
        f"/work/shared/ptbc/Dina/test_project/datas/Annotation_TCGA/{mySlide[slide_num]}/Annotation/"
    )

    list_files_tumor = [l for l in list_files if "Tumor" in l]
    list_files_other = [l for l in list_files if "Stroma" in l]
    list_files_duodenum = [l for l in list_files if "Duodenum" in l]
    list_files_normal = [l for l in list_files if "normal" in l]

    # load into a list coord XY file
    tile_points = pd.read_csv(
        f"{myData}TCGA_tiles/{mySlide[slide_num]}/{mySlide[slide_num]}_tileXY.txt",
        sep="\t",
    )

    print("read annotations DONE")
    ##############################################################################

    # select point 1
    tile_points["Point1"] = None
    temp = []
    for i in tile_points["Tile-Point"]:
        if "Point1" in i:
            temp.append(i)
        else:
            temp.append(np.nan)

    tile_points["Point1"] = temp

    # verify nan
    tile_points.isna().sum()

    # drop nan
    tile_points = tile_points.dropna().drop("Tile-Point", axis=1)

    # select tiles <number>
    temp = []
    for i in tile_points["Point1"]:
        temp.append(i.split(" ")[0])
    tile_points["Point1"] = temp

    # remove 'Tile'
    temp = []
    for i in tile_points["Point1"]:
        temp.append(i.replace("Tile", ""))
    tile_points["Point1"] = temp

    # rename col
    tile_points.rename(columns={"Point1": "Tile.Point"}, inplace=True)

    # concatenate 'tile number' with 'slide code'
    temp = []
    for i in tile_points["Tile.Point"]:
        temp.append(f"{mySlide[slide_num]}_{i}.tif")
    tile_points["Tile.Point"] = temp

    print("select point1 DONE")
    ##############################################################################

    # search for centroid
    tile_dim, temp = 402, []
    for x in tile_points["x"]:
        temp.append(x + (tile_dim / 2))
    tile_points["centroidX"] = temp
    temp.clear()
    for y in tile_points["y"]:
        temp.append(y + (tile_dim / 2))
    tile_points["centroidY"] = temp

    # list normalised tiles for one slide
    tiles_list = os.listdir(f"{myData}/TCGA_reinhard/{mySlide[slide_num]}/")

    # reset index to be able to enume
    tile_points.reset_index(drop=True, inplace=True)

    # drop tile.point which doeos't exist in normalised tiles list
    for i, tp in enumerate(tile_points["Tile.Point"]):
        if tp not in tiles_list:
            tile_points.drop(i, axis=0, inplace=True)

    print("looking for centroid DONE")
    ##############################################################################
    # create a polygone and check if point is inside it
    def point_in_polygon(classe, cx, cy) -> bool:
        coords = []
        for i in range(classe.shape[0]):
            coords.append((classe["x"].iloc[i], classe["y"].iloc[i]))
        poly = Polygon(coords)
        p = Point(cx, cy)
        return p.within(poly)

    for class_data in [
        list_files_tumor,
        list_files_other,
        list_files_duodenum,
        list_files_normal,
    ]:
        tiles = []
        for myFile_class in class_data:
            classe = pd.read_csv(
                f"{myData}Annotation_TCGA/{mySlide[slide_num]}/Annotation/{myFile_class}"
            )
            print(classe.shape[0])
            for i in range(tile_points.shape[0]):
                if point_in_polygon(
                    classe, tile_points.iloc[i, 4], tile_points.iloc[i, 5]
                ):  # if centroids inside polygone
                    tiles.append(tile_points.iloc[i, 3])  # recuperer la tuile
        try:
            os.mkdir(f"{myData}TCGA_annot_3classes/{class_data}/")
        except:
            pass
        for tile in tiles:
            img = Image.open(f"{myData}/TCGA_reinhard/{mySlide[slide_num]}/{tile}")
            img.save(f"{myData}TCGA_annot_3classes/{class_data}/{tile}")

        print(f"{class_data} DONE")


if __name__ == "__main__":
    """
    for each slide we select differents classe inside a specific folders
    """
    for slide_num in range(len(mySlide)):
        select_tiles_3classes(slide_num)
