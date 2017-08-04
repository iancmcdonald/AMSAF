from itertools import imap
from random import randint

import SimpleITK as sitk
from sklearn.model_selection import ParameterGrid

from amsaf.amsaf_functional import optimize_parameter_map

img = sitk.ReadImage("/home/ian/Programming/HART/mri_data/SUBJECT 3/2-forearm/2-forearm_for_ITK-SNAP.nii",
                     sitk.sitkFloat32)

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")


def generate_parameter_map():
    # TODO(Ian): Use grid search or some other means to generate parameter map. Think closures.
    elastix_params = {'a': [1, 2], 'b': [True, False]}  # parameters go here
    param_grid = ParameterGrid(elastix_params)

    for pmap in param_grid:
        yield pmap


print(optimize_parameter_map(PQ_forearm_img_cropped, PQ_forearm_muscles, sub3_forearm_img_cropped,
                             sub3_forearm_muscles_ground_truth, None))
