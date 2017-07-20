import unittest

import numpy as np

from IOHMM import (cal_log_alpha, cal_log_beta, cal_HMM)


class HMMUtilsTests(unittest.TestCase):
    # test case from pyhmm
    @classmethod
    def setUpClass(cls):
        cls.log_prob_initial = np.log(
            np.array([0.4, 0.3, 0.3]))
        cls.log_prob_transition = np.log(
            np.array([[[0.6, 0.3, 0.1],
                       [0.2, 0.5, 0.3],
                       [0.3, 0.2, 0.5]]] * 11))
        cls.log_Ey = np.log(
            np.array([[0.3, 0.7, 0.5],
                      [0.3, 0.7, 0.5],
                      [0.7, 0.3, 0.5],
                      [0.7, 0.3, 0.5],
                      [0.7, 0.3, 0.5],
                      [0.7, 0.3, 0.5],
                      [0.3, 0.7, 0.5],
                      [0.3, 0.7, 0.5],
                      [0.3, 0.7, 0.5],
                      [0.7, 0.3, 0.5],
                      [0.7, 0.3, 0.5],
                      [0.3, 0.7, 0.5]]))

    def test_cal_alpha_beta(self):
        # forward algorithm
        log_alpha = cal_log_alpha(self.log_prob_initial, self.log_prob_transition, self.log_Ey, {})
        np.testing.assert_array_almost_equal(
            np.exp(log_alpha),
            np.array([[1.20000000e-01, 2.10000000e-01, 1.50000000e-01],
                      [4.77000000e-02, 1.19700000e-01, 7.50000000e-02],
                      [5.25420000e-02, 2.67480000e-02, 3.90900000e-02],
                      [3.40212600e-02, 1.10863800e-02, 1.64118000e-02],
                      [1.92875004e-02, 5.70957840e-03, 7.46697000e-03],
                      [1.04681548e-02, 3.04033000e-03, 3.68755428e-03],
                      [2.39856756e-03, 3.77868562e-03, 1.90134581e-03],
                      [8.29584420e-04, 2.09242757e-03, 1.16206767e-03],
                      [3.79456940e-04, 1.06925185e-03, 6.45860274e-04],
                      [4.44697832e-04, 2.33290519e-04, 3.40825693e-04],
                      [2.91007157e-04, 9.54659242e-05, 1.42434893e-04],
                      [7.09283841e-05, 1.14465462e-04, 6.44789697e-05]]),
            decimal=2)
        # backward algorithm
        log_beta = cal_log_beta(self.log_prob_transition, self.log_Ey, {})
        np.testing.assert_array_almost_equal(
            np.exp(log_beta),
            np.array([[4.66170742e-04, 5.55151324e-04, 5.15670321e-04],
                      [1.23431939e-03, 8.96027127e-04, 1.11655111e-03],
                      [2.32427431e-03, 1.69786509e-03, 2.10632641e-03],
                      [4.35918163e-03, 3.27228685e-03, 3.97824421e-03],
                      [8.02824268e-03, 6.78021860e-03, 7.54200053e-03],
                      [1.35088245e-02, 1.81218837e-02, 1.44713375e-02],
                      [2.63228424e-02, 3.48915192e-02, 2.88698760e-02],
                      [5.40079200e-02, 6.48328800e-02, 5.97302400e-02],
                      [1.40748000e-01, 1.05828000e-01, 1.28988000e-01],
                      [2.59200000e-01, 2.17600000e-01, 2.46000000e-01],
                      [4.40000000e-01, 5.60000000e-01, 4.80000000e-01],
                      [1.00000000e+00, 1.00000000e+00, 1.00000000e+00]]),
            decimal=2)

    def test_cal_hmm(self):
        log_gamma, log_epsilon, log_likelihood = cal_HMM(
            self.log_prob_initial, self.log_prob_transition, self.log_Ey, {})
        # likelihood
        self.assertAlmostEqual(np.exp(log_likelihood), 0.000249872815287, places=6)

        # gamma
        np.testing.assert_array_almost_equal(
            np.exp(log_gamma),
            np.array([[0.22387585, 0.46656447, 0.30955968],
                      [0.23562801, 0.42923616, 0.33513583],
                      [0.48873672, 0.18175044, 0.32951283],
                      [0.59352135, 0.14518512, 0.26129352],
                      [0.6196942, 0.15492758, 0.22537823],
                      [0.56593778, 0.2204982, 0.21356402],
                      [0.25267701, 0.52764476, 0.21967823],
                      [0.17930774, 0.54290862, 0.27778364],
                      [0.21373996, 0.45285753, 0.33340251],
                      [0.46129739, 0.20315942, 0.33554319],
                      [0.51243329, 0.21395252, 0.27361419],
                      [0.28385795, 0.4580949, 0.25804716]]),
            decimal=6)

        # epsilon
        np.testing.assert_array_almost_equal(
            np.exp(log_epsilon),
            np.array([[[0.10669948, 0.09036551, 0.02681087],
                       [0.06224136, 0.26356606, 0.14075705],
                       [0.06668717, 0.07530459, 0.16756792]],

                      [[0.18635285, 0.02917058, 0.02010458],
                       [0.15588006, 0.12200274, 0.15135336],
                       [0.14650381, 0.03057713, 0.15805489]],

                      [[0.38498326, 0.0619272, 0.04182626],
                       [0.06532889, 0.05254301, 0.06387854],
                       [0.1432092, 0.03071491, 0.15558872]],

                      [[0.45909352, 0.08308404, 0.05134379],
                       [0.04986769, 0.0451238, 0.05019363],
                       [0.11073298, 0.02671974, 0.12384081]],

                      [[0.43794925, 0.12589335, 0.0558516],
                       [0.04321461, 0.06211259, 0.04960038],
                       [0.08477392, 0.03249226, 0.10811204]],

                      [[0.19849813, 0.30696602, 0.06047363],
                       [0.01921701, 0.14859002, 0.05269118],
                       [0.03496187, 0.07208872, 0.10651342]],

                      [[0.09331746, 0.13069156, 0.02866799],
                       [0.04900388, 0.34315087, 0.13549001],
                       [0.0369864, 0.06906618, 0.11362565]],

                      [[0.08411168, 0.07378388, 0.02141218],
                       [0.07071718, 0.31017019, 0.16202125],
                       [0.0589111, 0.06890346, 0.14996908]],

                      [[0.16532091, 0.02974027, 0.01867878],
                       [0.15528304, 0.13967258, 0.1579019],
                       [0.14069344, 0.03374658, 0.1589625]],

                      [[0.32888796, 0.08969672, 0.04271272],
                       [0.05751204, 0.07842551, 0.06722187],
                       [0.12603329, 0.04583029, 0.1636796]],

                      [[0.2096318, 0.24457043, 0.05823106],
                       [0.02292348, 0.13372032, 0.05730871],
                       [0.05130266, 0.07980414, 0.14250739]]]),
            decimal=6)