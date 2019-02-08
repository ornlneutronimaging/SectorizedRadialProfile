from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

data_file = 'data_2_circles.tif'
data = np.array(Image.open(data_file))
working_data = data[:, :, 0]

plt.figure(0)
plt.imshow(working_data)
plt.show()

center = {'x0': 500, 'y0': 500}
angle_range = {'from': 0, 'to': 90}

o_profile = CalculateRadialProfile(
    data=working_data, center=center, angle_range=angle_range)
o_profile.calculate()

profile = o_profile.radial_profile

plt.figure(1)
plt.plot(profile)
plt.show()
