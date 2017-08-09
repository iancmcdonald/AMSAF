import SimpleITK as sitk
from sklearn.model_selection import ParameterGrid


class ParameterMapService(object):
    def __init__(self):
        super(ParameterMapService, self).__init__()

        self.rigidParamGridDict = {
            'AutomaticParameterEstimation': ['true'],
            'AutomaticTransformInitialization': ['true'],
            'BSplineInterpolationOrder': ['1', '3'],
            'CheckNumberOfSamples': ['true'],
            'DefaultPixelValue': ['0'],
            'FinalBSplineInterpolationOrder': ['3'],
            'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
            'Interpolator': ['BSplineInterpolator'],
            'MaximumNumberOfIterations': ['512' '1024' '2048'],
            'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                       'NormalizedMutualInformation'],
            'NumberOfHistogramBins': ['32', '64'],
            'NumberOfResolutions': ['3', '6'],
            'NumberOfSpatialSamples': ['2000'],
            'Registration': ['MultiResolutionRegistration'],
            'Resampler': ['DefaultResampler'],
            'ResampleInterpolator': ['FinalBSplineInterpolator']
        }

        self.affineParamGridDict = {
            'MaximumNumberOfIterations': ['512', '1024', '2048'],
            'Interpolator': ['LinearInterpolator', 'BSplineInterpolator'],
            'NumberOfHistogramBins': ['32', '64']
        }

        self.bsplineParamGridDict = {
            'AutomaticParameterEstimation': ['true'],
            'FinalGridSpacingInPhysicalUnits': ['2', '4', '8'],
            'MaximumNumberofIterations': ['512', '1024', '2048'],
            'NumberOfHistogramBins': ['32', '64']
        }

    def convertToElastix(self, rigidParams, affineParams, bsplineParams):
        # type: (dict, dict, dict) -> [sitk.ParameterMap, sitk.ParameterMap, sitk.ParameterMap]

        def editMap(paramDict, pMap):
            # type: (dict, sitk.ParameterMap) -> sitk.ParameterMap
            for param, val in paramDict.iteritems():
                pMap[param] = [val]
            return pMap

        # Edit default parameter maps to incorporate grid search values
        rigidParamMap = editMap(rigidParams, sitk.GetDefaultParameterMap('rigid'))
        affineParamMap = editMap(affineParams, sitk.GetDefaultParameterMap('affine'))
        bsplineParamMap = editMap(bsplineParams, sitk.GetDefaultParameterMap('bspline'))

        return [rigidParamMap, affineParamMap, bsplineParamMap]

    def generateParameterMaps(self, priors):
        # type: (object) -> [sitk.ParameterMap, sitk.ParameterMap, sitk.ParameterMap]

        bsplineGrid = ParameterGrid(self.bsplineParamGridDict)
        affineGrid = ParameterGrid(self.affineParamGridDict)
        rigidGrid = ParameterGrid(self.rigidParamGridDict)

        for bsplineParams in bsplineGrid:
            for affineParams in affineGrid:
                for rigidParams in rigidGrid:
                    yield self.convertToElastix(rigidParams, affineParams, bsplineParams)
