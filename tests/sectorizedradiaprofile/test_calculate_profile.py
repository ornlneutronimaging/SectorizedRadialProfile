
import unittest
import numpy as np
import os
from PIL import Image

from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile

class TestClass(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../notebooks/data_2_circles.tif'))
        
    def test_default_initialization(self):
        """assert if all parameters are coorectly set up when no parameters passed in"""
        o_calculate = CalculateRadialProfile()
        assert o_calculate.data == []
        assert o_calculate.center == {}
        assert o_calculate.angle_range == {}
        
    def test_initialization(self):
        '''assert all parameters are correctly set up when parameters passed in'''
        my_data = np.array([1,2,3])
        my_center = {'x0': 0.5,
                     'y0': 1.1}
        my_angle_range = {'from': 0,
                          'to': 90}
        o_calculate = CalculateRadialProfile(data=my_data,
                                             center=my_center,
                                             angle_range=my_angle_range)
        assert (o_calculate.data == my_data).all()
        assert o_calculate.center == my_center
        assert o_calculate.angle_range == my_angle_range
        
    def test_initialization_real_case(self):
        '''assert all parameters are correctly set up when real parameters are passed in'''
        assert os.path.exists(self.data_path)
        data = np.array(Image.open(self.data_path))
        data = data[:, :, 1]

        [height, width] = np.shape(data)
        [y0, x0] = [int(height/2), int(width/2)]
        center = {'x0': x0,
                  'y0': y0}

        angle_range = {'from': 0,
                       'to': 90}
        o_calculate = CalculateRadialProfile(data=data,
                                             center=center,
                                             angle_range=angle_range)
        
        assert (o_calculate.data == data).all()        
        assert o_calculate.center == center
        assert o_calculate.angle_range == angle_range
        assert o_calculate.x0 == center['x0']
        assert o_calculate.y0 == center['y0']
        assert o_calculate.from_angle == angle_range['from']
        assert o_calculate.to_angle == angle_range['to']

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