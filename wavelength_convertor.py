# -*- coding: utf-8 -*-

import numpy as np
from astropy import units as u

# u.Angstrom, u.m, u.nm, u.micron
def wavelength_convertor(input_wavelength,input_unit,output_unit):
    input_lambda = input_wavelength * input_unit
    output_lambda = input_lambda.to(output_unit)
    return output_lambda

def wavelength_category(output_lambda):
    wavelength_m = output_lambda.to(u.m)
    classification = None
    if wavelength_m >= 1.1e-3 and wavelength_m < 10000 * u.kilometer:
        classification == 'radio'
    if wavelength_m >= 1.1e-3 and wavelength_m < 1:
        classification == 'microwave'

# add func that generates a table converting between all quantities
# make this into a class