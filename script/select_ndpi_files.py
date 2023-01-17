# python 3

# DO

import re
import os
import shutil

# files than were passed inside qupath
done = os.listdir('/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/')

# source
org_root = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/SCAN 21_0_005_00/SCAN 21_0_005_00/'

# origin folder
org = os.listdir('/work/shared/ptbc/CNN_Pancreas_V2/Donnees/SCAN 21_0_005_00/SCAN 21_0_005_00')

# select only tiles code and remove white space
org_list = []
for slide in org:
    org_list.append(slide.split('-')[0].strip())


# add interesting files
diff = []
for d in org_list:
    if d not in done:
        diff.append(d)


# select right slides
myslides = []
for slide in org:
    for mydiff in diff:
        if re.search(mydiff, slide):
            myslides.append(slide)


# copy ndpi files
for file in org:
    source = f'{org_root}{file}'
    destination = f'/work/shared/ptbc/CNN_Pancreas_V2/Donnees/SCAN 21_0_005_00/SCAN_rest/{file}'
    shutil.copyfile(source, destination)
