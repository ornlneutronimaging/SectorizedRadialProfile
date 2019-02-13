import numpy as np
import pandas as pd


class CalculateRadialProfile(object):

    def __init__(self, data: np.ndarray):
        """

        :param data: numpy 2D array
        :type data: np.array
        """
        self.data = data
        self.dimension = len(data.shape)
        if self.dimension not in [2, 3]:
            raise ValueError('Only 2D or 3D np.array are supported.')
        self.bool_2d = self.dimension == 2  # boolean indicator of data dimension, True: 2D, False: 3D
        self.center = None
        self.radius = None
        self.angle_range = None
        self.x0 = None
        self.y0 = None
        self.z0 = None
        self.param_list = []
        if self.bool_2d:
            self.y_index, self.x_index = np.indices(self.data.shape)
            self.y_len, self.x_len = np.shape(self.data)  # retrieve the size of the array
        else:
            self.z_index, self.y_index, self.x_index = np.indices(self.data.shape)
            self.z_len, self.y_len, self.x_len = np.shape(self.data)  # retrieve the size of the array
        self.final_radius_array = None
        self.final_data_array = None

    def add_params(self, center: tuple, radius=None, angle_range=None):
        """

        :param center: Origin of the radial plot, '(x0, y0)' or '(x0, y0, z0)'.
        :type center: tuple
        :param radius: The maximum distance from specified center. Optional, default 'None' used to include all.
        :type radius: int or float
        :param angle_range: Angular coverage in degrees '(0, 360)'. Optional, default 'None' used to include all.
        :type angle_range: tuple
        """
        self._validate_params(center=center, radius=radius, angle_range=angle_range)
        self.center = center
        self.radius = radius
        self.angle_range = angle_range
        self.x0 = self.center[0]
        self.y0 = self.center[1]
        self.param_list.append(form_param_dict(center=center, radius=radius, angle_range=angle_range))

    def calculate(self):
        """
        Performs the radial profile calculation
        :return:
        :rtype:
        """
        _final_radius_array = np.array([])
        _final_data_array = np.array([])
        for each_param_dict in self.param_list:
            _current_radius_array, _current_data_array = self.get_sorted_radial_array(each_param_dict)
            _final_radius_array = np.concatenate((_final_radius_array, _current_radius_array), axis=None)
            _final_data_array = np.concatenate((_final_data_array, _current_data_array), axis=None)
        self.final_radius_array = np.array(_final_radius_array)
        self.final_data_array = np.array(_final_data_array)
        self.calculate_profile()

    def calculate_profile(self):
        '''calculate the final profile'''
        df = pd.DataFrame()
        df['radius'] = self.final_radius_array
        df['value'] = self.final_data_array
        df1 = df.groupby('radius').agg({'value': ['mean', 'std', 'sem']})['value']
        self.radial_profile = df1

    def get_sorted_radial_array(self, param_dict):
        """
        :return: sorted radius array and data array
        :rtype: np.array
        """
        self.center = param_dict['center']
        self.radius = param_dict['radius']
        self.angle_range = param_dict['angle_range']
        self.x0 = self.center[0]
        self.y0 = self.center[1]
        if not self.bool_2d:
            self.z0 = self.center[2]

        self.calculate_pixels_radius()
        self.calculate_pixels_angle_position()
        self.turn_off_data_outside()
        self.sort_indices_of_radius()
        self.sort_data_by_radius_value()
        return self.sorted_radius[:], self.data_sorted_by_radius[:]

    def sort_data_by_radius_value(self):
        '''sort the working data by radius indices'''
        _data_sorted_by_radius = self.working_data.flat[self.sorted_radius_indices]
        _sorted_radius = self.radius_array.flat[self.sorted_radius_indices]
        _nan_indices = np.isnan(_data_sorted_by_radius)
        _not_nan_indices = np.invert(_nan_indices)
        self.data_sorted_by_radius = _data_sorted_by_radius[_not_nan_indices]
        self.sorted_radius = _sorted_radius[_not_nan_indices]

    def sort_indices_of_radius(self):
        '''sort the indices of the radius array'''
        sort_indices = np.argsort(self.radius_array.flat)
        self.sorted_radius_indices = sort_indices

    def turn_off_data_outside(self):
        '''using the angle range provided and the angle value of each pixels,
        this algorithm replace all the initial data by 0 outside the range specified'''
        inside_indices = np.isreal(self.data)
        if self.angle_range is not None:
            left_angles_indices = self.array_angle_deg >= self.angle_range[0]
            right_angles_indices = self.array_angle_deg <= self.angle_range[1]
            inside_indices = np.logical_and(left_angles_indices, right_angles_indices)
        if self.radius is not None:
            in_radius_indices = self.radius_array <= self.radius
            inside_indices = np.logical_and(inside_indices, in_radius_indices)
        not_keep_indices = np.invert(inside_indices)

        working_data = np.array(self.data, dtype=np.float64)  # forced array to be float so NaN can be used
        working_data[not_keep_indices] = np.nan  # replaced 0 with NaN so the mean & std can be calculated correctly

        self.working_data = working_data

    def calculate_pixels_angle_position(self):
        '''determine the angle position related to the top vertical center of
        each pixel in radians'''
        if self.angle_range is not None:
            if self.bool_2d:
                complex_array = (self.y_len - self.y_index - self.y0) + 1j * \
                                (self.x_index - self.x0)
                array_angle_deg = np.angle(complex_array, deg=True)

                # removing all negative angles -> [0, 360[
                array_angle_deg_pos = np.array(array_angle_deg)
                for _y in np.arange(self.y_len):
                    for _x in np.arange(self.x_len):
                        _value = array_angle_deg[_y, _x]
                        if _value < 0:
                            array_angle_deg_pos[_y, _x] = 2 * 180 + _value

                self.array_angle_deg = array_angle_deg_pos
            else:
                raise ValueError('Angular range selection is not available for 3D data.')

    def calculate_pixels_radius(self):
        '''calculate radii of all pixels '''
        if self.bool_2d:
            r_array = np.sqrt((self.x_index - self.x0) ** 2 + (self.y_index - self.y0) ** 2)
            self.radius_array = r_array
        else:
            r_array = np.sqrt(
                (self.x_index - self.x0) ** 2 + (self.y_index - self.y0) ** 2 + (self.z_index - self.z0) ** 2)
            self.radius_array = r_array

    def _validate_params(self, center, radius, angle_range):
        assert type(center) == tuple
        if len(center) != self.dimension:
            raise ValueError("'center' input is not dimensionally correct for input data.")
        for each in center:
            if each < 0:
                raise ValueError("'center' input can not be negative.")
        if radius is not None:
            if radius <= 0:
                raise ValueError("'radius' has to be greater than zero.")
        if angle_range is not None:
            assert type(angle_range) == tuple
            assert len(angle_range) == 2
            for each in angle_range:
                if each < 0:
                    raise ValueError("'angle_range' has to be within (0, 360).")


