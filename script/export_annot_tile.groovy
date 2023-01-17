// Based on Pete's scripts here: https://qupath.readthedocs.io/en/latest/docs/advanced/exporting_images.html#images-regions
// Get the current image (supports 'Run for project')
def imageData = getCurrentImageData()

def server = getCurrentServer()
// Define output path (here, relative to project)
def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
/*******************
CHANGE THIS
*******************/
def pathOutput = "/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/lame francois/tiles/"

i=1
for (tile in getDetectionObjects()){
    def requestFull = RegionRequest.createInstance(server.getPath(),1,tile.getROI())
    x = tile.getROI().getCentroidX()
    y = tile.getROI().getCentroidY()
    tileClass = tile.getParent().toString()[22..28]
    fileName = pathOutput+name+"_x_"+x+"_y_"+y+"_"+tileClass+"_"+(i++)+".tif"
    //print describe(requestFull)
}