from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile
# from PIL import Image
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

# data_file = 'BC_bottom_crop_0050.tif'
im = io.imread('BC_bottom_sm_crop_0050.tif')

# plt.imshow(im)
center = {'x0': 79, 'y0': 93}
angle_range = {'from': 0, 'to': 72}
radius = 40

o_profile = CalculateRadialProfile(
    data=im, center=center, radius=radius, angle_range=angle_range)
o_profile.calculate()

plt.imshow(o_profile.working_data)

profile = o_profile.radial_profile

profile.plot()
plt.show()
