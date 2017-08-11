from ParameterMapGenerator import ParameterMapGenerator


class RigidParameterMapGenerator(ParameterMapGenerator):
    def __init__(self):
        super(RigidParameterMapGenerator, self).__init__()
        self.transformType = 'rigid'
        self.paramDict = {
            'AutomaticParameterEstimation': ['true'],
            'AutomaticTransformInitialization': ['true'],
            'BSplineInterpolationOrder': ['3'],
            'CheckNumberOfSamples': ['true'],
            'DefaultPixelValue': ['0'],
            'FinalBSplineInterpolationOrder': ['3'],
            'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
            'Interpolator': ['BSplineInterpolator'],
            'MaximumNumberOfIterations': ['1024'],
            'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation'],
            'NumberOfHistogramBins': ['64'],
            'NumberOfResolutions': ['3', '6'],
            'NumberOfSpatialSamples': ['2000'],
            'Registration': ['MultiResolutionRegistration'],
            'Resampler': ['DefaultResampler'],
            'ResampleInterpolator': ['FinalBSplineInterpolator']
        }
