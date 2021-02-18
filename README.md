# CSO Network Gas HTML to GeoJSON

This repository contains a `Jupyter Notebook` that:

- Converts [CSO Network Gas Consumption data](https://www.cso.ie/en/releasesandpublications/er/ngc/networkedgasconsumption2019/) from `HTML` to `pandas.DataFrame`
- Extracts Dublin Postcode data
- Links each Poscode to it's corresponding boundary geometry
- Saves the result for each table as a `GeoJson` file

The results can be accessed directly from the [Zenodo Page](https://zenodo.org/record/4545792)

## Installation

Install [Anaconda or Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#installing-conda-on-a-system-that-has-other-python-installations-or-packages)

> If you are using Windows you may want to install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

In your terminal run:
```bash
conda env create --file environment.yml 
```

And open the `py` files in [`Jupyter Notebook`](https://jupyter.org/) or [`vscode`](https://code.visualstudio.com/) 