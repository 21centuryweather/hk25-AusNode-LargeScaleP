# Demonstration using radar and ERA5

The scripts in this folder is for demonstration using data from Darwin radar and ERA5.

`steiner_radar_time_series.ipynb`: use Steiner classification to extract convective cells
`steiner_prcp_threshold.ipynb`: use rainrate >= 6 mm h-1 to extract convective cells
`pre_process_env_condition.ipynb`: preprocessing scripts to extract environmental conditions from ERA5 and linearly interpolate to radar times

`Demo_figure1_steiner.ipynb`: use Steiner classification results to plot Figure 1 in Louf et al. (2019)
`Demo_figure2_steiner.ipynb`: use Steiner classification results to plot Figure 2 in Louf et al. (2019)
`Demo_figure1_prcp.ipynb`: use rainrate threshold results to plot Figure 1 in Louf et al. (2019)
`Demo_figure2_prcp.ipynb`: use rainrate threshold results to plot Figure 2 in Louf et al. (2019)

`py_scripts`: have all the jupyter notebook in python scripts (use the command in `ipynb2py.sh` to convert)
`bash_xcape.sh`: a demo bash script to run cape and cin calculation parallelly; the `calc_xcape.py` script calculates cape and cin (the demo is for ERA5)



