# Windfarm-Suitability-Philippines

"""
Wind Turbine Suitability Analysis
----------------------------------
This script identifies suitable areas for wind turbine placement using
a moving window (neighborhood) analysis on multiple raster datasets.

The workflow:
1. Load wind speed raster as the reference grid.
2. Reproject all other rasters to match the wind raster.
3. Clean and preprocess data (handle nodata and invalid values).
4. Apply a moving window filter to calculate neighborhood statistics.
5. Apply suitability criteria.
6. Save suitability outputs.
7. Compute distances from suitable sites to nearest transmission stations.
"""
