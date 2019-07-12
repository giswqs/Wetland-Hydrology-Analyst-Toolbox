__author__ = 'Qiush'
import arcpy
import os

def DelineateCatchment(DEMRasterPath,SinkPolyPath,OutputPath):
    arcpy.CheckOutExtension("Spatial")
    workspace = os.path.split(OutputPath)[0]
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    if arcpy.Exists(DEMRasterPath) == False:
        print("The input raster does not exist")
        quit()

    if (os.path.splitext(OutputPath)[1].lower() == ".shp"):
        FieldOID = "FID"
        FlowDirection = os.path.join(workspace,"FlowDirection.tif")
        SinkRaster = os.path.join(workspace,"SinkRaster.tif")
        Watershed = os.path.join(workspace,"Watershed.tif")
        Catchment = os.path.join(workspace,"Catchment.shp")


    else:
        FieldOID = "OBJECTID"
        FlowDirection = os.path.join(workspace,"FlowDirection")
        SinkRaster = os.path.join(workspace,"SinkRaster")
        Watershed = os.path.join(workspace,"Watershed")
        Catchment = os.path.join(workspace,"Catchment")

    input_dem = arcpy.Raster(DEMRasterPath)
    flow_direction = arcpy.sa.FlowDirection(input_dem)
    flow_direction.save(FlowDirection)

    cell_size = input_dem.meanCellWidth
    arcpy.env.extent = input_dem.extent
    arcpy.PolygonToRaster_conversion(SinkPolyPath,FieldOID,SinkRaster,"CELL_CENTER","NONE",cell_size)

    watershed = arcpy.sa.Watershed(flow_direction,SinkRaster,"Value")
    watershed.save(Watershed)

    arcpy.RasterToPolygon_conversion(watershed,Catchment,"NO_SIMPLIFY","Value")

    return OutputPath

# DEMRasterPath = r"C:\temp\flow\testdata.gdb\dem_final"
# OutputPath = r"C:\temp\flow\testdata.gdb\catchment"
# SinkPolyPath = r"C:\temp\flow\testdata.gdb\sink_poly"

DEMRasterPath = arcpy.GetParameterAsText(0)
SinkPolyPath = arcpy.GetParameterAsText(1)
OutputPath = arcpy.GetParameterAsText(2)

DelineateCatchment(DEMRasterPath,SinkPolyPath,OutputPath)