def load_label_analysis_amira(file_path, drop=None, z_flipper=None):
    """

    :param file_path: File path to the 'Label-Analysis.csv' file generated by Amira-Avizo
    :type file_path: str
    :param drop: Drop row or rows by index. Default: None
    :type drop: int or list
    :param z_flipper: Optional. the value of Z-1 (stack number -1) to flip the Amira correct BeryCenterZ output.
    :type z_flipper: int
    :return: A dictionary containing center and radius
    :rtype: dict
    """
    _df_amira = pd.read_csv(file_path, skiprows=1)
    _df_amira.insert(loc=1, column='EqRadius', value=_df_amira['EqDiameter'] / 2)
    if drop is not None:
        _df_amira.drop(index=drop, inplace=True)
        _df_amira.reset_index(drop=True, inplace=True)
    if z_flipper is not None:
        _df_amira['BaryCenterZ'] = z_flipper - _df_amira['BaryCenterZ']
    df_amira = _df_amira.round(decimals=0)
    print(_df_amira)
    _analysis_dict = {}
    for _i, _each in enumerate(df_amira['index']):
        _name = 'obj_' + str(_each)
        _analysis_dict[_name] = [
            (df_amira['BaryCenterX'][_i],
             df_amira['BaryCenterY'][_i],
             df_amira['BaryCenterZ'][_i]),
            df_amira['EqRadius'][_i]
        ]
    return _analysis_dict


def form_param_dict(center: tuple, radius: float, angle_range):
    """

    :param center: coordinates in form of (x,y) or (x, y, z)
    :type center: tuple
    :param radius: radius of the radial plot range
    :type radius: float
    :param angle_range: optional sector defined using tuple, eg. (0, 360)
    :type angle_range: tuple
    :return: shaped dictionary containing parameters
    :rtype: dict
    """
    _dict = {
        'center': center,
        'radius': radius,
        'angle_range': angle_range
    }
    return _dict
