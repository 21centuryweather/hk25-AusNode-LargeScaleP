# How to create your own Conda environment and work with ARE

## 1. Use existing conda to create a new environment 
Specify the location and name for the environment

```
conda create --prefix /your_directory/xcape_env 
```

## 2. Activate the new environment

```
conda activate /your_directory/xcape_env
```

## 3. Install the XCAPE package 

```
conda install -c conda-forge xcape
```

Use conda or pip later to install other pacakges you need. 

## 4. Install an ipython kernal so the ARE jupyter can see

```
conda install ipykernel  
ipython kernel install --user --name=xcape_env   
```

