// get the image server
import qupath.lib.gui.images.servers.RenderedImageServer

BSC_TILES = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_krenek03/test_qpath/'

// Get slide name & create a folder to put results in it //
def imageData = getCurrentImageData()
def server = getCurrentServer()
def name =  GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
print name
// def newname = name.replace("_", " ")
newname = name
print newname
def words = newname.split(" ")
def filename = words[0]
def path = BSC_TILES+filename
File dir= new File(path);
dir.mkdir();
def path_img = BSC_TILES+filename+'/Images_'+filename+'/'
File dir2 = new File(path_img)
dir2.mkdir();


//Get focus on tissue (= Simple Tissue Detection)
runPlugin('qupath.imagej.detect.tissue.SimpleTissueDetection2', '{"threshold": 209,  "requestedPixelSizeMicrons": 20.0,  "minAreaMicrons": 10000.0,  "maxHoleAreaMicrons": 1000000.0,  "darkBackground": false,  "smoothImage": true,  "medianCleanup": true,  "dilateBoundaries": false,  "smoothCoordinates": true,  "excludeOnBoundary": false,  "singleAnnotation": true}');
// Make square tiles of 100µ, measure things in it & export informations //
selectAnnotations()
runPlugin('qupath.lib.algorithms.TilerPlugin', '{"tileSizeMicrons": 100.0,  "trimToROI": false,  "makeAnnotations": false,  "removeParentAnnotation": true}');


// Get the right Class as name for each tile //

i=1

for (detection in getDetectionObjects()){

    roi = detection.getROI()
            
    def request = RegionRequest.createInstance(imageData.getServerPath(), 1, roi)
        
    String tiletype = detection.getParent().getPathClass()
    if (!tiletype.equals("Image")) {
    
        String tilename = String.format("%d", i)
        
rightname = getPathClass(tilename)
detection.setPathClass(rightname)
i++
}}
fireHierarchyUpdate()


// Exporting tiles as images //
i = 1

for (detection in getDetectionObjects()){

    roi = detection.getROI()
            
    def request = RegionRequest.createInstance(imageData.getServerPath(), 1, roi)
        
    String tiletype = detection.getParent().getPathClass()
    if (!tiletype.equals("Image")) {
    
        String tilename = String.format("%s_%d.tif", filename, i)
        ImageWriterTools.writeImageRegion(server, request, path_img + "/" + tilename);
   i++
    }}
print ('Tiles images exported')


// Define how many decimal places to use in output
int nDecimalPlaces = 3

// Create an output file & get a PrintWriter in a Groovy way

def file = new File(BSC_TILES+filename+'/'+filename+'_tileXY.txt')
def a=1;
def b=1;
def polname=""
file.withPrintWriter { writer ->
writer.println("Tile-Point"+"\t"+"x"+"\t"+"y"+"\t"+'Nb points')   
    // Loop through all detections
    for (detection in QPEx.getDetectionObjects()) {
        // Get the nucleus ROI if we have a PathCellObject,
        // or the 'standard' ROI otherwise (i.e. we just have a PathDetectionObject only)
       
        def roi = PathObjectTools.getROI(detection, true)
        try {
            // Not sure how you want to format the output...
            // Here, I create a list & then join entries with a comma
            def x = ['x=']
            def y = ['y=']
            def nbXY = roi.getAllPoints().size()
                       
                      for (p in roi.getAllPoints()) {
                x << GeneralTools.formatNumber(p.getX(), nDecimalPlaces)
                y << GeneralTools.formatNumber(p.getY(), nDecimalPlaces)
            xtemp=x.get(b);
            ytemp=y.get(b);
            
                         polname="Tile"+a+" Point"+b
                         writer.println(polname+"\t"+xtemp+"\t"+ytemp+"\t"+nbXY)
         
             b=b+1}
          
            
            // Write number of points, then x & y coordinates
            //writer.println(x.size())
            //writer.println(String.join('\t', x))
            //writer.println(String.join('\t', y))
        } catch (Exception e) {
            print 'Problem exporting points for ' + roi
        }
   a=a+1;
   b=1
    }
    
}
print "Tile points' exported!"

// Save qpadata of this //
def img1 = getCurrentImageData()
def qpdata1 = new File(BSC_TILES+filename+'/'+filename+'_tiles.qpdata')
qupath.lib.io.PathIO.writeImageData(qpdata1, img1)
