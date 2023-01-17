guiscript=true
slide = new File("/work/shared/ptbc/CNN_Pancreas_V2/Donnees/SCAN 21_0_005_00/").listFiles()
for(s in slide) {
    clearAllObjects()
    try {
    QuPathGUI.getInstance().openImage(s.toString(), false, false)
    shortname = s.toString().split("/")[-1].split(" ")[0]
    imageData = QuPathGUI.getInstance().getViewer().getImageData()
    setBatchImageData(imageData)
    server = QuPathGUI.getInstance().getViewer().getServer()


// get the image name and cut it into short name 
    //qupath.lib.io.PathIO.readImageData(new File("/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/"+shortname+"/"+shortname+"_tiles.qpdata"), getCurrentImageData(), getCurrentServer(), BufferedImage.class) 
    importObjectsFromFile("/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles/"+shortname+"/"+shortname+"_tiles.qpdata")
    // Save qpadata of this //
    new File('/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles2/'+shortname).mkdirs()
    img1 = imageData
    qpdata1 = new File('/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/scan_tiles2/'+shortname+'/'+shortname+'.qpdata')
    qupath.lib.io.PathIO.writeImageData(qpdata1, img1)
    } catch(Exception e) {
        continue
    }
}