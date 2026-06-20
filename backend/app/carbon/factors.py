"""Emission factors used by the carbon engine.

All values are kg CO2e and are India-oriented approximations gathered from public
datasets (IPCC AR6, India CEA grid factor, Our World in Data food footprints).
Centralised here so the numbers are auditable and easy to swap for an authoritative
dataset without touching business logic.

NOTE: illustrative defaults for a demo. Replace with a cited dataset before making
any real-world claim.
"""

from __future__ import annotations

from typing import Final

from app.models import Diet, TransportMode

WEEKS_PER_YEAR: Final[float] = 52.0
MONTHS_PER_YEAR: Final[float] = 12.0

# Transport: kg CO2e per passenger-km.
TRANSPORT_FACTORS: Final[dict[TransportMode, float]] = {
    "car_petrol": 0.170,
    "car_diesel": 0.160,
    "car_ev": 0.060,
    "bus": 0.050,
    "rail": 0.035,
    "motorbike": 0.090,
}

FLIGHT_FACTOR_PER_HOUR: Final[float] = 90.0

# Diet: annual kg CO2e for the food component of a typical diet.
DIET_FACTORS: Final[dict[Diet, float]] = {
    "meat_heavy": 2500.0,
    "meat_medium": 1900.0,
    "pescatarian": 1500.0,
    "vegetarian": 1200.0,
    "vegan": 1000.0,
}

GRID_FACTOR_PER_KWH: Final[float] = 0.710
LPG_FACTOR_PER_CYLINDER: Final[float] = 42.0
CONSUMPTION_FACTOR_PER_1000_INR: Final[float] = 22.0

GLOBAL_AVERAGE_KG: Final[float] = 4700.0
INDIA_AVERAGE_KG: Final[float] = 1900.0
PARIS_ALIGNED_TARGET_KG: Final[float] = 2000.0
