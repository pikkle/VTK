# Loic Serafin
import vtk

white = (1, 1, 1)
top_left = (0, 0.5, 0.5, 1)
top_right = (0.5, 0.5, 1, 1)
bottom_left = (0, 0, 0.5, 0.5)
bottom_right = (0.5, 0, 1, 0.5)
palette = [(0, 0.225, 0.28, 0.765), (127, 0.867, 0.867, 0.867), (255, 0.714, 0, 0.127)] # palette used by paraview

camera = vtk.vtkCamera()
camera.SetViewUp(0, 0, 1)
camera.SetPosition(0, 1, 0)

def generate_volume_from_slc(file, opacity_points, viewport, rgb_points=palette, camera=camera, background_color=white):
    """
    Generates a volume extracted from an SLC file. 
    Sets an opacity piecewise function to determine how to display the volume.
    :param file: the slc file path
    :param opacity_points: the points to add to the opacity piecewise function
    :param viewport: where to display in the renderer
    :param rgb_points: the palette for the volume
    :param camera: the camera used by the renderer
    :param background_color: the background color of the renderer
    :return: the renderer containing the volume
    """
    reader = vtk.vtkSLCReader()
    reader.SetFileName(file)

    opacity = vtk.vtkPiecewiseFunction()
    for op_point in opacity_points:
        opacity.AddPoint(*op_point)

    color = vtk.vtkColorTransferFunction()
    for color_point in rgb_points:
        color.AddRGBPoint(*color_point)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(color)
    volumeProperty.SetScalarOpacity(opacity)
    volumeProperty.SetInterpolationTypeToLinear()

    composite = vtk.vtkVolumeRayCastCompositeFunction()
    mapper = vtk.vtkVolumeRayCastMapper()
    mapper.SetVolumeRayCastFunction(composite)
    mapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volumeProperty)

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(*background_color)
    renderer.SetViewport(*viewport)
    renderer.AddVolume(volume)
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()

    return renderer


stage10 = generate_volume_from_slc("data/ts10.slc",
                                   [(0, 0), (72.290, 0), (175.561, 0.022), (255, 0)], # calculated on paraview
                                   top_left)
stage11 = generate_volume_from_slc("data/ts11.slc",
                                   [(0, 0), (101.682, 0), (140.514, 0.03), (255, 0)],
                                   top_right)
stage12 = generate_volume_from_slc("data/ts12.slc",
                                   [(0, 0), (101.682, 0), (112.4, 0.03), (255, 0)],
                                   bottom_left)
stage13 = generate_volume_from_slc("data/ts13.slc",
                                   [(0, 0), (101.682, 0), (125.65, 0.1), (255, 0)],
                                   bottom_right)


ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(stage10)
ren_win.AddRenderer(stage11)
ren_win.AddRenderer(stage12)
ren_win.AddRenderer(stage13)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)
ren_win.SetSize(1200, 800)
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

ren_win.Render()

iren.Start()
