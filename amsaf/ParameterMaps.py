# This file contains parameter maps to be iterated over for both affine and bspline transformations

if transform == 'affine':
    param_grid = {
        'AutomaticParameterEstimation': ['true'],
        'AutomaticTransformInitialization': ['true'],
        'AutomaticTransformInitializationMethod': ['CenterOfGravity', 'Origins', 'GeometricalCenter',
                                                   'GeometryTop'],
        'BSplineInterpolationOrder': ['1', '3'],
        'CheckNumberOfSamples': ['true'],
        'DefaultPixelValue': ['0'],
        'FinalBSplineInterpolationOrder': ['3'],
        'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
        'ImagePyramidSchedule': ['8 8 8  4 4 4  2 2 2  1 1 1', '4 4  4 3  2 1  1 1'],
        'ImageSampler': ['Random'],
        'Interpolator': ['BSplineInterpolator'],
        'MaximumNumberOfIterations': ['256', '512', '1024'],
        'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                   'NormalizedMutualInformation'],
        'NewSamplesEveryIteration': ['true'],
        'NumberOfHistogramBins': ['32', '64', '128', '16 32 64', '64 32 16'],
        'NumberOfResolutions': ['3', '4', '6'],
        'NumberOfSpatialSamples': ['2048'],
        'Registration': ['MultiResolutionRegistration'],
        'Resampler': ['DefaultResampler'],
        'ResampleInterpolator': ['FinalBSplineInterpolator']
    }

if transform == 'bspline':
    param_grid = {
        'AutomaticParameterEstimation': ['true'],
        'AutomaticTransformInitialization': ['true'],
        'AutomaticTransformInitializationMethod': ['CenterOfGravity', 'Origins', 'GeometricalCenter',
                                                   'GeometryTop'],
        'BSplineInterpolationOrder': ['1', '3'],
        'CheckNumberOfSamples': ['true'],
        'DefaultPixelValue': ['0'],
        'FinalBSplineInterpolationOrder': ['3'],
        'FinalGridSpacingInPhysicalUnits': ['4', '8', '16', '32', '64'],
        'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
        'ImagePyramidSchedule': ['8 8 8  4 4 4  2 2 2  1 1 1', '4 4  4 3  2 1  1 1'],
        'ImageSampler': ['Random'],
        'Interpolator': ['BSplineInterpolator'],
        'MaximumNumberOfIterations': ['256', '512', '1024', '2048'],
        'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                   'NormalizedMutualInformation'],
        'NewSamplesEveryIteration': ['true'],
        'NumberOfHistogramBins': ['32', '64', '128', '16 32 64', '64 32 16'],
        'NumberOfResolutions': ['3', '4', '6'],
        'NumberOfSpatialSamples': ['2048'],
        'Registration': ['MultiResolutionRegistration'],
        'Resampler': ['DefaultResampler'],
        'ResampleInterpolator': ['FinalBSplineInterpolator']
    }