import unittest
from amsaf.amsaf_functional import *

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")


class TestAmsafFunctional(unittest.TestCase):
    def test_get_transform_parameter_map(self):
        parameter_map = sitk.GetDefaultParameterMap('rigid')
        parameter_map['AutomaticTransformInitialization'] = ['true']
        get_transform_parameter_map(sub3_forearm_img_cropped, PQ_forearm_img_cropped, parameter_map)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
