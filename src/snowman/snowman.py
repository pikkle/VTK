# coding=utf-8
# Loïc Serafin

import time
import vtk

SNOWMAN_COLOR = (1, 1, 1)  # white
CARROT_COLOR = (0.968, 0.667, 0)  # orange
EYE_COLOR = (0, 0, 0)  # black
BACKGROUND_COLOR = (1, 0.894, 0.893)


def createActor(outputPort, color):
	"""Creates an actor with a PolyDataMapper from the source's outputport given, and sets a color to it"""
	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInputConnection(outputPort)
	actor = vtk.vtkActor()
	actor.SetMapper(mapper)
	actor.GetProperty().SetColor(color)
	return actor


def createSphere(radius, resolution, position):
	"""Creates a sphere source given the radius, the resolution and the position"""
	sphere = vtk.vtkSphereSource()
	sphere.SetRadius(radius)
	sphere.SetThetaResolution(resolution)
	sphere.SetPhiResolution(resolution)
	sphere.SetCenter(position)
	return sphere


def createCone(height, radius, resolution, position):
	"""Creates a cone source given the height, the radius, the resolution and the position"""
	cone = vtk.vtkConeSource()
	cone.SetDirection(0, -90, 0)
	cone.SetHeight(height)
	cone.SetRadius(radius)
	cone.SetResolution(resolution)
	cone.SetCenter(position)
	return cone


def getTransfAndFilter(actor):
	"""Creates both Transform and TransformPolyDataFilter for a given actor"""
	transform = vtk.vtkTransform()
	filter = vtk.vtkTransformPolyDataFilter()
	filter.SetInputConnection(actor.GetOutputPort())
	filter.SetTransform(transform)
	filter.Update()
	return (transform, filter)

# create all objects
head = createSphere(1, 20, (-3, 0, 0))
body = createSphere(1.5, 20, (0, 0, 0))
carrot = createCone(0.3, 0.1, 20, (3, 0, 0))
eye1 = createSphere(0.1, 20, (0.2, 2.3, 1))
eye2 = createSphere(0.1, 20, (-0.2, 2.3, 1))

# create transforms and filters for objects
(headTransform, headFilter) = getTransfAndFilter(head)
(bodyTransform, bodyFilter) = getTransfAndFilter(body)
(carrotTransform, carrotFilter) = getTransfAndFilter(carrot)
(eye1Tranform, eye1Filter) = getTransfAndFilter(eye1)
(eye2ranform, eye2Filter) = getTransfAndFilter(eye2)

# create associated actors
headActor = createActor(headFilter.GetOutputPort(), SNOWMAN_COLOR)
bodyActor = createActor(bodyFilter.GetOutputPort(), SNOWMAN_COLOR)
carrotActor = createActor(carrotFilter.GetOutputPort(), CARROT_COLOR)
eye1Actor = createActor(eye1Filter.GetOutputPort(), EYE_COLOR)
eye2Actor = createActor(eye2Filter.GetOutputPort(), EYE_COLOR)

# prepare the renderers
ren1 = vtk.vtkRenderer()
ren1.AddActor(headActor)
ren1.AddActor(bodyActor)
ren1.AddActor(carrotActor)
ren1.SetBackground(BACKGROUND_COLOR)
camera = ren1.GetActiveCamera()
camera.SetPosition(0, 0, 20) # sets the camera a bit higher

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(600, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()

def animate(animationFunction, params, steps, deltaT=0.03):
	"""Simple animation procedure, executing the animationFunction parameter with the params, doing *steps* ticks separated by *deltaT* seconds"""
	for i in range(0, steps):
		time.sleep(deltaT)
		iren.Render()
		animationFunction(params)


# use PostMultiply to make all transformations in comparison of the origin
headTransform.PostMultiply()
bodyTransform.PostMultiply()
carrotTransform.PostMultiply()

# place head on body
animate(headTransform.RotateZ, -1, 90)
animate(headTransform.Translate, (0, -0.05, 0), 16)

# place carrot on head
animate(carrotTransform.RotateY, -1, 90)
animate(carrotTransform.Translate, (0, 0, -0.05), 20)
animate(carrotTransform.RotateX, -1, 90)
animate(carrotTransform.Translate, (0, 0.05, 0), 3)
animate(carrotTransform.Translate, (0, 0, 0.05), 22)

# display eyes
ren1.AddActor(eye1Actor)
ren1.AddActor(eye2Actor)

# rotates the camera
animate(camera.Roll, 1, 360)
animate(camera.Azimuth, 1, 360)
animate(camera.Elevation, 1, 90)
animate(camera.Elevation, -1, 90)

iren.Start() # lets the user interact with the snowman at the end of the animation
