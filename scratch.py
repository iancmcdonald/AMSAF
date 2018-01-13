import SimpleITK as sitk
from amsaf import AmsafImageFilter

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_combined = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_combined.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP_biascorr.nii")

sub3_forearm_combined_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_combined.nii")

PQ_forearm_masked_bones = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_bones_subtracted.nii")

sub3_forearm_masked_bones = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_bones_subtracted.nii")


def main():
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(sub3_forearm_masked_bones)
    elastixImageFilter.SetMovingImage(PQ_forearm_masked_bones)
    pMap = sitk.GetDefaultParameterMap('rigid')
    pMap['AutomaticTransformInitialization'] = ['true']
    pMap['ResampleInterpolator'] = ['FinalNearestNeighborInterpolator']
    elastixImageFilter.SetParameterMap(pMap)
    elastixImageFilter.Execute()

    PQ_init_image = elastixImageFilter.GetResultImage()
    transformParameterMap = elastixImageFilter.GetTransformParameterMap()

    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(PQ_forearm_combined)
    transformixImageFilter.Execute()

    PQ_init_seg = transformixImageFilter.GetResultImage()

    amsafImageFilter = AmsafImageFilter()
    amsafImageFilter.SetTargetGroundTruthImage(sub3_forearm_img_cropped)
    amsafImageFilter.SetRefGroundTruthImage(PQ_init_image)
    amsafImageFilter.SetTargetGroundTruthSeg(sub3_forearm_combined_ground_truth)
    amsafImageFilter.SetRefGroundTruthSeg(PQ_init_seg)
    amsafImageFilter.SetSimilarityMetric('dice')
    amsafImageFilter.Execute()

    resultsDir = '/home/ian/Programming/HART/AMSAF-results/latest/'

    amsafImageFilter.WriteTopNParameterMaps(10, resultsDir + 'parameter-maps/')

    for i, seg in enumerate(amsafImageFilter.GetTopNSegmentations(10)):
        sitk.WriteImage(seg, resultsDir + 'seg-images/seg_result.' + str(i) + '.nii')

    sitk.WriteImage(PQ_init_image, resultsDir + 'PQ_bones_initialized.nii')


if __name__ == '__main__':
    main()
