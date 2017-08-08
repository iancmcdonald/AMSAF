from itertools import imap
from random import randint

import SimpleITK as sitk
from sklearn.model_selection import ParameterGrid

from amsaf.amsaf_functional import optimize_parameter_map

# img = sitk.ReadImage("/home/ian/Programming/HART/mri_data/SUBJECT 3/2-forearm/2-forearm_for_ITK-SNAP.nii",
#                      sitk.sitkFloat32)

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")

if __name__ == '__main__':
    print(optimize_parameter_map(PQ_forearm_img_cropped, PQ_forearm_muscles, sub3_forearm_img_cropped,
                                 sub3_forearm_muscles_ground_truth, None))
    # print("hello from server!")
