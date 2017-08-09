from itertools import imap
from sklearn.model_selection import ParameterGrid
import SimpleITK as sitk


class AmsafExecutor(object):
    def __init__(self):
        super(AmsafExecutor, self).__init__()
        self._refGroundTruthImage = None
        self._refGroundTruthSeg = None
        self._targetGroundTruthImage = None
        self._targetGroundTruthSeg = None
        self._parameterPriors = None
        self._parameterMaps = None
        self._parameterMapGenerator = None

    #######################
    # Getters and Setters #
    #######################

    @property
    def refGroundTruthImage(self):
        return self._refGroundTruthImage

    @refGroundTruthImage.setter
    def refGroundTruthImage(self, value):
        self._refGroundTruthImage = value

    @property
    def refGroundTruthSeg(self):
        return self._refGroundTruthSeg

    @refGroundTruthSeg.setter
    def refGroundTruthSeg(self, value):
        self._refGroundTruthSeg = value

    @property
    def targetGroundTruthImage(self):
        return self._targetGroundTruthImage

    @targetGroundTruthImage.setter
    def targetGroundTruthImage(self, value):
        self._targetGroundTruthImage = value

    @property
    def targetGroundTruthSeg(self):
        return self._targetGroundTruthSeg

    @targetGroundTruthSeg.setter
    def targetGroundTruthSeg(self, value):
        self._targetGroundTruthSeg = value

    @property
    def parameterPriors(self):
        return self._parameterPriors

    @parameterPriors.setter
    def parameterPriors(self, value):
        self._parameterPriors = value

    @property
    def parameterMaps(self):
        return self._parameterMaps

    @parameterMaps.setter
    def parameterMaps(self, value):
        self._parameterMaps = value

    @property
    def parameterMapGenerator(self):
        return self._parameterMapGenerator

    @parameterMapGenerator.setter
    def parameterMapGenerator(self, value):
        self._parameterMapGenerator = value

    ###########
    # Methods #
    ###########

    def findTransformParameterMap(self):
        # type: () -> sitk.ParameterMap

        # Initialize Elastix registration
        elastixImageFilter = sitk.ElastixImageFilter()
        elastixImageFilter.SetFixedImage(self.targetGroundTruthImage)
        elastixImageFilter.SetMovingImage(self.refGroundTruthImage)
        elastixImageFilter.SetParameterMap(self.parameterMaps)

        # Execute Registration
        elastixImageFilter.Execute()

        return elastixImageFilter.GetTransformParameterMap()

    def findResultSeg(self, transformParameterMapVec):
        # type: ([sitk.ParameterMap]) -> sitk.Image

        # Use nearest neighbors interpolator for segmentations
        for tMap in transformParameterMapVec:
            tMap['ResampleInterpolator'] = ['FinalNearestNeighborInterpolator']

        # Initialize Transformix
        transformixImageFilter = sitk.TransformixImageFilter()
        transformixImageFilter.SetMovingImage(self.refGroundTruthSeg)
        transformixImageFilter.SetTransformParameterMap(transformParameterMapVec)

        # Execute transformation
        transformixImageFilter.Execute()

        # Cast voxel types
        resultSeg = sitk.Cast(transformixImageFilter.GetResultImage(), self.refGroundTruthSeg.GetPixelID())

        self.refGroundTruthSeg.CopyInformation(resultSeg)  # copy header information so images are comparable

    def subtractionScore(self, seg):
        # type: (sitk.Image) -> float

        subSeg = self.targetGroundTruthSeg - seg
        statsFilter = sitk.StatisticsImageFilter()
        statsFilter.Execute(subSeg == 0)  # read as: 1 if 0 else 0 for voxel in subSeg

        # sum of ones
        return statsFilter.GetSum()

    def diceScore(self, seg):
        # type: (sitk.Image) -> float

        overlapFilter = sitk.LabelOverlapMeasuresImageFilter()
        overlapFilter.Execute(self.targetGroundTruthSeg, seg)

        return overlapFilter.GetDiceCoefficient()





