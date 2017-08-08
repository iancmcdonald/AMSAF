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


class TestAmsafFunctional(unittest.TestCase):
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

        self_dice = dice_evaluator(sub3_forearm_muscles_ground_truth, sub3_forearm_muscles_ground_truth)
        dice_score = dice_evaluator(sub3_forearm_muscles_ground_truth, seg_result)

        self.assertEqual(self_dice, 1)
        self.assertTrue(dice_score)

    def test_subtraction_evaluator(self):
        seg_result = setup()[1]

        self_sub = subtraction_evaluator(sub3_forearm_muscles_ground_truth, sub3_forearm_muscles_ground_truth)
        sub_score = subtraction_evaluator(sub3_forearm_muscles_ground_truth, seg_result)

        self.assertEqual(self_sub, sub3_forearm_muscles_ground_truth.GetNumberOfPixels())
        self.assertTrue(sub_score)


if __name__ == '__main__':
    unittest.main()
