.. tutorial:

****************
Getting Started
****************

First we need to import the various librairies::

    from sectorizedradialprofile.calculate_radial_profile import CalculateRadialProfile
    from PIL import Image
    import matplotlib.pyplot as plt
    %matplotlib notebook

then we load the data (data_2_circles.tif)::

    data_file = 'data_2_circles.tif'
    data = np.array(Image.open(data_file))
    working_data = data[:,:,0]    

checking the data::

    plt.figure(0)
    plt.imshow(working_data)
    
.. image:: _static/raw_data.png

We need to define the **center** of the profile region and the **angle range**::

    center = {'x0': 500, 'y0': 500}  #pixels
    angle_range = {'from': 0, 'to': 90}  #degrees

We now run the algorithm to find the profile:: 

    o_profile = CalculateRadialProfile(data=working_data, center=center, angle_range=angle_range)
    o_profile.calculate()
    profile = o_profile.radial_profile

Now we can display the result::

    plt.figure(1)
    plt.plot(profile)

.. image:: _static/sector_profile.png

    
   