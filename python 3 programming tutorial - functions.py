import pandas as pd
import scipy



def example():
    print('basic function')
    z = 3 + 9
    print(z)


example()


def simple_addition(num1,num2):
    answer = num1 + num2
    print('num1 is', num1)
    print(answer)

simple_addition(5,3)




# import os
# import arcpy
# from arcpy.sa import *
# import tempfile, shutil
#
#
# arcpy.env.workspace = r'E:\Home\rkush\sara model\PRISM_data_proj'
# arcpy.env.overwriteOutput = True
# outworkspace = r'E:\Home\rkush\sara model\PRISM_data_clip'
#
# arcpy.CheckOutExtension('Spatial')
# tmpdir = tempfile.mkdtemp()
# arcpy.env.scratchWorkspace = tmpdir
# #arcpy.env.scratchWorkspace = r'E:\Home\rkush\sara model\PRISM_data_clip\Scratch.gdb'
#
# shape_file = 'grid_DIS_v2.shp'
# shape_file_repaired = r'E:\Home\rkush\sara model\PRISM_data_proj\grid_DIS_v2_repair.shp'
# for i in arcpy.ListFeatureClasses():
#     shape_file = arcpy.Describe(i)
#
# print(shape_file)
# y_max = 3329607.549667
# x_max = 790897.005375
# y_min = 3005655.000422
# x_min = 497592.292000
#
# rectangle = str(str(x_min) + ' ' + str(y_min) + ' ' + str(x_max) + ' ' + str(y_max))
# print(rectangle)
#
# extent = r'E:\Home\rkush\sara model\PRISM_data_proj\grid_DIS_v2.shp'
# disc = arcpy.Describe(extent)
# #rectangle = arcpy.Polygon(arcpy.Array([extent.lowerLeft, extent.upperLeft, extent.upperRight, extent.lowerRight, extent.lowerLeft]),
#
# try:
#     for raster in arcpy.ListRasters():
#         print(raster)
#         dsc = arcpy.Describe(raster)
#         if dsc.spatialReference.Name == "Unknown":
#             print ('skipped this raster due to undefined coordinate system: ' + raster)
#         else:
#             #arcpy.Describe(raster).baseName
#             out_raster = os.path.join(outworkspace, str(raster))
#             print('Superman')
#             #raster_name = str(raster + '.bil')
#             #arcpy.MakeRasterLayer_management(raster, out_raster)
#             print(raster)
#             print('SHAZAM!')
#             print(arcpy.Describe(raster).spatialReference.name)
#             #outPJ = arcpy.SpatialReference(26914) #26914 is the code for 'NAD_1983_UTM_Zone_14N'
#             print('Batman')
#             # try:
#             #     arcpy.BuildRasterAttributeTable_management(raster, "Overwrite")
#             # except:
#             #     print "Build Raster Attribute Table example failed."
#             #     print arcpy.GetMessages()
#             print('Martian Man Hunter')
#             i = 1
#             print('This is raster number ' + i)
#             i += 1
#             #Clip_management(in_raster, rectangle, out_raster, {in_template_dataset}, {nodata_value},{clipping_geometry}, {maintain_clipping_extent})
#             arcpy.Clip_management(raster,'#',out_raster,shape_file_repaired,'0','ClippingGeometry')#,'MAINTAIN_EXTENT')
#             # outExtractByMask = ExtractByMask(raster,shape_file_repaired)
#             # print('Aquaman')
#             # #
#             # print('Green Lantern')
#             # outExtractByMask.save(r'E:\Home\rkush\sara model\PRISM_data_clip\clipped_rasters.gdb')
#             # print('Wonder Woman')
#
#             print('Cyborg')
#
#
#             #arcpy.ProjectRaster_management(raster, out_raster, outPJ)
#             print(arcpy.GetMessages())
# except arcpy.ExecuteError:
#     print(arcpy.GetMessages(2))
#
# except Exception as ex:
#     print(ex.args[0])
#
# arcpy.CheckInExtension('Spatial')
# shutil.rmtree(tmpdir)
