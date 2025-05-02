# The relationship of cloud size and number with large-scale environment for precipitation in high-resolution models  <img src='https://21centuryweather.org.au/wp-content/uploads/Hackathon-Image-WCRP-Positive-1536x736.jpg' align="right" height="139" />

Simulating clouds remains one of the greatest challenges in global climate models. Convective clouds, in particular, are often much smaller than the grid size of traditional global climate models. As a result, these models rely on convective parameterisation schemes that assume quasi-equilibrium between the large-scale environment and the convective processes within each grid box. However, as model resolution gets finer, this assumption breaks down — especially when convection occupies a significant portion of a grid cell.

[Louf et al. (2019)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019GL083964) examined how the size and number of clouds relate to their large-scale environment in regions of deep tropical convection. Using radar data from Darwin, Australia, and environmental conditions derived from a blend of ECMWF analyses and observations, they found that the strongest rainfall doesn't always align with the most intense convection at the model grid scale.

In this Hackathon, we are using high-resolution models that omit several traditional parameterisations, including those for convection, gravity waves, and the boundary layer. However, removing these schemes introduces new challenges: some high-resolution models may now produce storms that are smaller than those presented in the observations. This project explores whether these high-resolution models can reproduce the environmental conditions and precipitation patterns similar to those in Louf et al. (2019), and how these features differ across models.

See more description [here](https://github.com/dongqi-DQ/hk25-teams/blob/main/hk25-AusNode/hk25-AusNode-LargeScaleP.md).

**Project leads:**  

Dongqi Lin ([@dongqi-DQ](https://github.com/dongqi-DQ)), Monash University ([dongqi.lin@monash.edu](dongqi.lin@monash.edu))  

Yi-Xian Li ([@y-x-li](https://github.com/y-x-li)), Monash University ([yi-xian.li@monash.edu](yi-xian.li@monash.edu))  


**Project members:**   


Name, affiliation/github username

**Collaborators:** 
- This project overlaps with the Mesoscale Degree of Organization (hk25-AusNode-DOCmeso)
- and perhaps some projects in other nodes (e.g. [hk25-CloudClimato](https://github.com/digital-earths-global-hackathon/hk25-teams/tree/main/hk25-CloudClimato))

**Data:**
- Region of interest: northern Australia and the maritime continent
- 2D output variables (1hr instantaneous): precipitation_flux (pr), toa_outgoing_longwave_flux (rlut)
- 2D output variables (3hr mean): precipitation_flux (pr), toa_outgoing_longwave_flux (rlut), cloud_area_fraction (clt)
- 3D output variables (6hr instantaneous): upward_air_velocity (wa), relative_humidity (hur), temperature (ta)
- Darwin radar and ERA5 are available on NCI ([`rq0`](https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f4093_2998_3846_6573) and [`rt52`](https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f2836_1346_3774_9763))
- Potentially any radar in the tropics, or satellite data if anyone or any node has the data

**Demonstration code:**  

Demo scripts can be found in [Demo](/Demo/). These scripts replicate Figures 1 and 2 in Louf et al. (2019) using the Darwin radar and ERA5 for the wet season between 2020-03-01 and 2021-02-28 (the high-res model simulation period). For fast CAPE calculation, refer to [calc_xcape.py](/Demo/py_scripts/calc_xcape.py). 

We may need to have a separate Python environment for the XCAPE pacakge. Follow the [instructions](Instructions_for_python_environment.md) if you are not familiar with conda environment handling.

More instructions about the hackathon can be found [here](https://github.com/21centuryweather/hackathon-2025-australia-node). 

## Contributing Guidelines

> The group will decide how to work as a team. This is only an example. 

This section outlines the guidelines to ensure everyone can work and collaborate. All project members have write access to this repository, to avoid overlapping and merge issues make sure you discuss the plan and any changes to existing code or analysis.

### Project organisation

All tasks and activities will be managed through GitHub Issues. While most discussions will take place face-to-face, it is important to document the main ideas and decisions on an issue. Issues will be assigned to one or more people and classified using labels. If you want to work on an issue, comment and make sure is assigned to you to avoid overlapping. If you find a problem in the code or a new task, you can open an issue. 

### How to collaborate

* **Main branch:** We want to keep things simple, if you are working on a notebook alone you can push changes to the main branch. Make sure to 1) only add and ccommit that file and nothing else, 2) pull from the remote repo and 3) push.

* **Working on a branch:** if you want to fix or propose a change to someone else code you will need to create a branch and open a pull request. Make sure you explain your suggestion in the pull request message. **This also applies to collaborators outside the project team.**

### Repository structure

This is how the project should look like but make sure to change the name `template-hackathon-project` to something meaningful. 

```bash
template-hackathon-project/
├── LICENCE
├── README.md
├── template_project_hackathon
│   ├── analysis.py
│   ├── __init__.py
│   └── read.py
└── tests
    ├── test_analysis.py
    └── test_read.py
```
* `template_hackathon_project/` this folder will include the code to analysis the data.
* `tests/` this folder contains test code that verifies that your code does what it should.

