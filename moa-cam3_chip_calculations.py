# -*- coding: utf-8 -*-

###############################################################################
#---------------------MOA-CAM3 CHIP SIZE CALCULATIONS-------------------------#
###############################################################################

# This is a Python script for quick MOA-cam3 chip calculations
# MOA-cam3 is a CCD camera with 10 chips arranged in a 5x2 array
# Reference for values: Sako et al., 2008 
# (https://arxiv.org/abs/0804.0653)

import numpy as np

# area of 1 pixel (pixel size) = (15 * 10 ** -6) m^2
pixel_size = 0.58 #arcsec squared

# dimensions of 1 pixel (assuming square pixel shape)
pixel_side = np.sqrt(pixel_size)

# dimensions of chip
chip_length_pixels = 4000 #pixels
chip_length_arcsec = pixel_side * chip_length_pixels
chip_length_arcmin = chip_length_arcsec / 60
chip_length_deg = chip_length_arcmin / 60

chip_width_pixels = 2000 #pixels
chip_width_arcsec = pixel_side * chip_width_pixels
chip_width_arcmin = chip_width_arcsec / 60
chip_width_deg = chip_width_arcmin / 60

chip_area_arcsec = chip_length_arcsec * chip_width_arcsec
chip_area_arcmin = chip_length_arcmin * chip_width_arcmin
chip_area_deg = chip_length_deg * chip_width_deg