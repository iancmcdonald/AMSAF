from itertools import imap

import SimpleITK as sitk
from sklearn.model_selection import ParameterGrid


def get_transform_parameter_map(fixed_image, moving_image, parameter_map):
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(fixed_image)
    elastixImageFilter.SetMovingImage(moving_image)
    elastixImageFilter.SetParameterMap(parameter_map)

    elastixImageFilter.Execute()

    return elastixImageFilter.GetTransformParameterMap()


def apply_transformation(moving_image, transform_parameter_map):
    transform_parameter_map = transform_parameter_map[0]
    transform_parameter_map['ResampleInterpolator'] = ['FinalNearestNeighborInterpolator']
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetMovingImage(moving_image)
    transformixImageFilter.SetTransformParameterMap(transform_parameter_map)
    transformixImageFilter.Execute()

    return transformixImageFilter.GetResultImage()


def subtraction_evaluator(ground_truth, seg):
    def subtract_images():
        """Subtracts the automated segmentation with the ground truth segmentation
        Args:
            autoseg:
            groundtruth:
        Returns: (SimpleITK.SimpleITK.Image) of the automated segmentation subtracted with the ground truth seg
        """
        seg_casted = sitk.Cast(seg, ground_truth.GetPixelID())
        subtractedImage = ground_truth - seg_casted
        return subtractedImage

    def count_zeros(img):
        """Adding up the number of zero values resulting from subtracting segmentation images
        Args:
            img (SimpleITK.SimpleITK.Image): subtracted segmentation image
        Returns: Integer
        """
        statFilter = sitk.StatisticsImageFilter()
        statFilter.Execute(img == 0)
        return statFilter.GetSum()

    # return count_zeros(subtract_images())
    overlapFilter = sitk.LabelOverlapMeasuresImageFilter()
    seg_casted = sitk.Cast(seg, ground_truth.GetPixelID())
    overlapFilter.Execute(ground_truth, seg_casted)
    return overlapFilter.GetDiceCoefficient()


def generate_parameter_map():
    # elastix_params = {}  # parameters go here
    # param_grid = ParameterGrid(elastix_params)
    translation_map = sitk.GetDefaultParameterMap('rigid')
    translation_map['AutomaticTransformInitialization'] = ['true']
    param_grid = [translation_map]

    for param_map in param_grid:
        yield param_map


def optimize_parameter_map(ref_image_ground_truth_crop, ref_seg_ground_truth_crop, target_image_ground_truth_crop,
                           target_seg_ground_truth_crop, parameter_priors):
    def get_seg_score_and_transform_parameter_map(parameter_map):
        transform_parameter_map = get_transform_parameter_map(target_image_ground_truth_crop,
                                                              ref_image_ground_truth_crop, parameter_map)
        print("registration finished")

        result_seg = apply_transformation(ref_seg_ground_truth_crop, transform_parameter_map)

        print("transformation applied")

        sitk.WriteImage(target_seg_ground_truth_crop, "target_ground_truth_seg.nii")
        sitk.WriteImage(result_seg, "result_seg.nii")

        seg_score = subtraction_evaluator(target_seg_ground_truth_crop, result_seg)

        return seg_score, transform_parameter_map

    # TODO(Ian): Replace imap with numap or Multiprocess imap
    best_parameter_map = max(imap(get_seg_score_and_transform_parameter_map, generate_parameter_map()),
                             key=lambda pair: pair[0])

    return best_parameter_map
