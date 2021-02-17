import re

import geopandas as gpd
import pandas as pd


def _replace_column_names_with_third_row(df):

    columns = df.iloc[2].tolist()
    df.columns = columns

    return df.drop(index=[0, 1, 2]).reset_index(drop=True)


def clean_dublin_postal_districts(dublin_postal_districts):

    return (
        dublin_postal_districts.pipe(_replace_column_names_with_third_row)
        .assign(
            postcodes=lambda df: df["Dublin Postal District"].str.replace(
                pat=r"""     # Replace all substrings
                    0        # starting with 0
                    (?=\d)   # followed by a number
                    """,
                repl="",  # with an empty string
                flags=re.VERBOSE,
            )
        )
        .dropna(how="all")
        .drop(columns="Dublin Postal District")
        .drop(23)  # row number of 'Total'
    )


def get_county_dublin(counties):

    return (
        counties.pipe(_replace_column_names_with_third_row)
        .iloc[4:5]  # index of 'Dublin County'
        .rename(columns={"County": "postcodes"})
        .replace({"Dublin County": "Co. Dublin"})
    )


def clean_dublin_counties(counties):

    return (
        counties.pipe(_replace_column_names_with_third_row)
        .iloc[4:6]  # index of 'Dublin County' & 'Dublin Postal Districts'
        .rename(columns={"County": "postcodes"})
        .replace({"Dublin County": "Co. Dublin"})
    )


def amalgamate_postal_districts(dublin_postcode_boundaries):

    dublin_postal_districts = (
        dublin_postcode_boundaries.assign(x=0)
        .query("`postcodes` != 'Co. Dublin'")
        .dissolve("x")
        .reset_index(drop=True)
        .replace({"Dublin 1": "Dublin Postal Districts"})
    )

    dublin_postcode_boundaries = pd.concat(
        [dublin_postcode_boundaries, dublin_postal_districts]
    )
    return gpd.GeoDataFrame(dublin_postcode_boundaries).reset_index(drop=True)
