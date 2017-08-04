from abc import ABCMeta, abstractmethod


class AbstractEvaluator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def eval(self, autoseg, groundtruth):
        """An inherited abstract method that handles the evaluation of automated segmentation quality
        and it should return the rating describing the quality of the autoseg input

        Args:
            autoseg (SimpleITK.SimpleITK.Image): Automatically segmented image
            groundtruth (SimpleITK.SimpleITK.Image): The ground truth segmentation img
        """
        pass

