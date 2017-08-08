from itertools import imap
from itertools import islice

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
    """

    Args:
        moving_image:
        transform_parameter_map:

    Returns: SimpleITK.SimpleITK.Image

    """
    transform_parameter_map_vec = transform_parameter_map[0]
    transform_parameter_map_vec['ResampleInterpolator'] = ['FinalNearestNeighborInterpolator']
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
        subtractedImage = ground_truth - seg
        return subtractedImage

    def count_zeros(img):
        """Adding up the number of nonzero values resulting from subtracting segmentation images
        Args:
            img (SimpleITK.SimpleITK.Image): subtracted segmentation image
        Returns: Integer
        """
        statFilter = sitk.StatisticsImageFilter()
        statFilter.Execute(img == 0)
        return statFilter.GetSum()

    return count_zeros(subtract_images())


def dice_evaluator(ground_truth, seg):
    overlapFilter = sitk.LabelOverlapMeasuresImageFilter()
    overlapFilter.Execute(ground_truth, seg)
    return overlapFilter.GetDiceCoefficient()


def generate_parameter_maps(priors=None):
    # priors is a list of tuples [()]
    def get_parameter_options_dict(transform):
        if transform == 'rigid':
            param_grid = {
                'AutomaticParameterEstimation': ['true'],
                'AutomaticTransformInitialization': ['true'],
                'AutomaticTransformInitializationMethod': ['CenterOfGravity', 'Origins', 'GeometricalCenter',
                                                           'GeometryTop'],
                'BSplineInterpolationOrder': ['1', '3'],
                'CheckNumberOfSamples': ['true'],
                'DefaultPixelValue': ['0'],
                'FinalBSplineInterpolationOrder': ['3'],
                'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
                'ImagePyramidSchedule': ['2 2 1', '4 4 1  2 2 1  1 1 1', '32 32 2  16 16 2',
                                         '16 16 2  8 8 1  4 4 1  2 2 1  1 1 1'],
                'Interpolator': ['BSplineInterpolator'],
                'MaximumNumberOfIterations': ['512', '1024', '2048'],
                'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                           'NormalizedMutualInformation'],
                'NumberOfHistogramBins': ['32', '64', '128', '16 32 64', '64 32 16'],
                'NumberOfResolutions': ['1', '2', '3', '6'],
                'NumberOfSpatialSamples': ['2000', '4000', '8000'],
                'Registration': ['MultiResolutionRegistration'],
                'Resampler': ['DefaultResampler'],
                'ResampleInterpolator': ['FinalBSplineInterpolator']
            }

            if priors:
                for key, val in priors:
                    param_grid[key] = [val]

            return param_grid

    def convert_to_elastix(param_dict):
        # type: (dict) -> sitk.ParameterMap
        elastix_param_map = sitk.GetDefaultParameterMap('rigid')
        for param, val in param_dict.iteritems():
            elastix_param_map[param] = [val]

        return elastix_param_map

    param_grid = ParameterGrid(get_parameter_options_dict('rigid'))

    for param_map in param_grid:
        yield convert_to_elastix(param_map)


def optimize_parameter_map(ref_image_ground_truth_crop, ref_seg_ground_truth_crop, target_image_ground_truth_crop,
                           target_seg_ground_truth_crop, parameter_priors=None):
    def process_seg_result(ground_truth, seg):
        processed_seg = sitk.Cast(seg, ground_truth.GetPixelID())
        ground_truth.CopyInformation(processed_seg)
        return processed_seg

    def get_seg_score_and_transform_parameter_map(parameter_map):
        transform_parameter_map = get_transform_parameter_map(target_image_ground_truth_crop,
                                                              ref_image_ground_truth_crop, parameter_map)
        result_seg = apply_transformation(ref_seg_ground_truth_crop, transform_parameter_map)

        processed_result_seg = process_seg_result(target_seg_ground_truth_crop, result_seg)

        seg_score = dice_evaluator(target_seg_ground_truth_crop, processed_result_seg)

        return seg_score, parameter_map

    # TODO(Ian): Replace imap with numap or Multiprocess imap

    best_parameter_map = max(imap(get_seg_score_and_transform_parameter_map, islice(generate_parameter_maps(), 3)),
                             key=lambda pair: pair[0])

    return best_parameter_map
