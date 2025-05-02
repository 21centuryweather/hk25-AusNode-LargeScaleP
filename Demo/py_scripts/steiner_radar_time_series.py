#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


from scipy import ndimage
from skimage.measure import label
from tqdm import tqdm
import re
from multiprocess import Pool
import os


# Following Louf et al. (2019), we only need take wet seasons (October to April)
# 
# The simulation is from 2020-03-01 to 2021-02-28
# 
# So data between 2020-04-30 and 2020-09-30 are not considered for now

# I'll test with Steiner classification first and then just use the precipitation threshold (with object size more than 5 grid points in radar to remove some ground clutter)

# In[3]:


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


# In[4]:


def calc_clouds(yyyymmdd):
    ## initialisation
    steiner_file = f"/g/data/rq0/level_2/63/STEINER/63_{yyyymmdd}_steiner.nc"
    if os.path.exists(steiner_file):
        ds_radar = xr.open_dataset(steiner_file)
        radar_area = 70661#len(np.argwhere(~np.isnan(ds_radar["steiner"].isel(time=0).values)))
        ds_prcp = xr.open_dataset(f"/g/data/rq0/admin/level_2_decomissioned_fields/63/RAINRATE/63_{yyyymmdd}_rainrate.nc")
        ## array to store object number
        num_obj_arr = np.zeros(len(ds_radar.time))
        
        ## array for total area
        tot_area_arr = np.zeros(len(ds_radar.time))
        ## array to store mean cell size
        mean_obj_area_arr = np.zeros(len(ds_radar.time))
        ## array to store convective area fraction
        area_frac_arr = np.zeros(len(ds_radar.time))
        ## mean precipitation over convective area
        cvt_mean_prcp_arr = np.zeros(len(ds_radar.time))
        ## mean precipitation over the entire radar scan
        tot_mean_prcp_arr = np.zeros(len(ds_radar.time))
        ## total convective precipitation
        cvt_tot_prcp_arr = np.zeros(len(ds_radar.time))
        
        for its in range(0,len(ds_radar.time)):
            data = ds_radar["steiner"].isel(time=its)
            prcp = ds_prcp["rainrate"].isel(time=its)
            cvt_prcp = np.sum(prcp.values[data.values==2])    
            cv_obj = data.copy().fillna(0)
            cv_obj.values[cv_obj.values < 2] = 0
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
                "time":  ds_radar.time.values,
            },
        )
        out.to_netcdf(f"/scratch/xp65/dl6968/prep_hk25/steiner_ts/number_size_{yyyymmdd}.nc")
        out.close()
        ds_radar.close()
        ds_prcp.close()


# In[6]:


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




