# coding=utf-8
# Loic Serafin
import vtk

reader = vtk.vtkSLCReader()
reader.SetFileName("data/ts14_painted.slc")

DELTA = 0.001


class Region:
    def __init__(self, scalar_from, scalar_to, color, opacity):
        self.scalar_from = scalar_from
        self.scalar_to = scalar_to
        self.color = color
        self.opacity = opacity


def isolate_region(region, opacity_func, color_func):
    opacity_func.AddPoint(region.scalar_from - DELTA, 0.0)
    opacity_func.AddPoint(region.scalar_from, region.opacity)
    opacity_func.AddPoint(region.scalar_to, region.opacity)
    opacity_func.AddPoint(region.scalar_to + DELTA, 0.0)

    r, g, b = region.color

    color_func.AddRGBPoint(region.scalar_from, r, g, b)
    color_func.AddRGBPoint(region.scalar_to, r, g, b)


def isolate_regions(region_list):
    opacity_func = vtk.vtkPiecewiseFunction()
    color_func = vtk.vtkColorTransferFunction()
    opacity_func.AddPoint(0, 0.0)
    opacity_func.AddPoint(255, 0.0)
    color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)
    color_func.AddRGBPoint(255, 0.0, 0.0, 0.0)

    for region in region_list:
        isolate_region(region, opacity_func, color_func)

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
    (1, 1, 0),
    (1, 0.583, 0.173),
    (0, 0.8, 0.8),
    (0.543, 0.886, 0.206),
    (0.307, 0.606, 0.023),
    (0.448, 0.624, 0.811),
    (0.128, 0.288, 0.529),
    (0.678, 0.498, 0.658),
    (0.936, 0.159, 0.162)
]

ligne_primitive = Region(64, 95, colors[0], 0.003)
ectoderme = Region(96, 127, colors[1], 0.005)
appareil_digestif = Region(128, 159, colors[2], 0.005)
cerveau = Region(160, 191, colors[3], 0.005)
colonne_vertebrale = Region(192, 223, colors[5], 0.005)
carotide_gauche = Region(224, 224, colors[4], 0.100)
carotide_droit = Region(225, 225, colors[6], 0.100)
vesicule_optique = Region(226, 226, colors[7], 0.010)
paroi_externe = Region(227, 227, colors[8], 0.005)

volume = isolate_regions([
    ligne_primitive,
    ectoderme,
    appareil_digestif,
    cerveau,
    colonne_vertebrale,
    carotide_gauche,
    carotide_droit,
    vesicule_optique,
    paroi_externe
])

renderer.AddVolume(volume)
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
