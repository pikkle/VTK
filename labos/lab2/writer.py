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

triangleStrips = [[0, 1, 2, 3, 6, 7, 4, 5],
                  [2, 6, 0, 4, 1, 5, 3, 7]]


def writeFile(filename, polydata):
	writer = vtk.vtkPolyDataWriter()
	writer.SetFileName(filename)
	writer.SetInputData(polydata)
	writer.Write()


# Use squares
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

writeFile('data/cubeSquares.vtk', cube)

# Use triangles
polys = vtk.vtkCellArray()

for face in triangles:
	polys.InsertNextCell(3, face)

cube.SetPolys(polys)

writeFile('data/cubeTriangles.vtk', cube)

# Using two triangle strips
strip = vtk.vtkCellArray()
for s in triangleStrips:
	strip.InsertNextCell(len(s))
	for i in s:
		strip.InsertCellPoint(i)

cube = vtk.vtkPolyData()
cube.SetPoints(points)
cube.SetStrips(strip)
cube.GetPointData().SetScalars(scalars)

writeFile('data/cubeStrip.vtk', cube)
