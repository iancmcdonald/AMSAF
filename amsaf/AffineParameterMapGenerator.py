from ParameterMapGenerator import ParameterMapGenerator


class AffineParameterMapGenerator(ParameterMapGenerator):
    def __init__(self):
        super(AffineParameterMapGenerator, self).__init__()
        self.transformType = 'affine'
        self.paramDict = {
            'MaximumNumberOfIterations': ['512', '1024'],
            'Interpolator': ['BSplineInterpolator'],
            'NumberOfHistogramBins': ['32', '64']
        }
