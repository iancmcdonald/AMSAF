from AbstractImageSegContainer import AbstractImageSegContainer
from SegmentationController import SegmentationController


class AmsafImageFilter(AbstractImageSegContainer):
    """ Public interface for executing AMSAF segmentation.

    Explicit getters and setters wrap inherited getters and setters to provide interface consistency with SimpleITK and
    SimpleElastix. See AbstractImageSegContainer for implementation and type information.

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

    def SetReferenceImage(self, value):
        """Set reference image.

        Args:
            value ([SimpleITK.SimpleITK.Image]): List of articulation slices of reference image to be used
                in segmentation. Each slice should have a corresponding segmentation slice.
        """
        self.referenceImage = value

    def SetReferenceImageSeg(self, value):
        """Set segmentation for reference image.

        Args:
            value ([SimpleITK.SimpleITK.Image]): List of articulation slices of segmentation corresponding
                to the reference image.
        """
        self.referenceImageSeg = value

    def SetTargetImage(self, value):
        """Set target image.

        Args:
            value ([SimpleITK.SimpleITK.Image]): List of articulation slices of target image to be used in
                segmentation. At least one of these slices should have a corresponding segmentation slice.
        """
        self.targetImage = value

    def SetTargetImageSegGroundTruth(self, value):
        """Set ground truth segmentation slice for target image.

        Args:
            value (SimpleITK.SimpleITK.Image): A segmentation articulation slice which will be used
                as a ground truth for evaluating segmentation quality.
        """
        self.targetImageSegGroundTruth = value

    def SetTargetImageSliceGroundTruth(self, value):
        """Set target image slice corresponding to ground truth segmentation.

        Args:
            value (SimpleITK.SimpleITK.Image): The slice of the target image corresponding to the ground truth
                segmentation.
        """
        self.targetImageSliceGroundTruth = value

    def SetReferenceImageSliceGroundTruth(self, value):
        """Set reference image slice corresponding to target ground truth.

        Args:
            value (SimpleITK.SimpleITK.Image): Target image slice corresponding to target ground truth.
        """
        self.referenceImageSliceGroundTruth = value

    def SetReferenceImageSegGroundTruth(self, value):
        """Set reference image segmentation corresponding to target ground truth.

        Args:
            value (SimpleITK.SimpleITK.Image): Reference image segmentation corresponding to target ground truth.
        """
        self.referenceImageSegGroundTruth = value

    def SetParameterPriors(self, value):
        """Set known registration parameter values.

        The user might have some intuition for certain parameter values which will work best for their application.
        This method allows the user to lock in these parameters to specific values, so that they will remain constant
        while optimal values for other parameters are searched for.

        Args:
            value (SimpleITK.SimpleITK.ParameterMap): A parameter map populated with values which will
                be treated as constants during the parameter optimization procedure.
        """
        self.parameterPriors = value

    def Execute(self):
        """Execute AMSAF segmentation.

        """
        segmentationController = SegmentationController()
        # TODO(Ian): Override InjectProperties
        self.InjectProperties(segmentationController)
        segmentationController.Execute()

    def GetResultSeg(self):
        """Get resulting segmentation after execution.

        Returns:
            A [SimpleITK.SimpleITK.Image] which is the result segmentation after self.Execute() has completed.

        """
        return self.resultSeg

    def GetResultParameterMap(self):
        """Get resulting transformation parameter map after execution.

        Returns:
            A SimpleITK.SimpleITK.ParameterMap which is the parameter map associated with the result segmentation after
            self.Execute() has completed.

        """
        return self.resultParameterMap
