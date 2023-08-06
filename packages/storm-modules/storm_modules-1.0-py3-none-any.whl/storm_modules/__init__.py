"""Storm modules"""
from pathlib import Path

__version__ = "1.0"
PROJECT_NAME = "storm-modules"
PROJECT_DIR = Path(__file__).parents[0]
REPO_DIR = PROJECT_DIR.parents[0]

MODULE_LIST = [
    "availability",
    "co2",
    "demand",
    "exo_prod",
    "french_nuke",
    "fuel_price",
    "fx",
    "german_coal",
    "hydro_calibration",
    "interco",
    "past_wind",
    "row_prices",
    "solar_and_wind",
]
