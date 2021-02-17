import pandas as pd

from clean import get_county_dublin
from clean import clean_dublin_counties
from clean import clean_dublin_postal_districts


def link_counties_and_postal_districts_to_postcode_boundaries(
    raw_gas_tables,
    dublin_postcode_boundaries,
    postal_district_table_index,
    county_table_index,
):
    dublin_postal_districts = clean_dublin_postal_districts(
        raw_gas_tables[postal_district_table_index]
    )
    dublin_county = get_county_dublin(raw_gas_tables[county_table_index])
    postcodes = pd.concat([dublin_postal_districts, dublin_county])

    return dublin_postcode_boundaries.merge(postcodes)


def link_counties_to_postcode_boundaries(
    raw_gas_tables,
    dublin_postcode_boundaries,
    county_table_index,
):
    counties = clean_dublin_counties(raw_gas_tables[county_table_index])
    return dublin_postcode_boundaries.merge(counties, how="right")