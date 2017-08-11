import SimpleITK as sitk
from amsaf.AmsafExecutor import AmsafExecutor

PQ_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_for_ITK-SNAP_biascorr.nii")

PQ_forearm_muscles = sitk.ReadImage("/srv/hart_mri/mri_data/PQ_Full/crops/forearm/PQ_forearm_cropped_muscles.nii")

sub3_forearm_img_cropped = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_for_ITK-SNAP.nii")

sub3_forearm_muscles_ground_truth = sitk.ReadImage(
    "/srv/hart_mri/mri_data/SUBJECT_3/2-forearm/crops/sub3_forearm_cropped_ground_truth_muscles.nii")


if __name__ == '__main__':
    amsafExecutor = AmsafExecutor()
    amsafExecutor.targetGroundTruthImage = sub3_forearm_img_cropped
    amsafExecutor.refGroundTruthImage = PQ_forearm_img_cropped
    amsafExecutor.targetGroundTruthSeg = sub3_forearm_muscles_ground_truth
    amsafExecutor.refGroundTruthSeg = PQ_forearm_muscles
    amsafExecutor.execute()

    topTwenty = amsafExecutor.getTopNParameterMaps(20)

    for i, (pMaps, segScore) in enumerate(topTwenty):
        for transformMap, transformType in zip(pMaps, ['Rigid', 'Affine', 'Bspline']):
            writeFileName = 'SegResult.' + transformType + '.' + str(i) + '.txt'
            sitk.WriteParameterFile(transformMap, writeFileName)
        f = open('ParamMapsIterScore.' + str(i) + '.txt', 'a')
        f.write('score: ' + str(segScore) + '\n')
        f.close()
