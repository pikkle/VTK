# Loic Serafin
import vtk

SKIN_COLOR = 0.812, 0.630, 0.633
BACKGROUND_BL = 0.823, 0.824, 0.994
BACKGROUND_BR = 0.823, 0.824, 0.823
BACKGROUND_TL = 1, 0.827, 0.825
BACKGROUND_TR = 0.823, 0.999, 0.830

reader = vtk.vtkSLCReader()
reader.SetFileName("vw_knee.slc")

skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(reader.GetOutputPort())
skinExtractor.SetValue(0, 45)
skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)
skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper.ScalarVisibilityOff()

boneExtractor = vtk.vtkContourFilter()
boneExtractor.SetInputConnection(reader.GetOutputPort())
boneExtractor.SetValue(0, 75)
boneNormals = vtk.vtkPolyDataNormals()
boneNormals.SetInputConnection(boneExtractor.GetOutputPort())
boneNormals.SetFeatureAngle(60.0)
boneMapper = vtk.vtkPolyDataMapper()
boneMapper.SetInputConnection(boneNormals.GetOutputPort())
boneMapper.ScalarVisibilityOff()

sphere = vtk.vtkSphere()
sphere.SetCenter(70, 40, 100)
sphere.SetRadius(45)

sphereSource = vtk.vtkSphereSource()
sphereSource.SetCenter(70, 40, 100)
sphereSource.SetRadius(45)
sphereSource.SetPhiResolution(20)
sphereSource.SetThetaResolution(20)
sphereSource.Update()

sphereMapper = vtk.vtkPolyDataMapper()
sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
sphereActor = vtk.vtkActor()
sphereActor.SetMapper(sphereMapper)
sphereActor.GetProperty().SetColor(0.3, 0.3, 0)
sphereActor.GetProperty().SetOpacity(0.1)

plane = vtk.vtkPlane()
cutter = vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputData(skinMapper.GetInput())
cutter.GenerateValues(20, 0, 200)
cutterMapper = vtk.vtkPolyDataMapper()
cutterMapper.SetInputConnection(cutter.GetOutputPort())
cutterMapper.ScalarVisibilityOff()
ringsLegActor = vtk.vtkActor()
ringsLegActor.GetProperty().SetLineWidth(4)
ringsLegActor.SetMapper(cutterMapper)
ringsLegActor.GetProperty().SetColor(SKIN_COLOR)

def skinActor():
	skin = vtk.vtkActor()
	skin.GetProperty().SetColor(SKIN_COLOR)
	skin.SetMapper(skinMapper)
	return skin

def cutSkinActor():
	clipper = vtk.vtkClipPolyData()
	clipper.SetInputConnection(skinNormals.GetOutputPort())
	clipper.SetClipFunction(sphere)
	clipper.GenerateClipScalarsOn()
	clipper.GenerateClippedOutputOn()
	clipper.SetValue(10)
	clipMapper = vtk.vtkPolyDataMapper()
	clipMapper.SetInputConnection(clipper.GetOutputPort())
	clipMapper.ScalarVisibilityOff()
	cutLegActor = vtk.vtkActor()
	interior = vtk.vtkProperty()
	interior.SetColor(SKIN_COLOR)
	cutLegActor.SetMapper(clipMapper)
	cutLegActor.GetProperty().SetColor(SKIN_COLOR)
	cutLegActor.SetBackfaceProperty(interior)
	return cutLegActor

def boneActor():
	bone = vtk.vtkActor()
	bone.SetMapper(boneMapper)
	return bone

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

camera = vtk.vtkCamera()
camera.SetViewUp(0, 0, 1)
camera.SetPosition(0, 1, 0)

bottomLeft = vtk.vtkRenderer()
bottomLeft.AddActor(cutSkinActor())
bottomLeft.AddActor(boneActor())
bottomLeft.AddActor(outlineActor)
bottomLeft.AddActor(sphereActor)
bottomLeft.SetBackground(BACKGROUND_BL)
bottomLeft.SetViewport(0, 0, 0.5, 0.5)
bottomLeft.SetActiveCamera(camera)
bottomLeft.ResetCamera()


# Il faudrait stocker ce polydata dans un fichier externe... le temps de calcul est long
distanceFilter = vtk.vtkDistancePolyDataFilter()
distanceFilter.SetInputData(0, boneActor().GetMapper().GetInput())
distanceFilter.SetInputData(1, skinActor().GetMapper().GetInput())
distanceFilter.Update()
distanceMapper = vtk.vtkPolyDataMapper()
distanceMapper.SetInputConnection(distanceFilter.GetOutputPort())
distanceMapper.SetScalarRange(
	distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[0],
	distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[1]
)
distanceActor = vtk.vtkActor()
distanceActor.SetMapper(distanceMapper)

bottomRight = vtk.vtkRenderer()
bottomRight.AddActor(distanceActor)
bottomRight.AddActor(outlineActor)
bottomRight.SetBackground(BACKGROUND_BR)
bottomRight.SetViewport(0.5, 0, 1, 0.5)
bottomRight.SetActiveCamera(camera)
bottomRight.ResetCamera()

topLeft = vtk.vtkRenderer()
topLeft.AddActor(boneActor())
topLeft.AddActor(outlineActor)
topLeft.AddActor(ringsLegActor)
topLeft.SetBackground(BACKGROUND_TL)
topLeft.SetViewport(0, 0.5, 0.5, 1)
topLeft.SetActiveCamera(camera)
topLeft.ResetCamera()

topRight = vtk.vtkRenderer()
tRSkin1 = cutSkinActor()
tRSkin1.GetProperty().FrontfaceCullingOn()
tRSkin2 = cutSkinActor()
tRSkin2.GetProperty().SetOpacity(0.5)
tRSkin2.GetProperty().BackfaceCullingOn()
topRight.AddActor(tRSkin1)
topRight.AddActor(tRSkin2)
topRight.AddActor(boneActor())
topRight.AddActor(outlineActor)
topRight.SetBackground(BACKGROUND_TR)
topRight.SetViewport(0.5, 0.5, 1, 1)
topRight.SetActiveCamera(camera)
topRight.ResetCamera()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(bottomLeft)
renWin.AddRenderer(bottomRight)
renWin.AddRenderer(topLeft)
renWin.AddRenderer(topRight)
renWin.SetSize(1200, 800)

for i in range(0, 360):
	renWin.Render()
	camera.Azimuth(1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
