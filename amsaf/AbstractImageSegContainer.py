class AbstractImageSegContainer(object):
    """Abstract base class providing core getter/setter functionality for other AMSAF classes.

    Methods:
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
        super(AbstractImageSegContainer, self).__init__()

        # Private [SimpleITK.SimpleITK.Image] holding slices of reference image
        self._referenceImage = None

        # Private [SimpleITK.SimpleITK.Image] holding slices of reference segmentation image
        self._referenceImageSeg = None

        # Private [SimpleITK.SimpleITK.Image] holding slices of target image
        self._targetImage = None

        # Private SimpleITK.SimpleITK.Image holding the target image's ground truth segmentation slice
        self._targetImageSegGroundTruth = None

        # Private SimpleITK.SimpleITK.Image holding the target image's ground truth MR image slice.
        # This should be the image corresponding to the ground truth segmentation for the target image.
        self._targetImageSliceGroundTruth = None

        # Private SimpleITK.SimpleITK.Image holding the reference image segmentation corresponding to the target
        # image's ground truth slice
        self._referenceImageSegGroundTruth = None

        # Private SimpleITK.SimpleITK.Image holding the reference image slice corresponding to the target image's
        # ground truth slice
        self._referenceImageSliceGroundTruth = None

        # Private [(String, String)] holding known parameters values to constrain registration/segmentation
        self._parameterPriors = None

        # Private [SimpleITK.SimpleITK.Image] holding slices of result segmentation
        self._resultSeg = None

        # Private SimpleITK.SimpleITK.ParameterMap parameter map associated with result segmentation
        self._resultParameterMap = None

    @property
    def referenceImage(self):
        """

        Returns:
            [SimpleITK.SimpleITK.Image]

        """
        return self._referenceImage

    @referenceImage.setter
    def referenceImage(self, value):
        """Set reference image.

        Args:
            value ([SimpleITK.SimpleITK.Image]): List of articulation slices of reference image to be used
                in segmentation. Each slice should have a corresponding segmentation slice.
        """
        self._referenceImage = value

    @property
    def referenceImageSeg(self):
        """

        Returns:
            [SimpleITK.SimpleITK.Image]

        """
        return self._referenceImageSeg

    @referenceImageSeg.setter
    def referenceImageSeg(self, value):
        """Set segmentation for reference image.

        Args:
            value ([SimpleITK.SimpleITK.Image]): List of articulation slices of segmentation corresponding
                to the reference image.
        """
        self._referenceImageSeg = value

    @property
    def targetImage(self):
        """

        Returns:
            [SimpleITK.SimpleITK.Image]

        """
        return self._targetImage

    @targetImage.setter
    def targetImage(self, value):
        """Set target image.

        Args:
            value ([SimpleITK.SimpleITK.Image]): List of articulation slices of target image to be used in
                segmentation. At least one of these slices should have a corresponding segmentation slice.
        """
        self._targetImage = value

    @property
    def targetImageSegGroundTruth(self):
        """

        Returns:
            SimpleITK.SimpleITK.Image

        """
        return self._targetImageSegGroundTruth

    @targetImageSegGroundTruth.setter
    def targetImageSegGroundTruth(self, value):
        """Set ground truth segmentation slice for target image.

        Args:
            value (SimpleITK.SimpleITK.Image): A segmentation articulation slice which will be used
                as a ground truth for evaluating segmentation quality.
        """
        self._targetImageSegGroundTruth = value

    @property
    def targetImageSliceGroundTruth(self):
        """Get target image slice corresponding to ground truth segmentation.

        Returns:
            SimpleITK.SimpleITK.Image

        """
        return self._targetImageSliceGroundTruth

    @targetImageSliceGroundTruth.setter
    def targetImageSliceGroundTruth(self, value):
        """Set target image slice corresponding to ground truth segmentation.

        Args:
            value (SimpleITK.SimpleITK.Image): The slice of the target image corresponding to the ground truth
                segmentation.
        """
        self._targetImageSliceGroundTruth = value

    @property
    def referenceImageSegGroundTruth(self):
        """Get reference image segmentation corresponging to target image ground truth.

        Returns:
            SimpleITK.SimpleITK.Image

        """
        return self._referenceImageSegGroundTruth

    @referenceImageSegGroundTruth.setter
    def referenceImageSegGroundTruth(self, value):
        """Set reference image segmentation corresponding to target image ground truth.

        Args:
            value (SimpleITK.SimpleITK.Image):
        """
        self._referenceImageSegGroundTruth = value

    @property
    def referenceImageSliceGroundTruth(self):
        """Get reference image slice corresponding to target ground truth.

        Returns:
            SimpleITK.SimpleITK.Image

        """
        return self._referenceImageSliceGroundTruth

    @referenceImageSliceGroundTruth.setter
    def referenceImageSliceGroundTruth(self, value):
        """Set reference image slice corresponding to target ground truth.

        Args:
            value (SimpleITK.SimpleITK.Image): Target image slice corresponding to target ground truth.
        """
        self._referenceImageSliceGroundTruth = value

    @property
    def parameterPriors(self):
        """

        Returns:
            SimpleITK.SimpleITK.ParameterMap

        """
        return self._parameterPriors

    @parameterPriors.setter
    def parameterPriors(self, value):
        """Set known registration parameter values.

        The user might have some intuition for certain parameter values which will work best for their application.
        This method allows the user to lock in these parameters to specific values, so that they will remain constant
        while optimal values for other parameters are searched for.

        Args:
            value (SimpleITK.SimpleITK.ParameterMap): A parameter map populated with values which will
                be treated as constants during the parameter optimization procedure.
        """
        self._parameterPriors = value

    @property
    def resultParameterMap(self):
        """Get resulting transformation parameter map after execution.

        Returns:
            A SimpleITK.SimpleITK.ParameterMap which is the parameter map associated with the result segmentation after
            self.Execute() has completed.

        """
        return self._resultParameterMap

    @resultParameterMap.setter
    def resultParameterMap(self, value):
        self._resultParameterMap = value

    @property
    def resultSeg(self):
        """Get resulting segmentation after execution.

        Returns:
            A [SimpleITK.SimpleITK.Image] which is the result segmentation after self.Execute() has completed.

        """
        return self._resultSeg

    @resultSeg.setter
    def resultSeg(self, value):
        """Set resulting segmentation after execution.

        Args:
            value ([SimpleITK.SimpleITK.Image]):
        """
        self._resultSeg = value

    def InjectProperties(self, other):
        """Inject this object's properties into another object.

        This injection is used to support the service-oriented structure of AMSAF.

        Args:
            other (AbstractImageSegContainer): An object which inherits from AbstractImageSegContainer.
        """

        other.referenceImage = self.referenceImage
        other.referenceImageSeg = self.referenceImageSeg
        other.targetImage = self.targetImage
        other.targetImageSegGroundTruth = self.targetImageSegGroundTruth
        other.targetImageSliceGroundTruth = self.targetImageSliceGroundTruth
        other.referenceImageSliceGroundTruth = self.referenceImageSliceGroundTruth
        other.referenceImageSegGroundTruth = self.referenceImageSegGroundTruth
        other.parameterPriors = self.parameterPriors
