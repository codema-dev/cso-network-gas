# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from os import path
from shutil import unpack_archive
from urllib.request import urlretrieve

import geopandas as gpd
import pandas as pd

from clean import amalgamate_postal_districts
from link import link_counties_and_postal_districts_to_postcode_boundaries
from link import link_counties_to_postcode_boundaries

# %% [markdown]
# # Get Dublin Postcode Boundaries

# %%
if not path.exists("data/dublin_postcode_boundaries"):
    urlretrieve(
        url="https://zenodo.org/record/4327005/files/dublin_postcode_boundaries.zip",
        filename="data/dublin_postcode_boundaries.zip"
    )
    unpack_archive("data/dublin_postcode_boundaries.zip", "data")
    
dublin_postcode_boundaries = gpd.read_file("data/dublin_postcode_boundaries").pipe(amalgamate_postal_districts)

# %% [markdown]
# # Convert HTML to a list of pandas.DataFrame

# %%
raw_gas_tables = pd.read_html("https://www.cso.ie/en/releasesandpublications/er/ngc/networkedgasconsumption2019/")

# %% [markdown]
# # Link Residential (resi) total annual gas demand to Postcode Boundaries

# %%
resi_total_annual_gas_by_postcodes = link_counties_and_postal_districts_to_postcode_boundaries(
    raw_gas_tables=raw_gas_tables,
    dublin_postcode_boundaries=dublin_postcode_boundaries,
    postal_district_table_index=11,
    county_table_index=9,
)

# %%
resi_total_annual_gas_by_postcodes.to_file(
    "data/resi_total_annual_gas_by_postcodes.geojson",
    driver="GeoJSON",
)

# %% [markdown]
# # Link Non-residential (non_resi) total annual gas demand to Postcode Boundaries

# %%
non_resi_total_annual_gas_by_postcodes = link_counties_and_postal_districts_to_postcode_boundaries(
    raw_gas_tables=raw_gas_tables,
    dublin_postcode_boundaries=dublin_postcode_boundaries,
    postal_district_table_index=10,
    county_table_index=8,
)

# %%
non_resi_total_annual_gas_by_postcodes.to_file(
    "data/non_resi_total_annual_gas_by_postcodes.geojson",
    driver="GeoJSON",
)

# %% [markdown]
# # Link Residential (resi) median annual gas demand to Postcode Boundaries

# %%
resi_median_annual_gas_by_postcodes = link_counties_and_postal_districts_to_postcode_boundaries(
    raw_gas_tables=raw_gas_tables,
    dublin_postcode_boundaries=dublin_postcode_boundaries,
    postal_district_table_index=14,
    county_table_index=13,
)

# %%
resi_median_annual_gas_by_postcodes.to_file(
    "data/resi_median_annual_gas_by_postcodes.geojson",
    driver="GeoJSON"
)

# %% [markdown]
# # Link Residential (resi) meters to Postcode Boundaries

# %%
resi_total_meters_by_postcodes = link_counties_and_postal_districts_to_postcode_boundaries(
    raw_gas_tables=raw_gas_tables,
    dublin_postcode_boundaries=dublin_postcode_boundaries,
    postal_district_table_index=19,
    county_table_index=18,
)

# %%
resi_total_meters_by_postcodes.to_file(
    "data/resi_total_meters_by_postcodes.geojson",
    driver="GeoJSON",
)

# %% [markdown]
# # Link Non-residential (non_resi) meters to Postcode Boundaries

# %%
non_resi_total_meters_by_postcodes = link_counties_to_postcode_boundaries(
    raw_gas_tables=raw_gas_tables,
    dublin_postcode_boundaries=dublin_postcode_boundaries,
    county_table_index=-3,
)

# %%
non_resi_total_meters_by_postcodes.to_file(
    "data/non_resi_total_meters_by_postcodes.geojson",
    driver="GeoJSON",
)
