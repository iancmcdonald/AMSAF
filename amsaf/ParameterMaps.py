# This file contains parameter maps to be iterated over for both affine and bspline transformations

if transform == 'affine':
    param_grid = {
        'AutomaticParameterEstimation': ['true'],
        'AutomaticTransformInitialization': ['true'],
        'BSplineInterpolationOrder': ['1', '3'],
        'CheckNumberOfSamples': ['true'],
        'DefaultPixelValue': ['0'],
        'FinalBSplineInterpolationOrder': ['3'],
        'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
        'ImagePyramidSchedule': ['8 8 8  4 4 4  2 2 2  1 1 1', '4 4  4 3  2 1  1 1'],
        'ImageSampler': ['Random'],
        'Interpolator': ['BSplineInterpolator'],
        'MaximumNumberOfIterations': ['1024'],
        'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation'],
        'NewSamplesEveryIteration': ['true'],
        'NumberOfHistogramBins': ['32', '64'],
        'NumberOfResolutions': ['3', '6'],
        'NumberOfSpatialSamples': ['2048'],
        'Registration': ['MultiResolutionRegistration'],
        'Resampler': ['DefaultResampler'],
        'ResampleInterpolator': ['FinalBSplineInterpolator']
    }

if transform == 'bspline':
    param_grid = {
        'AutomaticParameterEstimation': ['true'],
        'AutomaticTransformInitialization': ['true'],
        'BSplineInterpolationOrder': ['1', '3'],
        'CheckNumberOfSamples': ['true'],
        'DefaultPixelValue': ['0'],
        'FinalBSplineInterpolationOrder': ['3'],
        'FinalGridSpacingInPhysicalUnits': ['4', '8', '16', '32', '64'],
        'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
        'ImagePyramidSchedule': ['8 8 8  4 4 4  2 2 2  1 1 1', '4 4  4 3  2 1  1 1'],
        'ImageSampler': ['Random'],
        'Interpolator': ['BSplineInterpolator'],
        'MaximumNumberOfIterations': ['2048'],
        'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                   'NormalizedMutualInformation'],
        'NewSamplesEveryIteration': ['true'],
        'NumberOfHistogramBins': ['32', '64'],
        'NumberOfResolutions': ['3', '6'],
        'NumberOfSpatialSamples': ['2048'],
        'Registration': ['MultiResolutionRegistration'],
        'Resampler': ['DefaultResampler'],
        'ResampleInterpolator': ['FinalBSplineInterpolator']
    }