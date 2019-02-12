from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile
# from PIL import Image
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

# data_file = 'BC_bottom_crop_0050.tif'
im_3d = io.imread('BC_bottom_sm_crop.tif')

# plt.imshow(im)
center_2d = {'x0': 79, 'y0': 93}
center_3d = {'x0': 79, 'y0': 93, 'z0': 50}

angle_range = {'from': 0, 'to': 72}

# center_3d = [(79, 93, 50), []]

radius = 50
o_profile = CalculateRadialProfile(data=im_3d)
o_profile.add_params(center=(79, 93, 50), radius=40)
o_profile.calculate()

# plt.imshow(o_profile.working_data)

profile = o_profile.radial_profile

profile.plot()
plt.show()
