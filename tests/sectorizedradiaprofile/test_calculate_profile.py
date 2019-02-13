import unittest
import numpy as np
import os
from skimage import io

from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile


class TestClass(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../notebooks/data_2_circles.tif'))

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
        data = io.imread(self.data_path)
        data = data[:, :, 1]

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
        bad_center = {'x0': 10,
                      'x1': -1}
        self.assertRaises(ValueError, CalculateRadialProfile, [], bad_center)

    def test_throwing_error_when_angle_range_has_wrong_format(self):
        '''assert error is thrown when angle range does not have the right format'''
        bad_angle_range = {'from': 10,
                           'too': 20}
        self.assertRaises(ValueError, CalculateRadialProfile, [], {}, bad_angle_range)

    # def test_angle_conversion_to_rad(self):
    # '''assert angle are correctly converted to radians'''
    # data = np.array(Image.open(self.data_path))
    # data = data[:, :, 1]

    # [height, width] = np.shape(data)
    # [y0, x0] = [int(height/2), int(width/2)]
    # center = {'x0': x0,
    # 'y0': y0}

    # angle_range = {'from': 0,
    # 'to': 90}
    # o_calculate = CalculateRadialProfile(data=data,
    # center=center,
    # angle_range=angle_range)
    # o_calculate.calculate()

    # assert 0 == o_calculate.from_angle_rad
    # self.assertAlmostEqual(3.14/2, o_calculate.to_angle_rad, delta = 0.001)

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
        self.assertAlmostEquals(_radius_array[0, 0], 7.071, delta=0.01)

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
        real_working_data[0:6, 5:, ] = 1

        assert (working_data == real_working_data).all()

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
        self.assertAlmostEqual(7.071, sorted_radius[-1], delta=0.01)

    def test_working_data_correctly_sorted(self):
        '''assert the working data are correctly sorted according to the pixel radius'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        data_sorted_by_radius = o_calculate.data_sorted_by_radius

        assert ([1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1] == data_sorted_by_radius[:16]).all()

    def test_radius_bins_location(self):
        '''assert the location of radius bins'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        radius_bins_location = o_calculate.radius_bins_location

        assert ([0, 8, 24, 44, 68, 94, 98] == radius_bins_location).all()

    def test_radius_bins_size(self):
        '''assert the size of the radius bins'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        radius_bins_size = o_calculate.radius_bins_size

        assert ([8, 16, 20, 24, 26, 4] == radius_bins_size).all()

    def test_profile(self):
        '''assert the final profil'''
        data = np.ones((10, 10))
        [height, width] = np.shape(data)
        [y0, x0] = [int(height / 2), int(width / 2)]
        center = (x0, y0)
        angle_range = (0, 90)
        o_calculate = CalculateRadialProfile(data=data)
        o_calculate.add_params(center=center, angle_range=angle_range)
        o_calculate.calculate()
        radial_profile = o_calculate.radial_profile

        self.assertAlmostEquals(0.375, radial_profile[0], delta=0.01)
        self.assertAlmostEqual(0.313, radial_profile[1], delta=0.01)
        self.assertAlmostEqual(0.3, radial_profile[2], delta=0.01)
        self.assertAlmostEqual(0.292, radial_profile[3], delta=0.01)
