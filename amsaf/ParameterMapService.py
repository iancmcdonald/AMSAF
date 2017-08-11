import SimpleITK as sitk
from RigidParameterMapGenerator import RigidParameterMapGenerator
from AffineParameterMapGenerator import AffineParameterMapGenerator
from BSplineParameterMapGenerator import BSplineParameterMapGenerator


class ParameterMapService(object):
    def __init__(self, rigidParameterMapGeneratorInjectable=RigidParameterMapGenerator,
                 affineParameterMapGeneratorInjectable=AffineParameterMapGenerator,
                 bSplineParameterMapGeneratorInjectable=BSplineParameterMapGenerator):
        super(ParameterMapService, self).__init__()
        self.rigidParameterMapGenerator = rigidParameterMapGeneratorInjectable()
        self.affineParameterMapGenerator = affineParameterMapGeneratorInjectable()
        self.bSplineParameterMapGenerator = bSplineParameterMapGeneratorInjectable()

    def addParameterPriors(self, parameterPriors):
        for pMapGen, prior in zip(
                [self.rigidParameterMapGenerator, self.affineParameterMapGenerator, self.bSplineParameterMapGenerator],
                parameterPriors):
            pMapGen.addParameterPriors(prior)

    def generateParameterMaps(self):
        # type: ([dict]) -> [sitk.ParameterMap, sitk.ParameterMap, sitk.ParameterMap]

        for rigidPM in self.rigidParameterMapGenerator.generateParameterMaps():
            for affinePM in self.affineParameterMapGenerator.generateParameterMaps():
                for bSplinePM in self.bSplineParameterMapGenerator.generateParameterMaps():
                    yield [rigidPM, affinePM, bSplinePM]
