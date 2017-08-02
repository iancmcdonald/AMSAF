from abc import ABCMeta, abstractmethod


class AbstractEvaluator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def eval(self, autoseg, groundtruth):
        """An inherited abstract method that handles the evaluation of automated segmentation quality

        Args:
            autoseg: 
            groundtruth:
        """
        pass

