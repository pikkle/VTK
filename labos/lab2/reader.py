#!/usr/bin/env python

import vtk, sys

if len(sys.argv) != 2:
    sys.exit("Need one argument: vtk data file as parameter")

reader = vtk.vtkPolyDataReader()
reader.SetFileName(sys.argv[1])

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetScalarRange(0, 7)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().BackfaceCullingOn()

ren1 = vtk.vtkRenderer()
ren1.AddActor(actor)
ren1.SetBackground(0.1, 0.2, 0.4)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
