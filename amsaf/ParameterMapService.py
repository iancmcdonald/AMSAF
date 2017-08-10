import SimpleITK as sitk
from RigidParameterMapGenerator import RigidParameterMapGenerator
from AffineParameterMapGenerator import AffineParameterMapGenerator
from BSplineParameterMapGenerator import BSplineParameterMapGenerator


class ParameterMapService(object):
    def __init__(self):
        super(ParameterMapService, self).__init__()

    @staticmethod
    def generateParameterMaps(parameterPriors):
        # type: ([dict]) -> [sitk.ParameterMap, sitk.ParameterMap, sitk.ParameterMap]
        rigidParameterMapGenerator = RigidParameterMapGenerator()
        affineParameterMapGenerator = AffineParameterMapGenerator()
        bSplineParameterMapGenerator = BSplineParameterMapGenerator()

        rigidParameterMapGenerator.addParameterPriors(parameterPriors[0])
        affineParameterMapGenerator.addParameterPriors(parameterPriors[1])
        bSplineParameterMapGenerator.addParameterPriors(parameterPriors[2])

        for rigidPM in rigidParameterMapGenerator.generateParameterMaps():
            for affinePM in affineParameterMapGenerator.generateParameterMaps():
                for bSplinePM in bSplineParameterMapGenerator.generateParameterMaps():
                    yield [rigidPM, affinePM, bSplinePM]
