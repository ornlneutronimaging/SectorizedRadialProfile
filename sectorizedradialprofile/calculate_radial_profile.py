
import numpy as np

class CalculateRadialProfile(object):
    
    def __init__(self, data=[], center={}, angle_range={}):
        '''
        Arguments:
        
        - data: numpy 2D array
        - center: dictionary that defines the center position of the circle
              ex: 
              center = {'x0': 0.5,
                        'y0': 1.1}
        - angle_range: dictionary that defines the sector in degrees to consider. Angle 0 is
        the top vertical and going clockwise. So angle range is [0, 360[
        '''
        
        self.data = data
        self.center = center
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