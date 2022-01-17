#importing useful packages
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.io import ascii
import astropy.time
from astropy.time import Time
import astropy.table
from astropy.table import Table, Column, MaskedColumn
from astroplan import Observer
from astroquery.jplhorizons import Horizons
import pandas as pd
import csv
import astropy.time
import dateutil.parser

### Reading CSV file of dates targets were observed
raw_target_info = pd.read_csv("Lister2022/look_table.csv")

### Creating new dataframe with first date each target was observed
subset_df = raw_target_info[["Target","Date"]]
grouped_and_first_df = subset_df.groupby(["Target"]).first()
new_df = grouped_and_first_df.reset_index()
new_df.columns = ["Name","N"]

### 
target_location = '474'

obsDate_lst = []
for i in new_df.N:
    obsDate_lst.append(i)

targetname_lst = []
for i in new_df.Name:
    targetname_lst.append(i)

# need to convert epoch date to julian date
jd_obsDate_lst = []
for i in obsDate_lst:
    dt = dateutil.parser.parse(obsDate_lst[0]) #'2012.11.07'
    time = astropy.time.Time(dt)
    jd_obsDate_lst.append(time.jd)

# #need to query information from JPL Horizons database
eph_lst = []
el_lst = []
obj_lst = []
for index,jdDate in enumerate(jd_obsDate_lst):
    if targetname_lst[index] == "C/2018 F4":
        obj = Horizons(id='90004395', location=target_location,epochs=jdDate)
    else:
        obj = Horizons(id=targetname_lst[index], location=target_location,epochs=jdDate)
    obj_lst.append(obj)
    # eph_lst.append(obj.ephemerides())
    # el_lst.append(obj.elements())
yolo = obj_lst[1]
print(yolo)
print(yolo.elements())
# for i in obj_lst:
#     try:
#         print(i.elements())
#     except:
#         pass
# print(el_lst)
# #now we need to make the JPL data and the FITS data into tables
# JPLtableData = eph_lst['datetime_str','datetime_jd','RA','DEC','RA_rate','DEC_rate','Tmag','airmass','r','r_rate','delta','delta_rate','elong','alpha','constellation','EL']
# JPL_colnames = ['datetime_str','datetime_jd','RA','DEC','RA_rate','DEC_rate','Tmag','airmass','r','r_rate','delta','delta_rate','elong','alpha','constellation','EL']
# JPL_astropy_tbl = Table(JPLtableData,names=JPL_colnames)