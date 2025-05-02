#!/usr/bin/env python
import argparse
import numpy as np
import xarray as xr
from tqdm import tqdm
from xcape.core import calc_cape
import os


def xcape_calc(its, ds_t, ds_tdew, plvl):
    ta_surf = ds_t["t"].isel(level=0).stack(ngrid=('latitude','longitude'))-273.15
    td_surf = ds_tdew["tdew"].isel(level=0).stack(ngrid=('latitude','longitude'))-273.15
    
    ta_da = ds_t["t"].stack(ngrid=('latitude','longitude')).transpose('ngrid','level')-273.15
    td_da = ds_tdew["tdew"].stack(ngrid=('latitude','longitude')).transpose('ngrid','level')-273.15
    ta_val = ta_da.load().values
    td_val = td_da.load().values
    psurf = np.zeros(ta_val.shape[0])
    psurf[:] = plvl[0].values
    cape, cin, mulev, zmulev = calc_cape(plvl, ta_val, td_val, 
                                         psurf,ta_surf, 
                                         td_surf,
                                         source ='most-unstable', vertical_lev="pressure")
    cape_2d = cape.reshape(ds_t.latitude.shape[0],ds_t.longitude.shape[0])
    cin_2d = cin.reshape(ds_t.latitude.shape[0],ds_t.longitude.shape[0])

    return cape_2d, cin_2d


def main(idx,year):
    if not os.path.exists(f"/scratch/k10/dl6968/ERA5_AU/xcape/{year}/cape_cin_{year}_time{idx:04d}.nc"):
        # load only one time step
        ds_t = xr.open_mfdataset(
            f"/scratch/k10/dl6968/ERA5_AU/t/levels/aus_t_lft_{year}_plevel*.nc",
            combine="nested", concat_dim="level", parallel=False
        ).isel(time=idx)
    
        ds_tdew = xr.open_mfdataset(
            f"/scratch/k10/dl6968/ERA5_AU/tdew/tdew_{year}*.nc",
            combine="nested", concat_dim="level", parallel=False
        ).isel(time=idx)
        ## flip the pressure levels bcos so it goes from surface (descending order)
        ds_t = ds_t.chunk({'level': -1, 'latitude':20, 'longitude':20}) \
                   .transpose("latitude","longitude","level").isel(level=slice(None, None, -1))
        ds_tdew = ds_tdew.chunk({'level': -1, 'latitude':20, 'longitude':20}) \
                         .transpose("latitude","longitude","level").isel(level=slice(None, None, -1))
    
        plvl = ds_t.level
    
        cape_2d, cin_2d = xcape_calc(idx, ds_t, ds_tdew, plvl)
    
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
        out.to_netcdf(f"/scratch/k10/dl6968/ERA5_AU/xcape/{year}/cape_cin_{year}_time{idx:04d}.nc")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "time_index",
        type=int,
        help="which time slice to process (0-based)"
    )
    parser.add_argument(
        "year",
        type=int,
        help="4-digit year to select from the files"
    )
    args = parser.parse_args()
    main(args.time_index, args.year)


