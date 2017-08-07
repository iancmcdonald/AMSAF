import unittest
#import amsaf
#import SimpleITK as sitk
test_img1 = "/Users/Daniel/hart_research/MRI_DATA/manual_seg/mergetest/combined.nii"
test_img2 = "/Users/Daniel/hart_research/MRI_DATA/manual_seg/mergetest/combined_seg.nii"


class SubtractorTest(unittest.TestCase):
    # def subtract_itself(self):
    #     # Note: Dimensions are 294 x 871 x 305
    #     autoseg = sitk.ReadImage(test_img1)
    #     groundtruth = sitk.ReadImage(test_img1)
    #     expected = amsaf.amsaf_functional.subtraction_evaluator(groundtruth, autoseg)
    #     self.assertEqual(expected, 78102570)

    def identity_test(self):
        identity = test_img1 - test_img2
        assert test_img1 == identity
        self.assertEqual(identity, test_img1)
# use simpleitk to generate an image of all zeros, subtract that from an image, and then check to see that the number of
# zeros are still the same
# init funtion needed here?

if __name__ == '__main__':
    unittest.main()
