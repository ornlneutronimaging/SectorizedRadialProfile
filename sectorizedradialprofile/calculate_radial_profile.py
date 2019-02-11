import numpy as np
import pandas as pd


class CalculateRadialProfile(object):
    radial_profile = []

    def __init__(self, data=[], center={}, radius=None, angle_range={}):
        """

        :param data: numpy 2D array
        :type data: np.array
        :param center: dictionary that defines the center position of the circle
              ex:
              center = {'x0': 0.5,
                        'y0': 1.1}
        :type center:
        :param radius: Radius of the region, optional.
        :type radius: float
        :param angle_range: Angle 0 is the top vertical and going clockwise. So angle range is [0, 360]
        :type angle_range: dict
        """

        self.data = data
        self.center = center
        self.radius = radius
        self.angle_range = angle_range

        if center:
            try:
                x0 = center['x0']
                y0 = center['y0']
                self.x0 = x0
                self.y0 = y0
            except:
                raise ValueError

        if angle_range:
            try:
                from_angle = angle_range['from']
                to_angle = angle_range['to']
                self.from_angle = from_angle
                self.to_angle = to_angle
            except:
                raise ValueError

    def calculate(self):
        """
        Performs the radial profile calculation
        :return:
        :rtype:
        """
        if self.data == []:
            return

        self.calculate_array_size()
        # self.convert_angles_to_radians()
        self.calculate_pixels_radius()
        self.calculate_pixels_angle_position()
        self.turn_off_data_outside_angle_range()
        self.sort_indices_of_radius()
        self.sort_radius()
        self.sort_data_by_radius_value()
        # self.calculate_radius_bins_location()
        # self.calculate_radius_bins_size()
        self.calculate_profile()

    def calculate_profile(self):
        '''calculate the final profile'''

        df = pd.DataFrame()
        df['radius'] = self.sorted_radius
        df['value'] = self.data_sorted_by_radius
        df.dropna(inplace=True)
        df1 = df.groupby('radius').agg({'value': ['mean', 'std', 'sem']})['value']
        self.radial_profile = df1

    def sort_data_by_radius_value(self):
        '''sort the working data by radius indices'''
        self.data_sorted_by_radius = self.working_data.flat[self.sorted_radius_indices]

    def sort_radius(self):
        '''sort the radius array'''
        self.sorted_radius = self.radius_array.flat[self.sorted_radius_indices]

    def sort_indices_of_radius(self):
        '''sort the indices of the radius array'''
        sort_indices = np.argsort(self.radius_array.flat)
        self.sorted_radius_indices = sort_indices

    def turn_off_data_outside_angle_range(self):
        '''using the angle range provided and the angle value of each pixels,
        this algorithm replace all the initial data by 0 outside the range specified'''
        left_angles_indices = self.array_angle_deg >= self.from_angle
        right_angles_indices = self.array_angle_deg <= self.to_angle
        inside_indices = np.logical_and(left_angles_indices, right_angles_indices)
        if self.radius is not None:
            in_radius_indices = self.radius_array <= self.radius
            inside_indices = np.logical_and(inside_indices, in_radius_indices)
        not_keep = np.invert(inside_indices)

        working_data = np.array(self.data, dtype=np.float64)  # forced array to be float so NaN can be used
        working_data[not_keep] = np.nan  # replaced 0 with NaN so the mean & std can be calculated correctly

        self.working_data = working_data

    def calculate_array_size(self):
        '''retrieve the width and height of the array'''
        [self.height, self.width] = np.shape(self.data)

    def calculate_pixels_angle_position(self):
        '''determine the angle position related to the top vertical center of
        each pixel in radians'''
        complex_array = (self.height - self.y_index - self.y0) + 1j * \
                        (self.x_index - self.x0)
        array_angle_deg = np.angle(complex_array, deg=True)

        # removing all negative angles -> [0, 360[
        array_angle_deg_pos = np.array(array_angle_deg)
        for _y in np.arange(self.height):
            for _x in np.arange(self.width):
                _value = array_angle_deg[_y, _x]
                if _value < 0:
                    array_angle_deg_pos[_y, _x] = 2 * 180 + _value

        self.array_angle_deg = array_angle_deg_pos

    def calculate_pixels_radius(self):
        '''calculate radii of all pixels '''
        self.y_index, self.x_index = np.indices(self.data.shape)
        r_array = np.sqrt((self.x_index - self.x0) ** 2 + (self.y_index - self.y0) ** 2)
        self.radius_array = r_array

    # def convert_angles_to_radians(self):
    # '''convert from degress to radians the angles. This is necessary
    # to evaluate the angle range with the the angle position of each pixel'''
    # self.from_angle_rad = np.deg2rad(self.from_angle)
    # self.to_angle_rad = np.deg2rad(self.to_angle)
