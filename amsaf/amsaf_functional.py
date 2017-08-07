import SimpleITK as sitk
from sklearn.model_selection import ParameterGrid
from Queue import PriorityQueue


def get_transform_parameter_map(fixed_image, moving_image, parameter_map):
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(fixed_image)
    elastixImageFilter.SetMovingImage(moving_image)
    elastixImageFilter.SetParameterMap(parameter_map)
    elastixImageFilter.Execute()

    return elastixImageFilter.GetTransformParameterMap()


def apply_transformation(moving_image, transform_parameter_map):
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetMovingImage(moving_image)
    transformixImageFilter.SetTransformParameterMap(transform_parameter_map)
    transformixImageFilter.Execute()

    return transformixImageFilter.GetResultImage()


def subtraction_evaluator(ground_truth, seg):
    def subtract_images(ground_truth, result_seg):
        """Subtracts the automated segmentation with the ground truth segmentation
        Args:
            autoseg:
            groundtruth:
        Returns: (SimpleITK.SimpleITK.Image) of the automated segmentation subtracted with the ground truth seg
        """
        subtractedImage = ground_truth - result_seg
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

    count_zeros(subtract_images(ground_truth, seg))


def evaluate_segmentation(seg, evaluator):
    return evaluator(seg)


def generate_parameter_map():
    # TODO(Ian): Use grid search or some other means to generate parameter map. Think closures.
    elastix_params = {}  # parameters go here
    param_grid = ParameterGrid(elastix_params)

    for param_map in param_grid:
        yield param_map





def segment_image(ref_image_crop_list, ref_seg_crop_list, ref_image_ground_truth_crop, ref_seg_ground_truth_crop,
                  target_image_crop_list, target_image_ground_truth_crop, target_seg_ground_truth_crop,
                  parameter_priors):

    def get_seg_score(evaluator, ground_truth, segmentation):
        return evaluator(segmentation, ground_truth)

    get_sub_score = get_seg_score(max, target_seg_ground_truth_crop)

    result_queue = []

    for parameter_map in generate_parameter_map():

        transform_parameter_map = get_transform_parameter_map(target_image_ground_truth_crop,
                                                              ref_image_ground_truth_crop, parameter_map)

        result_seg = apply_transformation(ref_seg_ground_truth_crop, transform_parameter_map)
        seg_score = evaluate_segmentation(result_seg, subtraction_evaluator(target_seg_ground_truth_crop))

        result_queue.append((seg_score, transform_parameter_map))







