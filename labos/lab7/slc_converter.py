
import vtk

def convert_slc_to_vtk(inputfile, outputfile):
    reader = vtk.vtkSLCReader()
    reader.SetFileName(inputfile)

    writer = vtk.vtkMetaImageWriter()
    writer.SetFileName(outputfile)
    writer.SetInputConnection(reader.GetOutputPort())
    writer.Write()


convert_slc_to_vtk("data/ts10.slc", "data/ts10.mhd")
convert_slc_to_vtk("data/ts11.slc", "data/ts11.mhd")
convert_slc_to_vtk("data/ts12.slc", "data/ts12.mhd")
convert_slc_to_vtk("data/ts13.slc", "data/ts13.mhd")
convert_slc_to_vtk("data/ts14.slc", "data/ts14.mhd")
convert_slc_to_vtk("data/ts14_painted.slc", "data/ts14_painted.mhd")
