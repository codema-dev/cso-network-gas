# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: 'Python 3.9.1 64-bit (''cso-network-gas'': conda)'
#     metadata:
#       interpreter:
#         hash: b61c169e19bc7874f8b9dc129b8bf2779b9e66e59b5e90264a492b9ef4b9b65d
#     name: python3
# ---

# %%
import geopandas as gpd
import numpy as np
import pandas as pd

from clean import amalgamate_postal_districts

# %%
years = [str(2011 + i) for i in range(0, 9, 1)]

# %% [markdown]
# # Get Dublin Postcode Boundaries

# %%
dublin_postcode_boundaries = gpd.read_file("data/dublin_postcode_boundaries").pipe(amalgamate_postal_districts)

# %% [markdown]
# # Get Residential Average Gas Consumption

# %%
resi_total_annual_gas_by_postcodes = gpd.read_file("data/resi_total_annual_gas_by_postcodes.geojson", driver="GeoJSON")

# %%
resi_total_meters_by_postcodes = gpd.read_file("data/resi_total_meters_by_postcodes.geojson", driver="GeoJSON")

# %%
resi_avg_annual_gas_by_postcodes = resi_total_annual_gas_by_postcodes.copy()
resi_avg_annual_gas_by_postcodes.loc[:, years] = np.round(
    1*10**6 * resi_total_annual_gas_by_postcodes[years].astype(np.int64) / resi_total_meters_by_postcodes[years].astype(np.int64),
    0,
)


# %%
resi_avg_annual_gas_by_postcodes.to_file("data/resi_avg_annual_gas_by_postcodes.geojson", driver="GeoJSON")

# %% [markdown]
# # Get Non-Residential Average Gas Consumption

# %%
non_resi_total_annual_gas_by_postcodes = gpd.read_file("data/non_resi_total_annual_gas_by_postcodes.geojson", driver="GeoJSON")

# %%
non_resi_total_annual_gas_dublin_postal_districts = (
    non_resi_total_annual_gas_by_postcodes
    .query("`postcodes` != 'Co. Dublin'")
    .loc[:, years]
    .sum()
    .to_frame().T
    .assign(postcodes="Dublin Postal Districts")
    .merge(dublin_postcode_boundaries)
)

# %%
non_resi_total_annual_gas_dublin_postal_districts

# %%
non_resi_total_annual_gas_by_postcodes = pd.concat(
    [
        non_resi_total_annual_gas_by_postcodes,
        non_resi_total_annual_gas_dublin_postal_districts,
    ]
).query("`postcodes` == ['Co. Dublin', 'Dublin Postal Districts']").reset_index(drop=True)

# %%
non_resi_total_annual_gas_by_postcodes

# %%
non_resi_total_annual_gas_by_postcodes.loc["Dublin Postal Districts", years] = non_resi_total_annual_gas_dublin_postal_districts

# %%
non_resi_total_meters_by_postcodes = gpd.read_file("data/non_resi_total_meters_by_postcodes.geojson", driver="GeoJSON")
non_resi_total_meters_by_postcodes.loc[:, years] = non_resi_total_meters_by_postcodes[years].astype(np.int64)

# %%
non_resi_total_annual_gas_by_postcodes

# %%
non_resi_avg_annual_gas_by_postcodes = non_resi_total_annual_gas_by_postcodes.copy()
non_resi_avg_annual_gas_by_postcodes.loc[:, years] = 1*10**6 * non_resi_total_annual_gas_by_postcodes[years] / non_resi_total_meters_by_postcodes[years]
non_resi_avg_annual_gas_by_postcodes.loc[:, years] = non_resi_avg_annual_gas_by_postcodes[years].round(0)

# %%
non_resi_avg_annual_gas_by_postcodes
