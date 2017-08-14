import SimpleITK as sitk
from amsaf.AmsafImageFilter import AmsafImageFilter

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")


def main():
    for metric in ['subtraction', 'dice', 'jaccard', 'volumeSimilarity', 'kappa']:
        amsafImageFilter = AmsafImageFilter()
        amsafImageFilter.SetTargetGroundTruthImage(sub3_forearm_img_cropped)
        amsafImageFilter.SetRefGroundTruthImage(PQ_forearm_img_cropped)
        amsafImageFilter.SetTargetGroundTruthSeg(sub3_forearm_muscles_ground_truth)
        amsafImageFilter.SetRefGroundTruthSeg(PQ_forearm_muscles)
        amsafImageFilter.SetSimilarityMetric(metric)
        amsafImageFilter.Execute()

        resultsDir = '/home/ian/Programming/HART/AMSAF-results/sim-metrics-data/' + metric + '/'

        amsafImageFilter.WriteTopNParameterMaps(20, resultsDir + 'parameter-maps/')

        for i, seg in enumerate(amsafImageFilter.GetTopNSegmentations(10)):
            sitk.WriteImage(seg, resultsDir + 'seg-images/seg_result.' + str(i) + '.nii')


if __name__ == '__main__':
    main()
