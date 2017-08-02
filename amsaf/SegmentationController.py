import SimpleITK as sitk

from AbstractImageSegContainer import AbstractImageSegContainer
from RegistrationService import RegistrationService
from TransformSegmentationService import TransformSegmentationService
from EvaluateSegmentationService import EvaluateSegmentationService

# TODO(Ian): Find a better way to implement this
MAX_ITERATIONS = 512

class SegmentationController(AbstractImageSegContainer):
    def GenerateParameterMap(self):
        # TODO(Ian): Include parameter map generation logic and return appropriate value
        return sitk.ParameterMap()

    def Execute(self):
        registrationService = RegistrationService()
        transformSegmentationService = TransformSegmentationService()
        evaluateSegmentationService = EvaluateSegmentationService()

        for i in xrange(MAX_ITERATIONS):
            # Registration service provides transform parameter map
            transformParameterMap = registrationService.Execute(
                self.targetImageSliceGroundTruth, self.referenceImageSliceGroundTruth, self.GenerateParameterMap()
            )

            # TransformSegmentationService applies transform and returns result segmentation
            resultSegmentation = transformSegmentationService.Execute(
                self.referenceImageSegGroundTruth, transformParameterMap
            )

            # TODO(Ian): EvaluateSegmentationService evaluates results

        # TODO(Ian): Return Top N result parameter maps



