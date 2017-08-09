from itertools import imap

import SimpleITK as sitk
from sklearn.model_selection import ParameterGrid


def get_transform_parameter_map(fixed_image, moving_image, parameter_maps):
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(fixed_image)
    elastixImageFilter.SetMovingImage(moving_image)
    elastixImageFilter.SetParameterMap(parameter_maps[0])
    elastixImageFilter.AddParameterMap(parameter_maps[1])
    elastixImageFilter.AddParameterMap(parameter_maps[2])

    elastixImageFilter.Execute()

    return elastixImageFilter.GetTransformParameterMap()


def apply_transformation(moving_image, transform_parameter_map_vec):
    """

    Args:
        moving_image:
        transform_parameter_map_vec:

    Returns: SimpleITK.SimpleITK.Image

    """
    for t_map in transform_parameter_map_vec:
        t_map['ResampleInterpolator'] = ['FinalNearestNeighborInterpolator']

    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transform_parameter_map_vec)
    transformixImageFilter.SetMovingImage(moving_image)
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


def get_parameter_options_dict(transform, priors=None):
    # priors is a list of tuples [()]
    if transform == 'rigid':
        param_grid = {
            'AutomaticParameterEstimation': ['true'],
            'AutomaticTransformInitialization': ['true'],
            'BSplineInterpolationOrder': ['1', '3'],
            'CheckNumberOfSamples': ['true'],
            'DefaultPixelValue': ['0'],
            'FinalBSplineInterpolationOrder': ['3'],
            'FixedImagePyramid': ['FixedSmoothingImagePyramid', 'FixedRecursiveImagePyramid'],
            'Interpolator': ['BSplineInterpolator'],
            'MaximumNumberOfIterations': ['512' '1024' '2048'],
            'Metric': ['AdvancedMattesMutualInformation', 'AdvancedNormalizedCorrelation',
                       'NormalizedMutualInformation'],
            'NumberOfHistogramBins': ['32', '64'],
            'NumberOfResolutions': ['3', '6'],
            'NumberOfSpatialSamples': ['2000'],
            'Registration': ['MultiResolutionRegistration'],
            'Resampler': ['DefaultResampler'],
            'ResampleInterpolator': ['FinalBSplineInterpolator']
        }
    elif transform == 'affine':
        param_grid = {
            'MaximumNumberOfIterations': ['512', '1024', '2048'],
            'Interpolator': ['LinearInterpolator', 'BSplineInterpolator'],
            'NumberOfHistogramBins': ['32', '64']
        }
    elif transform == 'bspline':
        param_grid = {
            'AutomaticParameterEstimation': ['true'],
            'FinalGridSpacingInPhysicalUnits': ['2', '4', '8'],
            'MaximumNumberofIterations': ['512', '1024', '2048'],
            'NumberOfHistogramBins': ['32', '64']
        }
    else:
        raise ValueError

    if priors and param_grid:
        for key, val in priors:
            param_grid[key] = [val]

    return param_grid


def convert_to_elastix(rigid_param_dict, affine_param_dict, bspline_param_dict):
    # type: (dict) -> [sitk.ParameterMap]

    def edit_map(param_dict, param_map):
        for param, val in param_dict.iteritems():
            param_map[param] = [val]
        return param_map

    rigid_param_map = edit_map(rigid_param_dict, sitk.GetDefaultParameterMap('rigid'))
    affine_param_map = edit_map(affine_param_dict, sitk.GetDefaultParameterMap('affine'))
    bspline_param_map = edit_map(bspline_param_dict, sitk.GetDefaultParameterMap('bspline'))

    return [rigid_param_map, affine_param_map, bspline_param_map]


def generate_parameter_maps(ref_image_ground_truth_crop, ref_seg_ground_truth_crop,
                            target_image_ground_truth_crop,
                            target_seg_ground_truth_crop):
    rigid_param_grid = ParameterGrid(get_parameter_options_dict('rigid'))
    affine_param_grid = ParameterGrid(get_parameter_options_dict('affine'))
    bspline_param_grid = ParameterGrid(get_parameter_options_dict('bspline'))

    for bspline_param_map in bspline_param_grid:
        for affine_param_map in affine_param_grid:
            for rigid_param_map in rigid_param_grid:
                yield ref_image_ground_truth_crop, ref_seg_ground_truth_crop, target_image_ground_truth_crop, \
                      target_seg_ground_truth_crop, convert_to_elastix(rigid_param_map, affine_param_map,
                                                                       bspline_param_map)


def process_seg_result(ground_truth, seg):
    processed_seg = sitk.Cast(seg, ground_truth.GetPixelID())
    ground_truth.CopyInformation(processed_seg)
    return processed_seg


def get_seg_score_and_transform_parameter_map(params):
    ref_image_ground_truth_crop, ref_seg_ground_truth_crop, target_image_ground_truth_crop, \
    target_seg_ground_truth_crop, parameter_maps = params

    transform_parameter_map = get_transform_parameter_map(target_image_ground_truth_crop,
                                                          ref_image_ground_truth_crop, parameter_maps)

    result_seg = apply_transformation(ref_seg_ground_truth_crop, transform_parameter_map)

    processed_result_seg = process_seg_result(target_seg_ground_truth_crop, result_seg)

    seg_score = dice_evaluator(target_seg_ground_truth_crop, processed_result_seg)

    return seg_score, parameter_maps


def optimize_parameter_map(ref_image_ground_truth_crop, ref_seg_ground_truth_crop, target_image_ground_truth_crop,
                           target_seg_ground_truth_crop, parameter_priors=None):
    # TODO(Ian): Replace imap with numap or Multiprocess imap

    seg_score, best_parameter_maps = max(imap(get_seg_score_and_transform_parameter_map,
                                              generate_parameter_maps(ref_image_ground_truth_crop,
                                                                      ref_seg_ground_truth_crop,
                                                                      target_image_ground_truth_crop,
                                                                      target_seg_ground_truth_crop)),
                                         key=lambda pair: pair[0])

    sitk.WriteParameterFile(best_parameter_maps, 'best_parameter_map.txt')
    return seg_score, best_parameter_maps
