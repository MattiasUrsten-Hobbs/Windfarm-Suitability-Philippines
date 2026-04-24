"""
Mapping Script
--------------
Creates cartographic outputs from analysis results.
"""

import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.transform import array_bounds
from matplotlib_scalebar.scalebar import ScaleBar

# Inputs
suit_score_tif = "lab5_suit_score.tif"
countries_shp = "data/ne_10m_admin_0_countries.shp"

# -------------------------------------------------------------------
# Load boundary
# -------------------------------------------------------------------
world = gpd.read_file(countries_shp)
philippines = world[world["ADMIN"] == "Philippines"]

# -------------------------------------------------------------------
# Clip raster
# -------------------------------------------------------------------
with rasterio.open(suit_score_tif) as src:

    philippines = philippines.to_crs(src.crs)
    clipped, transform = mask(src, philippines.geometry, crop=True)

    data = clipped[0]

    bounds = array_bounds(
        data.shape[0],
        data.shape[1],
        transform
    )

# Define extent
extent = [bounds[0], bounds[2], bounds[1], bounds[3]]

# Clean nodata
data = np.where(data == 255, np.nan, data)

# -------------------------------------------------------------------
# Plot map
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 10))

cmap = plt.get_cmap("viridis", 6)
img = ax.imshow(data, cmap=cmap, extent=extent)

philippines.boundary.plot(ax=ax, color="black", linewidth=0.5)

# North arrow
ax.annotate(
    "",
    xy=(0.92, 0.85),
    xytext=(0.92, 0.70),
    arrowprops=dict(facecolor="black", width=5, headwidth=9),
    xycoords="axes fraction"
)

ax.text(0.92, 0.88, "N", transform=ax.transAxes,
        ha="center", va="center", fontsize=12, fontweight="bold")

# Colorbar
cbar = plt.colorbar(img, ax=ax, ticks=range(6))
cbar.set_label("Suitability Score (0–5)")

# Scale bar
scalebar = ScaleBar(dx=1, units="m", location="lower left")
ax.add_artist(scalebar)

# Labels
ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")

# Title
ax.set_title("Wind Turbine Suitability — Philippines")

plt.savefig("Results/suitability_score_map.png",
            dpi=300, bbox_inches="tight")

plt.close()

print("Map saved.")
