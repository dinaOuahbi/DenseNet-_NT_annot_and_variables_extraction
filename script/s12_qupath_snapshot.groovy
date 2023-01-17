
// importations
import qupath.lib.roi.ROIs
import qupath.lib.regions.ImagePlane
import java.io.BufferedReader;
import java.io.FileReader;
import qupath.lib.objects.PathAnnotationObject;
import qupath.lib.roi.RectangleROI;
import qupath.lib.roi.*
import qupath.lib.objects.*
import qupath.lib.gui.measure.ObservableMeasurementTableData
import qupath.lib.geom.Point2
import qupath.lib.gui.images.servers.RenderedImageServer
import qupath.lib.gui.viewer.overlays.HierarchyOverlay


// get selected image and server
def imageData = getCurrentImageData()
def server = getCurrentServer()

// get the image name and cut it into short name 
def name =  GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
shortname = name[0..14]
print shortname
slide = "/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/QPdata_withduodenum/"+shortname+"/"
///Image export///
fireHierarchyUpdate()    
    
selectAnnotations()
def viewer = getCurrentViewer()   
def options = viewer.getOverlayOptions()
options.setFillDetections(true)
    
def viewer2 = getCurrentViewer()
def imageData2 = getCurrentImageData()
def downsample = 100
       
// Create a rendered server that includes a hierarchy overlay using the current display settings       
def server2 = new RenderedImageServer.Builder(imageData2)
    .downsamples(downsample)
    .layers(new HierarchyOverlay(viewer2.getImageRegionStore(), viewer2.getOverlayOptions(), imageData2))
    .build()
       
      
def region = RegionRequest.createInstance(server2, downsample)
def outputPath = buildFilePath(slide+shortname+"_org.tif")
writeImageRegion(server2, region, outputPath)

/*
def poscell = getCurrentImageData()
def poscellqpdata = new File(slide+shortname+".qpdata")
qupath.lib.io.PathIO.writeImageData(poscellqpdata, poscell);
print 'Ready for positive cells detection script!'
*/

