import unittest

from amsaf.amsaf_functional import *

from test_data.mr_images import PQ_forearm_img_cropped
from test_data.mr_images import sub3_forearm_img_cropped

from test_data.segmentations import PQ_forearm_muscles
from test_data.segmentations import sub3_forearm_muscles_ground_truth


def setup():
    parameter_map = sitk.GetDefaultParameterMap('rigid')
    parameter_map['AutomaticTransformInitialization'] = ['true']
    transform_parameter_map_rigid = get_transform_parameter_map(sub3_forearm_img_cropped, PQ_forearm_img_cropped,
                                                                parameter_map)
    result_image = apply_transformation(PQ_forearm_muscles, transform_parameter_map_rigid)

    result_image = sitk.Cast(result_image, sub3_forearm_muscles_ground_truth.GetPixelID())
    sub3_forearm_muscles_ground_truth.CopyInformation(result_image)

    return transform_parameter_map_rigid, result_image

test_img1 = sitk.ReadImage("/home/daniel/mridata/UnitTest/combined_seg.nii")

test_img2 = sitk.ReadImage("/home/daniel/mridata/UnitTest/transformation_result.nii")
class TestAmsafFunctional(unittest.TestCase):
<<<<<<< HEAD
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
=======
    def test_get_transform_parameter_map(self):
        parameter_map = sitk.GetDefaultParameterMap('rigid')
        parameter_map['AutomaticTransformInitialization'] = ['true']
        transform_parameter_map = get_transform_parameter_map(sub3_forearm_img_cropped, PQ_forearm_img_cropped,
                                                              parameter_map)
        self.assertTrue(transform_parameter_map, sitk.PrintParameterMap(transform_parameter_map))

    def test_apply_transformation(self):
        transform_parameter_map = setup()[0]
        result_image = apply_transformation(PQ_forearm_muscles, transform_parameter_map)
        self.assertEqual(sub3_forearm_img_cropped.GetSize(), result_image.GetSize())

    def test_dice_evaluator(self):
        seg_result = setup()[1]
        dice_score = dice_evaluator(sub3_forearm_muscles_ground_truth, seg_result)
        self.assertTrue(dice_score)

    def test_subtraction_evaluator(self):
        seg_result = setup()[1]
        sub_score = subtraction_evaluator(sub3_forearm_muscles_ground_truth, seg_result)
        self.assertTrue(sub_score)
>>>>>>> 2571f83bb9bc681a6e1defa06b37e303c62cbbd5


if __name__ == '__main__':
    unittest.main()
