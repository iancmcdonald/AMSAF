import SimpleITK as sitk
from amsaf.AmsafExecutor import AmsafExecutor

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")


def main():
    for metric in ['subtraction', 'dice', 'jaccard', 'volumeSimilarity', 'kappa']:
        amsafExecutor = AmsafExecutor()
        amsafExecutor.targetGroundTruthImage = sub3_forearm_img_cropped
        amsafExecutor.refGroundTruthImage = PQ_forearm_img_cropped
        amsafExecutor.targetGroundTruthSeg = sub3_forearm_muscles_ground_truth
        amsafExecutor.refGroundTruthSeg = PQ_forearm_muscles
        amsafExecutor.similarityMetric = metric
        amsafExecutor.execute()

        resultsDir = '/home/ian/Programming/HART/AMSAF-results/sim-metrics-data/' + metric + '/'

        amsafExecutor.writeTopNParameterMaps(20, resultsDir + 'parameter-maps/')

        for i, seg in enumerate(amsafExecutor.getTopNSegmentations(10)):
            sitk.WriteImage(seg, resultsDir + 'seg-images/seg_result.' + str(i) + '.nii')


if __name__ == '__main__':
    main()
