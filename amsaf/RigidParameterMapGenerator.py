from ParameterMapGenerator import ParameterMapGenerator


class RigidParameterMapGenerator(ParameterMapGenerator):
    def __init__(self):
        super(RigidParameterMapGenerator, self).__init__()
        self.transformType = 'rigid'
        self.paramDict = {
            'AutomaticParameterEstimation': ['true'],
            'AutomaticTransformInitialization': ['true'],
            'BSplineInterpolationOrder': ['1', '3'],
            'CheckNumberOfSamples': ['true'],
            'DefaultPixelValue': ['0'],
            'FinalBSplineInterpolationOrder': ['3'],
            'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
            'Interpolator': ['BSplineInterpolator'],
            'MaximumNumberOfIterations': ['512', '1024', '2048'],
            'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                       'NormalizedMutualInformation'],
            'NumberOfHistogramBins': ['32', '64'],
            'NumberOfResolutions': ['3', '6'],
            'NumberOfSpatialSamples': ['2000'],
            'Registration': ['MultiResolutionRegistration'],
            'Resampler': ['DefaultResampler'],
            'ResampleInterpolator': ['FinalBSplineInterpolator']
        }
