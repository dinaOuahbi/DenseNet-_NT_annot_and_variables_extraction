#!/bin/bash

eval slide=$1

python /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/script/reinhard.py $slide






#for slide in `ls /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/`
#do
#  echo $slide
#  qsub -q batch script/rein.sh $slide
#done
