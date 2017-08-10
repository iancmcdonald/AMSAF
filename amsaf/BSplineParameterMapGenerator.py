from ParameterMapGenerator import ParameterMapGenerator


class BSplineParameterMapGenerator(ParameterMapGenerator):
    def __init__(self):
        super(BSplineParameterMapGenerator, self).__init__()
        self.transformType = 'bspline'
        self.paramDict = {
            'AutomaticParameterEstimation': ['true'],
            'FinalGridSpacingInPhysicalUnits': ['2', '4', '8'],
            'MaximumNumberOfIterations': ['1024'],
            'NumberOfHistogramBins': ['32']
        }
