# coding=utf-8
# Loïc Serafin

import vtk

file = open('altitudes.txt', 'r')
(width, height) = file.readline().split()
width = int(width)
height = int(height)

leman_map = vtk.vtkPolyData()
points = vtk.vtkPoints()
strip = vtk.vtkCellArray()
scalars = vtk.vtkFloatArray()

width_meters = 277371. / width
height_meters = 197109. / height

matrix = []


def getPointIndex(i, j):
	return height * i + j


# Create all points and sets scalars based on height value
for x in range(0, width):
	row = map(int, file.readline().split())
	matrix.append(row)
	for y in range(0, height):
		points.InsertNextPoint(width_meters * x, height_meters * y, row[y])
		scalars.InsertTuple1(getPointIndex(x, y), row[y])

# Create triangle strips in the following order
# 2 4 6 8 ...
# 1 3 5 7 ...
# 3002 3004 3006 3008 ...
# 3001 3003 3005 3007 ...
# ...
for x in range(0, width - 1):
	strip.InsertNextCell((height - 1) * 2)
	for y in range(0, height - 1):
		strip.InsertCellPoint(getPointIndex(x + 1, y))
		strip.InsertCellPoint(getPointIndex(x, y))

# Tries to find lakes by checking 8 values around a points to be the same
for i, row in enumerate(matrix):
	for j, val in enumerate(row):
		if (width - 1 > i > 0 and height - 1 > j > 0
		    and val == row[j - 1] == row[j + 1] == matrix[i - 1][j] == matrix[i + 1][j] # left, right, up and bottom points
				== matrix[i - 1][j - 1] == matrix[i - 1][j + 1] == matrix[i + 1][j - 1] == matrix[i + 1][j + 1]): # diagonal points
			scalars.SetValue(getPointIndex(i, j), 0) # sets lake points at scalar 0

leman_map.SetPoints(points)
leman_map.SetStrips(strip)
leman_map.GetPointData().SetScalars(scalars)

transform = vtk.vtkTransform()
filter = vtk.vtkTransformPolyDataFilter()
filter.SetInputData(leman_map)
filter.SetTransform(transform)
transform.RotateZ(-90)
filter.Update()

lookupTable = vtk.vtkLookupTable()
lookupTable.SetNumberOfColors(100)
lookupTable.SetTableRange(100, 2000)
lookupTable.SetHueRange(128 / 360., 29 / 360.)
lookupTable.SetSaturationRange(0.35, 0)
lookupTable.SetValueRange(0.72, 0.8)
lookupTable.SetBelowRangeColor(102 / 255., 114 / 255., 221 / 255., 1) # blue color for lakes
lookupTable.UseBelowRangeColorOn()
lookupTable.Build()

mapper = vtk.vtkPolyDataMapper()

mapper.SetInputConnection(filter.GetOutputPort())
mapper.SetLookupTable(lookupTable)
mapper.UseLookupTableScalarRangeOn()

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(renderer)
ren_win.SetSize(1200, 800)

renderWinInteractor = vtk.vtkRenderWindowInteractor()
renderWinInteractor.SetRenderWindow(ren_win)

style = vtk.vtkInteractorStyleTrackballCamera()
renderWinInteractor.SetInteractorStyle(style)

renderWinInteractor.Initialize()

renderWinInteractor.Render()
renderWinInteractor.Start()
