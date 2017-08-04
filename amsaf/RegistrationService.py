import SimpleITK as sitk

from AbstractImageSegContainer import AbstractImageSegContainer


class RegistrationService(AbstractImageSegContainer):
    def Execute(self, targetImage, referenceImage, registrationParameterMap):
        """

        Args:
            targetImage ([SimpleITK.SimpleITK.Image]):
            referenceImage ([SimpleITK.SimpleITK.Image]):
            registrationParameterMap (SimpleITK.SimpleITK.ParameterMap):

        Returns:
            SimpleITK.SimpleITK.ParameterMap

        """

        elastixImageFilter = sitk.ElastixImageFilter()

        elastixImageFilter.SetFixedImage(targetImage)
        elastixImageFilter.SetMovingImage(referenceImage)
        elastixImageFilter.SetParameterMap(registrationParameterMap)
        elastixImageFilter.Execute()

        return elastixImageFilter.GetTransformParameterMap()
