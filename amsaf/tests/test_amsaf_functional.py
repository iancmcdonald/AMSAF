import unittest
from amsaf.amsaf_functional import *

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")

test_img1 = sitk.ReadImage("/home/daniel/mridata/UnitTest/combined_seg.nii")

test_img2 = sitk.ReadImage("/home/daniel/mridata/UnitTest/transformation_result.nii")
class TestAmsafFunctional(unittest.TestCase):
    # def test_get_transform_parameter_map(self):
    #     parameter_map = sitk.GetDefaultParameterMap('rigid')
    #     parameter_map['AutomaticTransformInitialization'] = ['true']
    #     get_transform_parameter_map(sub3_forearm_img_cropped, PQ_forearm_img_cropped, parameter_map)
    #
    #     self.assertEqual(True, False)

    def test_subtraction_evaluator(self):
        # Note: Dimensions are 294 x 871 x 305

        # Current problem: It looks like the double values are maxing out (1.7e+308), and Dice will become inf
        autoseg = test_img2
        groundtruth = sitk.Image(294, 871, 305, 3)
        groundtruth.SetOrigin(autoseg.GetOrigin())
        groundtruth.SetSpacing(autoseg.GetSpacing())
        groundtruth.SetDirection(autoseg.GetDirection())
        expected = subtraction_evaluator(groundtruth, autoseg)
        self.assertEqual(expected, 78102570)

    # def test_identity(self):
    #     identity = test_img1 - test_img2
    #     self.assertEqual(identity, test_img1)


if __name__ == '__main__':
    unittest.main()
