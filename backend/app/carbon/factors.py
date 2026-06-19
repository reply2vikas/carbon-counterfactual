"""Emission factors and reduction-action catalogue.

All factors are kg CO2e and are sourced from public datasets (Our World in Data
food emissions, IEA/EPA transport and electricity intensities). Values are
deliberately conservative, India-leaning where a national figure exists, and are
kept in one place so the calculator stays a pure function of these constants.
"""

from __future__ import annotations

# --- Annual baselines and conversion factors (kg CO2e) -----------------------

# Transport: kg CO2e per km by mode.
TRANSPORT_KG_PER_KM: dict[str, float] = {
    "car_petrol": 0.192,
    "car_diesel": 0.171,
    "car_ev": 0.053,  # using India grid intensity
    "bus": 0.103,
    "metro": 0.041,
    "motorbike": 0.103,
    "walk_cycle": 0.0,
}

# Diet: kg CO2e per day by dietary pattern.
DIET_KG_PER_DAY: dict[str, float] = {
    "heavy_meat": 7.19,
    "medium_meat": 5.63,
    "low_meat": 4.67,
    "pescatarian": 3.91,
    "vegetarian": 3.81,
    "vegan": 2.89,
}

# Home energy: kg CO2e per kWh (India grid average) and per unit of LPG.
ELECTRICITY_KG_PER_KWH: float = 0.71
LPG_KG_PER_KG: float = 2.98

# Flights: kg CO2e per hour in the air (economy, incl. radiative forcing).
FLIGHT_KG_PER_HOUR: float = 90.0

# Reference points used for context, in kg CO2e per year.
GLOBAL_AVG_ANNUAL: float = 4_700.0
PARIS_ALIGNED_TARGET: float = 2_000.0

DAYS_PER_YEAR: int = 365
WEEKS_PER_YEAR: int = 52
