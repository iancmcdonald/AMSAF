import SimpleITK as sitk


class AmsafImageFilter(object):
    """ Public interface for executing AMSAF segmentation.

    Public Methods:
        SetReferenceImage,
        SetReferenceImageSeg,
        SetTargetImage,
        SetTargetImageSegGroundTruth,
        SetParameterPriors,
        Execute,
        GetResultSeg,
        GetResultParameterMap
    """
    def __init__(self):
        super(AmsafImageFilter, self).__init__()

        # Private [SimpleITK.SimpleITK.Image] holding slices of reference image
        self._referenceImage = None

        # Private [SimpleITK.SimpleITK.Image] holding slices of reference segmentation image
        self._referenceImageSeg = None

        # Private [SimpleITK.SimpleITK.Image] holding slices of target image
        self._targetImage = None

        # Private SimpleITK.SimpleITK.Image holding the target image's ground truth segmentation slice
        self._targetImageSegGroundTruth = None

        # Private [(String, String)] holding known parameters values to constrain registration/segmentation
        self._parameterPriors = None

        # Private [SimpleITK.SimpleITK.Image] holding slices of result segmentation
        self._resultSeg = None

        # Private SimpleITK.SimpleITK.ParameterMap parameter map associated with result segmentation
        self._resultParameterMap = None

    def SetReferenceImage(self, referenceImageList):
        """Set reference image.

        Args:
            referenceImage ([SimpleITK.SimpleITK.Image]): List of articulation slices of reference image to be used in
                segmentation. Each slice should have a corresponding segmentation slice.
        """
        self._referenceImage = referenceImageList

    def SetReferenceImageSeg(self, referenceImageSeg):
        """Set segmentation for reference image.

        Args:
            referenceImageSeg ([SimpleITK.SimpleITK.Image]): List of articulation slices of segmentation corresponding
                to the reference image.
        """
        self._referenceImageSeg = referenceImageSeg

    def SetTargetImage(self, targetImage):
        """Set target image.

        Args:
            targetImage ([SimpleITK.SimpleITK.Image]): List of articulation slices of target image to be used in
                segmentation. At least one of these slices should have a corresponding segmentation slice.
        """
        self._targetImage = targetImage

    def SetTargetImageSegGroundTruth(self, targetImageSegGroundTruth):
        """Set ground truth segmentation slice for target image.

        Args:
            targetImageSegGroundTruth (SimpleITK.SimpleITK.Image): A segmentation articulation slice which will be used
                as a ground truth for evaluating segmentation quality.
        """
        self._targetImageSegGroundTruth = targetImageSegGroundTruth

    def SetParameterPriors(self, parameterPriors):
        """Set known registration parameter values.

        The user might have some intuition for certain parameter values which will work best for their application.
        This method allows the user to lock in these parameters to specific values, so that they will remain constant
        while optimal values for other parameters are searched for.

        Args:
            parameterPriors (SimpleITK.SimpleITK.ParameterMap): A parameter map populated with values which will
                be treated as constants during the parameter optimization procedure.
        """
        self._parameterPriors = parameterPriors

    def Execute(self):
        """Execute segmentation.

        This method delegates the responsibility of executing the segmentation to the SegmentationController.
        The results will be available after segmentation has completed.


        """
        # SegmentationController.ExecuteSegmentation(...)
        # Assign resulting values
        pass

    def GetResultSeg(self):
        """Get resulting segmentation after execution.

        Returns:
            A SimpleITK.SimpleITK.Image which is the result segmentation after self.Execute() has completed.

        """
        return self._resultSeg

    def GetResultParameterMap(self):
        """Get resulting transformation parameter map after execution.

        Returns:
            A SimpleITK.SimpleITK.ParameterMap which is the parameter map associated with the result segmentation after
            self.Execute() has completed.

        """
        return self._resultParameterMap
