# Loic Serafin
import vtk


def generate_volume_from_slc(file, opacity_points, rgb_points, camera, background_color, viewport):
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
    volumeProperty.ShadeOn()
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


camera1 = vtk.vtkCamera()
camera1.SetViewUp(0, 0, 1)
camera1.SetPosition(0, 1, 0)

stage10 = generate_volume_from_slc("data/ts10.slc",
                                   [(0, 0), (72.290, 0), (175.561, 0.022), (255, 0)],
                                   [(0, 0.225, 0.28, 0.765), (127, 0.867, 0.867, 0.867), (255, 0.714, 0, 0.127)],
                                   camera1,
                                   (1, 1, 1),
                                   (0, 0.5, 0.5, 1))
stage11 = generate_volume_from_slc("data/ts11.slc",
                                   [(0, 0), (101.682, 0), (125.514, 0.027), (255, 0)],
                                   [(0, 0.225, 0.28, 0.765), (127, 0.867, 0.867, 0.867), (255, 0.714, 0, 0.127)],
                                   camera1,
                                   (1, 1, 1),
                                   (0.5, 0.5, 1, 1))
stage12 = generate_volume_from_slc("data/ts12.slc",
                                   [(0, 0), (101.682, 0), (125.514, 0.027), (255, 0)],
                                   [(0, 0.225, 0.28, 0.765), (127, 0.867, 0.867, 0.867), (255, 0.714, 0, 0.127)],
                                   camera1,
                                   (1, 1, 1),
                                   (0, 0, 0.5, 0.5))
stage13 = generate_volume_from_slc("data/ts13.slc",
                                   [(0, 0), (101.682, 0), (125.514, 0.027), (255, 0)],
                                   [(0, 0.225, 0.28, 0.765), (127, 0.867, 0.867, 0.867), (255, 0.714, 0, 0.127)],
                                   camera1,
                                   (1, 1, 1),
                                   (0.5, 0, 1, 0.5))



ren_win_1 = vtk.vtkRenderWindow()
ren_win_1.AddRenderer(stage10)
ren_win_1.AddRenderer(stage11)
ren_win_1.AddRenderer(stage12)
ren_win_1.AddRenderer(stage13)

iren_1 = vtk.vtkRenderWindowInteractor()
iren_1.SetRenderWindow(ren_win_1)
ren_win_1.SetSize(1200, 800)
style = vtk.vtkInteractorStyleTrackballCamera()
iren_1.SetInteractorStyle(style)

ren_win_1.Render()

iren_1.Start()


# ren_win_2 = vtk.vtkRenderWindow()
# iren_2 = vtk.vtkRenderWindowInteractor()
# iren_2.SetRenderWindow(ren_win_1)
# ren_win_2.SetSize(1200, 800)
# iren_2.SetInteractorStyle(style)
#
# ren_win_2.Render()
#
# iren_2.Start()
