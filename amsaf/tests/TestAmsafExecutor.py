import unittest
import SimpleITK as sitk

from amsaf.ParameterMapService import *
from amsaf.AmsafExecutor import *


PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")

sub3_autoseg = sitk.ReadImage(
    "/home/daniel/mridata/Elastix/forearm/PQ_forearm_transformed_seg/transformation_result.nii")


class MyTestCase(unittest.TestCase):

    def test_injected_param_map(self):
        amsafExecutor = AmsafExecutor(ParameterMapService)
        amsafExecutor.targetGroundTruthImage = sub3_forearm_img_cropped
        amsafExecutor.refGroundTruthImage = PQ_forearm_img_cropped
        amsafExecutor.targetGroundTruthSeg = sub3_forearm_muscles_ground_truth
        amsafExecutor.refGroundTruthSeg = PQ_forearm_muscles
        amsafExecutor.execute()

        topTwo = amsafExecutor.getTopNResults(2)

        for i, (pMap, segScore) in enumerate(topTwo):
            writeFileName = 'SegResult.' + str(i) + '.txt'
            sitk.WriteParameterFile(pMap, writeFileName)
            f = open(writeFileName, 'a')
            f.write('score: ' + str(segScore) + '\n')
            f.close()
        self.assertEqual(True, True)

    def testSubtractionScore(self):
        # subtracts the same file from each other, checks for equality
        amsafExecutor = AmsafExecutor(ParameterMapService)
        amsafExecutor.targetGroundTruthSeg = PQ_forearm_muscles
        subtractScore = amsafExecutor.subtractionScore(PQ_forearm_muscles)
        self.assertEqual(subtractScore, 20580483.0)

    def testSubtractionScore1(self):
        # takes an image, and subtracts a blank image from it
        amsafExecutor = AmsafExecutor(ParameterMapService)
        amsafExecutor.targetGroundTruthSeg = PQ_forearm_muscles
        blankImg = sitk.Image(371, 451, 123, 3)
        subtractScore = amsafExecutor.subtractionScore(blankImg)
        self.assertEqual(subtractScore, 18476727.0)

    def testDiceScore(self):
        amsafExecutor = AmsafExecutor(ParameterMapService)
        amsafExecutor.targetGroundTruthSeg = sub3_forearm_muscles_ground_truth
        dice = amsafExecutor.diceScore(sub3_forearm_muscles_ground_truth)
        self.assertEqual(dice, 1.0)
        autoseg = sub3_autoseg
        autoseg = sitk.Cast(autoseg, amsafExecutor.targetGroundTruthSeg.GetPixelID())
        print(amsafExecutor.targetGroundTruthSeg.GetPixelIDValue())
        print(autoseg.GetPixelIDValue())
        diceScore2 = amsafExecutor.diceScore(autoseg)
        print(diceScore2)



if __name__ == '__main__':
    unittest.main()
