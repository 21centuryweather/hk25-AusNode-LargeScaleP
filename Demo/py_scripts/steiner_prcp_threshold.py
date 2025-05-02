#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.measure import label
from tqdm import tqdm
import re
from multiprocess import Pool
import os
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=RuntimeWarning)


# In[ ]:


import pandas as pd

# Create full date range from 2020-03-01 to 2021-02-28
full_range = pd.date_range(start="2020-03-01", end="2021-02-28", freq="D")

# Define exclusion period
exclude_start = pd.Timestamp("2020-05-01")
exclude_end = pd.Timestamp("2020-09-30")

# Filter out the excluded range
filtered_range = full_range[(full_range < exclude_start) | (full_range > exclude_end)]

# Convert to list of strings in yyyymmdd format
date_str_list = filtered_range.strftime("%Y%m%d").tolist()


# Use the threshold of 6 mm h-1 as in Johnson and Hamilton (1988)

# In[ ]:


def calc_clouds(yyyymmdd):
    ds_prcp = xr.open_dataset(f"/g/data/rq0/admin/level_2_decomissioned_fields/63/RAINRATE/63_{yyyymmdd}_rainrate.nc")
    radar_area = 70661
    ## initialisation
    num_obj_arr = np.zeros(len(ds_prcp.time))
    
    ## array for total area
    tot_area_arr = np.zeros(len(ds_prcp.time))
    ## array to store mean cell size
    mean_obj_area_arr = np.zeros(len(ds_prcp.time))
    ## array to store convective area fraction
    area_frac_arr = np.zeros(len(ds_prcp.time))
    ## mean precipitation over convective area
    cvt_mean_prcp_arr = np.zeros(len(ds_prcp.time))
    ## mean precipitation over the entire radar scan
    tot_mean_prcp_arr = np.zeros(len(ds_prcp.time))
    ## total convective precipitation
    cvt_tot_prcp_arr = np.zeros(len(ds_prcp.time))
    
    for its in range(0,len(ds_prcp.time)):
        # data = ds_prcp["steiner"].isel(time=its)
        prcp = ds_prcp["rainrate"].isel(time=its)
        cvt_prcp = np.sum(prcp.values[prcp.values>=6])    
        cv_obj = prcp.copy().fillna(0)
        cv_obj.values[cv_obj.values < 6] = 0
        cv_obj.values[cv_obj.values >= 6] = 6
        ## use scikit learn to label
        label_arr = label(cv_obj)
        ## find unique objects
        unique_label = np.unique(label_arr)
        ## get the number of objects 
        num_obj_arr[its] = len(unique_label) - 1   ## the background is 0
        ## individual object area
        ind_obj_area = np.zeros(len(unique_label) - 1)
        
        for i in unique_label:
            if i == 0:
                continue
            else:
                ind_obj_area[i-1]= np.sum(label_arr == i) ## the data is 1 km by 1 km so this is exactly the area
                ## this may be needed for precip thresholds
                # if obj_area <=5:
                #     label_new[label_new==i] = 0
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            
            tot_area_arr[its] = np.sum(ind_obj_area)
            mean_obj_area_arr[its] = tot_area_arr[its]/num_obj_arr[its]
            area_frac_arr[its] = tot_area_arr[its]/radar_area
        
            cvt_mean_prcp_arr[its] = cvt_prcp/tot_area_arr[its]
            tot_mean_prcp_arr[its] = cvt_prcp/radar_area
            cvt_tot_prcp_arr[its] = cvt_prcp
        
        ## save to netcdf
        out = xr.Dataset(
            {
                "num_obj": (("time"), num_obj_arr),
                "tot_area":  (("time"), tot_area_arr),
                "mean_obj_area":  (("time"), mean_obj_area_arr),
                "area_frac":  (("time"), area_frac_arr),
                "cvt_mean_prcp":  (("time"), cvt_mean_prcp_arr),
                "tot_mean_prcp":  (("time"), tot_mean_prcp_arr),
                "cvt_tot_prcp":  (("time"), cvt_tot_prcp_arr),
                
            },
            coords={
                "time":  ds_prcp.time.values,
            },
        )
        out.to_netcdf(f"/scratch/k10/dl6968/prep_hk25/prcp_ts/number_size_{yyyymmdd}.nc")
        out.close()
        ds_prcp.close()


# In[ ]:


## parallelise this
max_pool=24

with Pool(max_pool) as p:
    pool_outputs = list(
        tqdm(
            p.imap(calc_clouds,
                   date_str_list),
            total=len(date_str_list),
            position=0, leave=True
        )
    )
p.join()


# In[ ]:




