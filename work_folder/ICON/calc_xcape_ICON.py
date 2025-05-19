#!/usr/bin/env python
import argparse
import numpy as np
import xarray as xr
from tqdm import tqdm
from xcape.core import calc_cape
import os


def xcape_calc(ds_t, plvl, ta_val, td_val, psurf,ta_surf, tdew_surf):

    cape, cin, mulev, zmulev = calc_cape(plvl, ta_val, td_val, 
                                         psurf,ta_surf, 
                                         tdew_surf,
                                         source ='most-unstable', vertical_lev="pressure")
    
    cape_2d = cape.reshape(ds_t.latitude.shape[0],ds_t.longitude.shape[0])
    cin_2d = cin.reshape(ds_t.latitude.shape[0],ds_t.longitude.shape[0])

    return cape_2d, cin_2d


def main(idx):
    if not os.path.exists(f"/scratch/nf33/hk25_LSP/Germany/MC/cape_cin/cape_cin_time{idx:04d}.nc"):
        # load only one time step
        ds_t = xr.open_dataset(
            "/scratch/nf33/hk25_LSP/Germany/MC/ta_6hourly.nc").isel(time=idx)
    
        ds_tdew = xr.open_dataset(
            "/scratch/nf33/hk25_LSP/Germany/MC/tdew_6hourly.nc").isel(time=idx)
        
        ## flip the pressure levels bcos so it goes from surface (descending order)
        ta_da = ds_t["ta"].stack(ngrid=('latitude','longitude'))\
        .isel(pressure=slice(None, None, -1)).transpose('ngrid','pressure')-273.15
        tdew_da = ds_tdew["tdew"].stack(ngrid=('latitude','longitude'))\
        .isel(pressure=slice(None, None, -1)).transpose('ngrid','pressure')-273.15

        ta_surf = ds_t["ta"].isel(pressure=-1).stack(ngrid=('latitude','longitude')).values.flatten()-273.15
        tdew_surf = ds_tdew["tdew"].isel(pressure=-1).stack(ngrid=('latitude','longitude')).values.flatten()-273.15
                
        ta_val = ta_da.load().values
        td_val = tdew_da.load().values
        psurf = np.zeros(ta_val.shape[0])
        psurf[:] = 1000
        # ICON pressure is in Pa not hPa
        plvl = ds_t.pressure.isel(pressure=slice(None, None, -1)).values.astype(float)/100        
        
        cape_2d, cin_2d = xcape_calc(ds_t,plvl, ta_val, td_val, 
                                    psurf,ta_surf, tdew_surf)
    
        # write out a per‐index NetCDF
        out = xr.Dataset(
            {
                "cape": (("latitude","longitude"), cape_2d),
                "cin":  (("latitude","longitude"), cin_2d),
            },
            coords={
                "latitude": ds_t.latitude,
                "longitude": ds_t.longitude,
                "time":      [ds_t.time.values],
            },
        )
        out.to_netcdf(f"/scratch/nf33/hk25_LSP/Germany/MC/cape_cin/cape_cin_time{idx:04d}.nc")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "time_index",
        type=int,
        help="which time slice to process (0-based)"
    )
    args = parser.parse_args()
    main(args.time_index)


