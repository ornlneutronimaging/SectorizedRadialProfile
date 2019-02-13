from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile
from sectorizedradialprofile.calculate_radial_profile import load_label_analysis_amira
# from PIL import Image
from skimage import io
import matplotlib.pyplot as plt

# data_file = 'BC_bottom_crop_0050.tif'
data_file = 'BC_bottom_sm_crop.tif'
# data_file = 'GC_top_sm_crop.tif'
im = io.imread(data_file)

# plt.imshow(im)
center_2d = (79, 93)
# center_3d = {'x0': 79, 'y0': 93, 'z0': 50}
center_3d = (79, 93, 50)
angle_range = None
param_dict = load_label_analysis_amira('BC_sm.Label-Analysis.csv', drop=0, z_flipper=520)
# param_dict = load_label_analysis_amira('GC_sm.Label-Analysis-2.csv', drop=8, z_flipper=594)
radius = 41
# angle_range = (0,360)
# center_3d_list = {'9': [(79, 93, 50), 36],
#                   '8': [(109, 99, 110), 36],
#                   '7': [(80, 85, 169), 34],
#                   '6': [(106, 105, 226), 38],
#                   '5': [(78, 90, 284), 35],
#                   '4': [(103, 110, 341), 35],
#                   '3': []
#                   }

o_profile = CalculateRadialProfile(data=im)
for each in param_dict.keys():
    # o_profile.add_params(center=param_dict[each][0], radius=param_dict[each][1], angle_range=angle_range)
    o_profile.add_params(center=param_dict[each][0], radius=radius, angle_range=angle_range)

# o_profile.add_params(center=center_3d, radius=radius, angle_range=angle_range)
o_profile.calculate()

# plt.imshow(o_profile.working_data)

profile = o_profile.radial_profile

profile.plot()
plt.show()

# plt.errorbar(x=profile.index, y=profile['mean'], yerr=profile['std'])
# plt.show()
