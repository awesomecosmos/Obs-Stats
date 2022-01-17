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

raw_target_info = pd.read_csv("Lister2022/look_table.csv")



subset_df = raw_target_info[["Target","Date"]]
grouped_and_first_df = subset_df.groupby(["Target"]).first()
print(len(grouped_and_first_df))
print(type(grouped_and_first_df))

#print(len(target_val_counts))
#print(raw_target_info.Target.unique())
#print(len(raw_target_info.Target.unique()))

#new_tbl = pd.Series([target_val_counts.iloc[0],target_val_counts.iloc[1]],index=["Name","N"])
#print(new_tbl.head())
#target_val_counts = raw_target_info.Target.value_counts().rename_axis("Name").to_frame("N")
target_val_counts = pd.DataFrame(raw_target_info.Target.value_counts())
df_val_counts = target_val_counts.reset_index()
df_val_counts.columns = ["Name","N"]
#print(df_val_counts)




#print(subset_df.sort_values(by="Date",ascending=True))

# grouped_df = subset_df.groupby(["Date"]).first()
# print(grouped_df)
# raw_target_info.groupby(["Target","Date"]).first()
#grouped_df = grouped_df.first().sort_values(by="Date",ascending=True)
#new_grouped_df = 
#print(grouped_df)