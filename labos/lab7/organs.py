# coding=utf-8
import vtk

reader = vtk.vtkSLCReader()
reader.SetFileName("data/ts14_painted.slc")

DELTA = 0.001


def isolate_organ(scalar_from, scalar_to, color, opacity=1.0):
    """
    Creates a volume visible only within the bounds. 
    The parameter opacity sets the opacity ratio for the visible part.
    
    :param scalar_from: starting scalar bound
    :param scalar_to: ending scalar bound
    :param color: the color of the volume (r,g,b)
    :param opacity: the max opacity
    :return: 
    """
    r, g, b = color
    opacity_func = vtk.vtkPiecewiseFunction()
    opacity_func.AddPoint(0, 0.0)
    opacity_func.AddPoint(scalar_from - DELTA, 0.0)
    opacity_func.AddPoint(scalar_from, opacity)
    opacity_func.AddPoint(scalar_to, opacity)
    opacity_func.AddPoint(scalar_to + DELTA, 0.0)
    opacity_func.AddPoint(255, 0.0)

    color_func = vtk.vtkColorTransferFunction()
    for color_point in [(0, r, g, b), (255, r, g, b)]:
        color_func.AddRGBPoint(*color_point)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetScalarOpacity(opacity_func)
    volumeProperty.SetColor(color_func)
    volumeProperty.SetInterpolationTypeToLinear()

    composite = vtk.vtkVolumeRayCastCompositeFunction()
    mapper = vtk.vtkVolumeRayCastMapper()
    mapper.SetVolumeRayCastFunction(composite)
    mapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volumeProperty)

    return volume


renderer = vtk.vtkRenderer()
colors = [
    (0.929, 0.830, 0),
    (0.971, 0.583, 0.173),
    (0.561, 0.351, 0.008),
    (0.543, 0.886, 0.206),
    (0.307, 0.606, 0.023),
    (0.448, 0.624, 0.811),
    (0.128, 0.288, 0.529),
    (0.678, 0.498, 0.658),
    (0.936, 0.159, 0.162)
]

renderer.AddVolume(isolate_organ(64,  95,  colors[0], 0.003))  # Ligne Primitive,            JAUNE
renderer.AddVolume(isolate_organ(96,  127, colors[1], 0.005))  # Ectoderme,                  ORANGE
renderer.AddVolume(isolate_organ(128, 159, colors[2], 0.005))  # Appareil digestif,          BRUN
renderer.AddVolume(isolate_organ(160, 191, colors[3], 0.005))  # Futur cerveau,              VERT CLAIR
renderer.AddVolume(isolate_organ(192, 223, colors[4], 0.005))  # Future colonne vertébrale,  VERT FONCÉ
renderer.AddVolume(isolate_organ(224, 224, colors[5], 0.100))  # Artère carotide gauche,     BLEU CLAIR
renderer.AddVolume(isolate_organ(225, 225, colors[6], 0.100))  # Artère carotide droite,     BLEU FONCÉ
renderer.AddVolume(isolate_organ(226, 226, colors[7], 0.010))  # Vésicule optique,           VIOLET
renderer.AddVolume(isolate_organ(227, 227, colors[8], 0.005))  # Paroi externe de l'embryon, ROUGE
renderer.ResetCamera()
renderer.SetBackground(1, 1, 1)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1200, 800)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
