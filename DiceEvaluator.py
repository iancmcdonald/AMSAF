from AbstractEvaluator import AbstractEvaluator


class DiceEvaluator(AbstractEvaluator):
    def dice_coefficient(self, a, b):
        """Calculates the dice coefficient.
        This implementation of dice coefficient comes from :
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Dice%27s_coefficient

        Args:
            a (SimpleITK.SimpleITK.Image): The ground truth segmentation (provides positives)
            b (SimpleITK.SimpleITK.Image): Automatic segmentation

        Returns: A floating point number from 0.0 to 1.0

        """
        if not len(a) or not len(b): return 0.0
        if len(a) == 1:  a = a + u'.'
        if len(b) == 1:  b = b + u'.'

        a_bigram_list = []
        for i in range(len(a) - 1):
            a_bigram_list.append(a[i:i + 2])
        b_bigram_list = []
        for i in range(len(b) - 1):
            b_bigram_list.append(b[i:i + 2])

        a_bigrams = set(a_bigram_list)
        b_bigrams = set(b_bigram_list)
        overlap = len(a_bigrams & b_bigrams)
        dice_coeff = overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))
        return dice_coeff

    def eval(self, autoseg, groundtruth):
        return self.dice_coefficent(groundtruth, autoseg)
