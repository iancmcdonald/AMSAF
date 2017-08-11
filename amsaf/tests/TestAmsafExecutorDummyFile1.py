# This file is a test file that replicates ParameterMapService to be passed into one of the
# unit tests for the TestAmsafExecutor.py file

from amsaf.ParameterMapGenerator import ParameterMapGenerator


class TestParameterMapService(object):
    def __init__(self):
        self.RigidMap = EulerMap
        self.AffineMap = AffineMap
        self.BSplineMap = BSplineMap

    def addParameterPriors(self, parameterPriors):
        for params, priors in zip(
                [self.RigidMap, self.AffineMap, self.BSplineMap], parameterPriors):
            params.addParameterPriors(priors)


    def generateParameterMaps(self):
        for rigid in self.RigidMap.generateParameterMaps():
            for affine in self.AffineMap.generateParameterMaps():
                for bspline in self.AffineMap.generateParameterMaps():
                    yield [rigid, affine, bspline]


class BSplineMap(ParameterMapGenerator):
    def __init__(self):
        super(BSplineMap).__init__()
        self.transformType = "bspline_transform"
        self.paramDict = {}

class AffineMap(ParameterMapGenerator):
    def __init__(self):
        super(AffineMap).__init__()
        self.transformType = "affine_transform"
        self.paramDict = {}

class EulerMap(ParameterMapGenerator):
    def __init__(self):
        super(EulerMap).__init__()
        self.transformType = "rigid_transform"
        self.paramDict = {
            'AutomaticTransformInitialization': ['true']
        }