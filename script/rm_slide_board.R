#!/usr/bin/env Rscript

#L'objectif est de créer un polygone qui fait le tour de la lame selon une épaisseur donnée (ici 1000 pixels), 
#ensuite on enlève toutes les tuiles contenues dans ce polygone.
#Pour cela, il te faut les coordonnées de chaque tuile créées dans la tuile : 
#dans le code ce fichier s'appelle "polygons" et un fichier qui répertorie les centroides de chaque 
#tuile afin de pouvoir tester si la tuile est dans le polygone créé : dans le code le fichier s'appelle "centroids". 

slides = list.files(path = "/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/")


#arg <- commandArgs(trailingOnly = TRUE) 
library(rgeos)
for (arg in slides) {
  print(arg)
  root = paste0('/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/',arg,'/')
  # charger les coordonnees et les polygons
  
  polygons = read.csv(paste0(root,arg,'_tileXY.csv'), sep='\t')
  centroid = read.csv(paste0(root,arg,'_centroid.csv'))
  
  # Creation of a polygons on the edge of the lame and with a width of 1000 pixels :
  min_x = as.numeric(min(polygons[,2]))
  max_x = as.numeric(max(polygons[,2]))
  min_y = as.numeric(min(polygons[,3]))
  max_y = as.numeric(max(polygons[,3]))
  length_x = max_x - min_x
  length_y = max_y - min_y
  
  coord_bord = data.frame("X" = c(c(min_x:max_x), rep(max_x,length_y), sort(c(min_x:max_x),decreasing = T), rep(min_x,length_y)),
                          "Y" = c(rep(min_y,length_x), c(min_y:max_y), rep(max_y,length_x), sort(c(min_y:max_y),decreasing = T)))
  coord_bord$X = as.numeric(coord_bord$X)
  coord_bord$Y = as.numeric(coord_bord$Y)
  
  coef = 1500 # nb de px a ignoré
  min_x_hole = min_x+coef ; max_x_hole = max_x-coef
  min_y_hole = min_y+coef; max_y_hole = max_y-coef
  length_x_hole = max_x_hole - min_x_hole
  length_y_hole = max_y_hole - min_y_hole
  
  coord_bord_hole = data.frame("X" = c(c(min_x_hole:max_x_hole), rep(max_x_hole,length_y_hole), sort(c(min_x_hole:max_x_hole),decreasing = T), rep(min_x_hole,length_y_hole)),
                               "Y" = c(rep(min_y_hole,length_x_hole), c(min_y_hole:max_y_hole), rep(max_y_hole,length_x_hole), sort(c(min_y_hole:max_y_hole),decreasing = T)))
  coord_bord_hole$X = as.numeric(coord_bord_hole$X)
  coord_bord_hole$Y = as.numeric(coord_bord_hole$Y)
  
  p1 = Polygon(coords = coord_bord)
  p2 = Polygon(coords = coord_bord_hole, hole=T)
  P1 = Polygons(list(p1,p2), ID="p1")
  pol = SpatialPolygons(list(P1))
  # pol est le polygone qui longe les bords de la lame
  
  # Test of tiles centroids belong to the polygons edge :
  coord_centroid = data.frame("X" = as.numeric(centroid[,2]), "Y" = as.numeric(centroid[,3]))
  coord_spatial = SpatialPoints(coord_centroid)
  contains = gContains(pol, coord_spatial, byid=T)
  
  plot(pol, boder="green")
  plot(coord_spatial, add=T)
  # contains est un vecteur qui a pour taille le nombre de tuiles dans la lame et qui est TRUE si 
  #la tuile est sur le bord de la lame et FALSE sinon.
  write.csv(contains,paste0(root,arg,'_contains.csv'), row.names = TRUE)
}
