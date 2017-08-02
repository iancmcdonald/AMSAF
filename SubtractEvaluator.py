from AbstractEvaluator import AbstractEvaluator
import SimpleITK as sitk


class SubtractEvaluator(AbstractEvaluator):
    def SubtractEval(self, autoseg, groundtruth):
        """Subtracts the automated segmentation with the ground truth segmentation

        Args:
            autoseg:
            groundtruth:

        Returns: (SimpleITK.SimpleITK.Image) of the automated segmentation subtracted with the ground truth seg

        """
        subtractedImage = autoseg - groundtruth
        return subtractedImage

    def CountZeros(self, img):
        """Adding up the number of nonzero values resulting from subtracting segmentation images

        Args:
            img (SimpleITK.SimpleITK.Image): subtracted segmentation image

        Returns: Integer

        """
        statFilter = sitk.StatisticsFilter()
        statFilter.Execute(img == 0)
        return statFilter.GetSum()

    def eval(self, autoseg, groundtruth):
        return self.count_zeros(self.subtractEval(autoseg, groundtruth))