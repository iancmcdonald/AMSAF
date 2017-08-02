from CompareResults import CompareResults
from AbstractEvaluator import AbstractEvaluator


class SegmentationEval(object):
    def __init__(self):
        self.evaluator = Subtract

    def evalSegmentation(self, autoseg, groundtruth, parammap):
        """ evaluates the segmentation, and stores the results in database

        Args:
            autoseg (SimpleITK.SimpleITK.Image): The automatic segmentation created from Segementer component
            groundtruth (SimpleITK.SimpleITK.Image): The manual segmentation ground truth
            parammap (SimpleITK.SimpleITK.Image): The parameter map used to produce the auto segmentation
        """
        evalResults = self.evaluator.eval(autoseg, groundtruth)
        return CompareResults.AddItem(parammap, evalResults)


    def returnBestParamMap(self):
        """ Retrieves the best/highest priority parameter map stored in current database

        Returns: SimpleITK.SimpleITK.ParameterMap

        """
        return CompareResults.GetHighest()

    def getSegScore(self, autoseg, groundtruth):
        """only evaluates the segmentation and returns the numerical result

        Args:
            autoseg (SimpleITK.SimpleITK.Image): Automatic segmentation created from Segmenter component
            groundtruth (SimpleITK.SimpleITK.Image): The manual segmentation ground truth
        """





