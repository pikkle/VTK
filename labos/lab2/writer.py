#!/usr/bin/env python

import vtk

x = [(0.5, 0.5, 0.5),
     (-0.5, 0.5, 0.5),
     (0.5, -0.5, 0.5),
     (-0.5, -0.5, 0.5),
     (0.5, 0.5, -0.5),
     (-0.5, 0.5, -0.5),
     (0.5, -0.5, -0.5),
     (-0.5, -0.5, -0.5)]

squares = [(0, 2, 6, 4),
           (4, 5, 1, 0),
           (1, 3, 2, 0),
           (1, 5, 7, 3),
           (2, 3, 7, 6),
           (7, 5, 4, 6)]

triangles = [(0, 2, 4),
             (2, 6, 4),
             (4, 5, 0),
             (5, 1, 0),
             (1, 3, 2),
             (1, 2, 0),
             (1, 5, 3),
             (5, 7, 3),
             (2, 3, 6),
             (3, 7, 6),
             (7, 5, 6),
             (5, 4, 6)]

cube = vtk.vtkPolyData()
points = vtk.vtkPoints()
polys = vtk.vtkCellArray()
scalars = vtk.vtkFloatArray()

for i in range(0, 8):
    points.InsertPoint(i, x[i])

for face in squares:
    polys.InsertNextCell(4, face)

for i in range(0, 8):
    scalars.InsertTuple1(i, i)

cube.SetPoints(points)
cube.SetPolys(polys)
cube.GetPointData().SetScalars(scalars)

writer = vtk.vtkPolyDataWriter()
writer.SetFileName('data/cubeSquares.vtk')
writer.SetInputData(cube)
writer.Write()

# Use triangles instead of squares
polys = vtk.vtkCellArray()

for face in triangles:
    polys.InsertNextCell(3, face)

cube.SetPolys(polys)

writer = vtk.vtkPolyDataWriter()
writer.SetFileName('data/cubeTriangles.vtk')
writer.SetInputData(cube)
writer.Write()
