import unittest
import pytest
import numpy as np
import os
from skimage import io

from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile


class TestClass(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../notebooks/data2d_for_test_1.tif'))
        self.data = io.imread(self.data_path)

    # def test_default_initialization(self):
    #     """assert if all parameters are coorectly set up when no parameters passed in"""
    #     o_calculate = CalculateRadialProfile()
    #     assert o_calculate.data == []
    #     assert o_calculate.center == {}
    #     assert o_calculate.angle_range == {}

    def test_initialization(self):
        '''assert all parameters are correctly set up when parameters passed in'''
        my_data_2d = np.array([[1, 2, 3], [1, 2, 3]])
        o_calculate = CalculateRadialProfile(data=my_data_2d)
        assert (o_calculate.data == my_data_2d).all()
        my_data_3d = np.array([[1, 2, 3], [1, 2, 3], [0, 0, 0]])
        o_calculate = CalculateRadialProfile(data=my_data_3d)
        assert (o_calculate.data == my_data_3d).all()
        bad_dimension_data = np.array([1, 2, 3])
        self.assertRaises(ValueError, CalculateRadialProfile, bad_dimension_data)

    def test_initialization_real_case(self):
        '''assert all parameters are correctly set up when real parameters are passed in'''
        assert os.path.exists(self.data_path)

        data = self.data

        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)

        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        assert (o_calculate.data == data).all()
        assert o_calculate.center == center
        assert o_calculate.angle_range == angle_range
        assert o_calculate.x0 == center[0]
        assert o_calculate.y0 == center[1]
        # assert o_calculate.from_angle == angle_range[0]
        # assert o_calculate.to_angle == angle_range[1]

    def test_throwing_error_when_center_format_has_wrong_format(self):
        '''assert error is thrown when center does not have the right format'''
        o_calculate = CalculateRadialProfile(data=self.data)
        bad_center = (10, -1)
        self.assertRaises(ValueError, o_calculate.add_params, bad_center)
        bad_center = {10, 1}
        self.assertRaises(AssertionError, o_calculate.add_params, bad_center)
        bad_center = [10, 1]
        self.assertRaises(AssertionError, o_calculate.add_params, bad_center)
        bad_center = (10, 1, 3)
        self.assertRaises(ValueError, o_calculate.add_params, bad_center)

    def test_throwing_error_when_angle_range_has_wrong_format(self):
        '''assert error is thrown when angle range does not have the right format'''
        o_calculate = CalculateRadialProfile(data=self.data)
        bad_angle_range = (-10, 40)
        self.assertRaises(ValueError, o_calculate.add_params, bad_angle_range)
        bad_angle_range = {0, 90}
        self.assertRaises(AssertionError, o_calculate.add_params, bad_angle_range)
        bad_angle_range = [0, 90]
        self.assertRaises(AssertionError, o_calculate.add_params, bad_angle_range)
        bad_angle_range = (90, 180, 270)
        self.assertRaises(ValueError, o_calculate.add_params, bad_angle_range)

    def test_calculation_of_radius_array(self):
        '''assert that the array of pixel radius is correct'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)

        o_calculate.calculate()

        _radius_array = o_calculate.radius_array
        assert _radius_array[y0, x0] == 0  # center of circle
        assert _radius_array[0, 0] == pytest.approx(7.071, abs=0.01)

    def test_report_size_of_image(self):
        '''assert the size of the array is correctly retrieved'''
        data = np.ones((20, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)

        assert 10 == o_calculate.x_len
        assert 20 == o_calculate.y_len

    def test_calculate_array_of_angles(self):
        '''assert the array of angles is correct'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        array_angle_deg = o_calculate.array_angle_deg

        assert array_angle_deg[0, 0] == 315
        assert array_angle_deg[y0, x0] == 0
        assert array_angle_deg[np.int(height / 2), 0] == 270
        self.assertAlmostEqual(array_angle_deg[height - 1, 0], 231.3, delta=0.1)

    def test_new_working_data(self):
        '''assert the data outside the angle range are turned off - working data is correct'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        working_data = o_calculate.working_data
        real_working_data = np.zeros((10, 10))
        real_working_data[:] = np.nan
        real_working_data[0:6, 5:, ] = 1
        assert (working_data[0:6, 5:, ] == real_working_data[0:6, 5:, ]).all()

    def test_sort_indices_of_radius(self):
        '''assert the array of radius indices is correctly sorted'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        sorted_radius_indices = o_calculate.sorted_radius_indices

        assert 55 == sorted_radius_indices[0]
        assert 0 == sorted_radius_indices[-1]

    def test_sort_radius(self):
        '''assert the array of radius is correctly sorted'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        sorted_radius = o_calculate.sorted_radius

        assert 0 == sorted_radius[0]
        self.assertAlmostEqual(6.4031, sorted_radius[-1], delta=0.01)

    def test_working_data_correctly_sorted(self):
        '''assert the working data are correctly sorted according to the pixel radius'''
        data = np.ones((10, 10))
        data[5][4] = 100
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = None
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        data_sorted_by_radius = o_calculate.data_sorted_by_radius

        assert ([1., 1., 100., 1.] == data_sorted_by_radius[:4]).all()

    def test_profile(self):
        '''assert the final profil'''
        data = self.data
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        radial_profile = o_calculate.radial_profile
        self.assertAlmostEqual(0.005267, radial_profile['mean'][0], delta=0.0001)
        self.assertAlmostEqual(0.005289, radial_profile['mean'][1], delta=0.0001)
        self.assertAlmostEqual(0.005310, radial_profile['mean'][2], delta=0.0001)
        self.assertAlmostEqual(0.005312, radial_profile['mean'][3], delta=0.0001)

    def test_full_radial_profile(self):
        _file_path = os.path.dirname(__file__)
        data_path = os.path.abspath(os.path.join(_file_path, '../../notebooks/circle_profile.tif'))
        data = io.imread(data_path)
        o_calculate = CalculateRadialProfile(data=data)
        center = (500, 600)
        o_calculate.add_params(center=center)
        o_calculate.calculate()
        radial_profile = o_calculate.radial_profile

        radius_returned = radial_profile.index
        mean_counts_returned = np.array(radial_profile["mean"])

        radius_expected = [0, 1.0, 1.4142, 2.0, 2.236, 2.8284]
        for _expected, _returned in zip(radius_expected, radius_returned):
            assert _returned == pytest.approx(_expected, abs=1e-2)

        mean_counts_expected = [0.7, 1.14, 1.4977]
        for _expected, _returned in zip(mean_counts_expected, mean_counts_returned):
            assert _returned == pytest.approx(_expected, abs=1e-2)
        assert False

    def test_partial_radial_profile(self):
        _file_path = os.path.dirname(__file__)
        data_path = os.path.abspath(os.path.join(_file_path, '../../notebooks/circle_profile.tif'))
        data = io.imread(data_path)
        o_calculate = CalculateRadialProfile(data=data)
        center = (500, 600)
        angle_range = (0, 90)

        print("==== partial ====")
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        print(o_calculate.radial_profile)

        # print(o_calculate.final_radius_array)

        print("==== full ====")
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center)
        o_calculate.calculate()
        print(o_calculate.radial_profile)



        # radial_profile = o_calculate.radial_profile
        #
        # radius_returned = radial_profile.index
        # mean_counts_returned = np.array(radial_profile["mean"])
        #
        # print(radius_returned)
        #
        # radius_expected = [0, 1.0, 1.4142, 2.0, 2.236, 2.8284]
        # for _expected, _returned in zip(radius_expected, radius_returned):
        #     assert _returned == pytest.approx(_expected, abs=1e-2)
        #
        # mean_counts_expected = [0.7, 1.14, 1.4977]
        # for _expected, _returned in zip(mean_counts_expected, mean_counts_returned):
        #     assert _returned == pytest.approx(_expected, abs=1e-2)

        assert False