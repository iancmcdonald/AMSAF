from AbstractImageSegContainer import AbstractImageSegContainer
import SimpleITK as sitk

class TransformSegmentationService(AbstractImageSegContainer):
    def Execute(self, referenceImageSeg, transformParameterMap):
        transformixImageFilter = sitk.TransformixImageFilter()
        transformixImageFilter.SetMovingImage(referenceImageSeg)
        transformixImageFilter.SetTransformParameterMap(transformParameterMap)
        transformixImageFilter.Execute()

        return transformixImageFilter.GetResultImage()

