# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 15:26:59 2021

@author: ave41
"""

#importing useful packages
import matplotlib.pyplot as plt
import numpy as np
import os
#---
from astropy.io import fits
from astropy.io import ascii
import astropy.time
from astropy.time import Time
import astropy.table
from astropy.table import Table, Column, MaskedColumn
#---
from astroplan import Observer
from astroquery.jplhorizons import Horizons
#---
import pandas as pd
import csv

#%%
code_path = "C:/Users/aayus/OneDrive - University of Canterbury/Master's 2021/ASTR480 Research/ASTR480 Code/Observations-Stats"
os.chdir(code_path) #from now on, we are in this directory

#%%
obsDate_lst = ['2021-02-11T00:00:00','2021-02-12T00:00:00','2021-02-13T00:00:00','2021-02-18T00:00:00']
obsDate_lst_for_display = ['2021-02-11','2021-02-12','2021-02-13','2021-02-18']
target_name = 'C/2021 A7'
target_location = '474'
#%%
#need to convert epoch date from 'fits' type to julian date
jd_obsDate_lst = []
for i in obsDate_lst:
    t = Time(i, format='fits', scale='utc')
    jd_obsDate_lst.append(t.jd)

#%%
#need to query information from JPL Horizons database
eph_lst = []
for i in jd_obsDate_lst:
    obj = Horizons(id=target_name, location=target_location,epochs=i)
    eph_lst.append(obj.ephemerides())

#need to query full information from JPL Horizons database
observations = Horizons(id=target_name, location=target_location,epochs=jd_obsDate_lst)
jpl_data = observations.ephemerides()

#%%
#now we need to make the JPL data and the FITS data into tables
JPLtableData = jpl_data['datetime_str','datetime_jd','RA','DEC','RA_rate','DEC_rate','Tmag','airmass','r','r_rate','delta','delta_rate','elong','alpha']
JPL_colnames = ['datetime_str','datetime_jd','RA','DEC','RA_rate','DEC_rate','Tmag','airmass','r','r_rate','delta','delta_rate','elong','alpha']
JPL_astropy_tbl = Table(JPLtableData,names=JPL_colnames)

#%%
#WRITING TABLES!!!
#as an ASCII .dat file
ascii.write(JPL_astropy_tbl,"final_table.dat",overwrite=True)
#as a CSV
ascii.write(JPL_astropy_tbl,"final_table.csv",format="csv",overwrite=True)
#as an HTML file
JPL_astropy_tbl.write('final_table.html',format='jsviewer')
#as Latex code
ascii.write(JPL_astropy_tbl['datetime_str','airmass','r','delta','elong','alpha'],format="latex",
           formats={
                    'airmass':'%12.2f',
                    'r':'%12.2f',
                    'delta':'%12.2f',
                    'elong':'%12.2f',
                    'alpha':'%12.2f'})

#%%
r = []
d = []
t = []
e = []
a = []
m = []
for eph in eph_lst:
    r.append(eph['r'])
    d.append(eph['delta'])
    t.append(eph['datetime_jd'])
    e.append(eph['elong'])
    a.append(eph['alpha'])
    m.append(eph['Tmag'])

plt.figure()
plt.plot(obsDate_lst_for_display,m,"*",color="darkviolet")
plt.xlabel("date")
plt.ylabel("apparent magnitude of {}".format(target_name))
plt.title("Apparent Magnitude of {}".format(target_name))
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("{}_mag.jpeg".format(target_name.replace("/","").replace(" ","_")),dpi=900)
plt.show()

#combo plot of (d vs t) and (r vs t)
#(where d is distance from Earth in AU, r is distance from sun in AU, and t is time in Julian date)
plt.figure()
plt.plot(obsDate_lst_for_display,r,"o",color="gold",markeredgecolor="darkgoldenrod",label="distance from Sun")
plt.plot(obsDate_lst_for_display,d,".",color="dodgerblue",label="distance from Earth")
plt.xlabel("date")
plt.ylabel("distance of {} from Sun/Earth (au)".format(target_name))
plt.title("Distance of {} from Sun and Earth as a function of time".format(target_name))
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("{}_vs_sun_earth_combo.jpeg".format(target_name.replace("/","").replace(" ","_")),dpi=900)
plt.show()

# r vs d (where r is distance from sun in AU and d is distance from Earth in AU)
plt.figure()
plt.plot(r,d,".",color="darkviolet")
plt.xlabel("distance of {} from Sun (au)".format(target_name))
plt.ylabel("distance of {} from Earth (au)".format(target_name))
plt.title("Position of {} in relation to Sun and Earth".format(target_name))
plt.grid(alpha=0.3)
plt.savefig("{}_vs_sun_and_earth.jpeg".format(target_name.replace("/","").replace(" ","_")),dpi=900)
plt.show()

# elong vs alpha (where elong is elongation angle in deg and alpha is phase angle in deg)
plt.figure()
plt.plot(e,a,".",color="darkviolet")
plt.xlabel("elongation angle (degrees)")
plt.ylabel("phase angle (degrees)")
plt.title("Geometry of {} in relation to elongation and phase angles".format(target_name))
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("{}_elong_alpha.jpeg".format(target_name.replace("/","").replace(" ","_")),dpi=900)
plt.show()