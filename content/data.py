"""Create a datasets for workshop.

This module can be used the recreate the example datasets used in the workshop.
"""

__author__ = "Serge Rey <sjsrey@gmail.com>"

from geosnap import Community


# Census data for San Diego County Tracts 2010
sd = Community.from_census(county_fips='06073')
gdf = sd.gdf
gdf = gdf[gdf.year == 2010]
gdf = gdf.fillna(gdf.median())
gdf['median_home_value'] = gdf.median_home_value/1000
gdf['median_home_value'] = gdf.median_home_value.astype(int)
gdf.to_parquet("data/sdgdf.parquet")



