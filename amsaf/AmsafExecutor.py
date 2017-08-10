from itertools import imap
import heapq
from sklearn.model_selection import ParameterGrid
import SimpleITK as sitk

from ParameterMapService import ParameterMapService


class AmsafExecutor(object):
    def __init__(self, parameterMapServiceInjectable=ParameterMapService):
        super(AmsafExecutor, self).__init__()
        self._refGroundTruthImage = None
        self._refGroundTruthSeg = None
        self._targetGroundTruthImage = None
        self._targetGroundTruthSeg = None
        self._parameterPriors = None
        self._segResultsCollection = []
        self._parameterMapService = parameterMapServiceInjectable()

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
    def segResultsCollection(self):
        return self._segResultsCollection

    @segResultsCollection.setter
    def segResultsCollection(self, value):
        self._segResultsCollection = value

    @property
    def parameterMapService(self):
        return self._parameterMapService

    @parameterMapService.setter
    def parameterMapService(self, value):
        self._parameterMapService = value

    ###########
    # Methods #
    ###########

    def findTransformParameterMap(self, parameterMapVec):
        # type: ([sitk.ParameterMap]) -> sitk.ParameterMap

        # Initialize Elastix registration
        elastixImageFilter = sitk.ElastixImageFilter()
        elastixImageFilter.SetFixedImage(self.targetGroundTruthImage)
        elastixImageFilter.SetMovingImage(self.refGroundTruthImage)
        elastixImageFilter.SetParameterMap(parameterMapVec[0])
        elastixImageFilter.AddParameterMap(parameterMapVec[1])
        elastixImageFilter.AddParameterMap(parameterMapVec[2])

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

        # Cast voxel types to make images comparable
        resultSeg = sitk.Cast(transformixImageFilter.GetResultImage(), self.refGroundTruthSeg.GetPixelID())

        # Copy header information to make images comparable
        self.targetGroundTruthSeg.CopyInformation(resultSeg)

        return resultSeg

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

    def execute(self):
        # type: () -> [(sitk.ParameterMap, float)]

        for pMapVec in self.parameterMapService.generateParameterMaps(self.parameterPriors):
            # Register images to find transformation parameters
            transformParameterMapVec = self.findTransformParameterMap(pMapVec)

            # Transform ref segmentation
            resultSeg = self.findResultSeg(transformParameterMapVec)

            # Quantify segmentation accuracy
            segScore = self.subtractionScore(resultSeg)

            # append registration parameters and corresponding score to a list
            self.segResultsCollection.append((pMapVec, segScore))

    def getTopNResults(self, n):
        return heapq.nlargest(n, self.segResultsCollection, key=lambda x: x[1])  # return the n best results


