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
raw_target_info = pd.read_csv("input_obs_data.csv")

### Creating new dataframe with first date each target was observed
subset_df = raw_target_info[["Target","Date"]]
grouped_and_first_df = subset_df.groupby(["Target"]).first()
grouped_and_first_df["N"] = subset_df.groupby(["Target"]).nunique()
grouped_and_first_df

### Creating new dataframe with target name, date it was first observed, and N
new_df = grouped_and_first_df.reset_index()
new_df.columns = ["Name","first_date","N"]
new_df.tail(5)

### Preparation for querying data from JPL Horizons
target_location = '474' # Mt. John Observatory MPC code

obsDate_lst = []
for i in new_df["first_date"]:
    obsDate_lst.append(i)

targetname_lst = []
for i in new_df.Name:
    targetname_lst.append(i)

# need to convert epoch date to julian date
jd_obsDate_lst = []
for i in obsDate_lst:
    dt = dateutil.parser.parse(obsDate_lst[0]) 
    time = astropy.time.Time(dt)
    jd_obsDate_lst.append(time.jd)

### Querying information from JPL Horizons database
eph_lst = []
el_lst = []
obj_lst = []
for index,jdDate in enumerate(jd_obsDate_lst):
    # setting an exception for C/2018 F4 because it has fragmented and gives an error otherwise
    if targetname_lst[index] == "C/2018 F4": 
        obj = Horizons(id='90004395', epochs=jdDate)
        eph_lst.append(obj.ephemerides()) #from eph, only need 'r' heliocentric distance
        el_lst.append(obj.elements()) #from elems, need a0 (semimajor axis), q, and T (perihelion date)
    else:
        obj = Horizons(id=targetname_lst[index], epochs=jdDate)
        obj_lst.append(obj)
        eph_lst.append(obj.ephemerides()) #from eph, only need 'r' heliocentric distance
        el_lst.append(obj.elements()) #from elems, need a0 (semimajor axis), q, and T (perihelion date)

# to check elements returned by obj.elements, see:
# https://astroquery.readthedocs.io/en/latest/api/astroquery.jplhorizons.HorizonsClass.html#astroquery.jplhorizons.HorizonsClass.elements

### Combining ephemerides and elements info into single array
final_array = []
for index,target in enumerate(eph_lst):
    final_array.append([el_lst[index]['a'][0],eph_lst[index]['r'][0],
                        el_lst[index]['q'][0],el_lst[index]['Tp_jd'][0]])

### Converting array to dataframe and formatting
eph_el_df = pd.DataFrame(final_array,columns=['a','r','q','T'])
final_new_df = pd.concat([new_df,eph_el_df],axis=1)
final_new_df = final_new_df[['Name','first_date','a','N','r','q','T']]
final_new_df['T'] = final_new_df['T'].map(lambda name: Time(name, format='jd').to_value('iso')[:10])
final_new_df['a'] = np.round(final_new_df['a'], decimals = 6)
final_new_df['r'] = np.round(final_new_df['r'], decimals = 2)
final_new_df['q'] = np.round(final_new_df['q'], decimals = 2)
final_new_df = final_new_df.drop(columns="first_date")
final_column_names = ['Name','$a_0$ [au]','N','$r_0$ [au]','$q$ [au]','T']
final_new_df.columns = final_column_names

### Writing as CSV and Latex
final_new_df.to_csv("final_look_table.csv")
final_look_table = Table.from_pandas(final_new_df)
ascii.write(final_look_table,format="latex",
            formats={'$a_0$ [au]':'%12.6f'})