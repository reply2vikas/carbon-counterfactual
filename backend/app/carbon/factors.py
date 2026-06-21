"""Emission factors used by the carbon engine.

Every value is centralised here so the numbers are auditable in one place and easy to
swap for an updated dataset without touching business logic. Each factor is aligned to
a published authority; see CARBON_METHODOLOGY.md in the repo root for full provenance,
scope boundaries, and limitations.

Primary sources:
  - India grid intensity: Central Electricity Authority (CEA) CO2 Baseline Database.
  - Transport / flight: UK DEFRA/BEIS GHG conversion factors (per passenger-km).
  - Diet: Our World in Data / Poore & Nemecek (2018), Science.
  - LPG combustion: IPCC 2006 Guidelines, Vol. 2.
  - GWP basis: IPCC AR6 GWP-100.
"""

from __future__ import annotations

from typing import Final

from app.models import Diet, TransportMode

WEEKS_PER_YEAR: Final[float] = 52.0
MONTHS_PER_YEAR: Final[float] = 12.0

# Transport: kg CO2e per passenger-km. Source: DEFRA/BEIS conversion factors.
TRANSPORT_FACTORS: Final[dict[TransportMode, float]] = {
    "car_petrol": 0.170,  # average petrol car, per-km
    "car_diesel": 0.160,  # average diesel car, per-km
    "car_ev": 0.060,  # EV charged on the Indian grid (CEA intensity applied)
    "bus": 0.050,  # local diesel bus, per passenger-km
    "rail": 0.035,  # electric rail, per passenger-km
    "motorbike": 0.090,  # average two-wheeler, per-km
}

# Flight: kg CO2e per hour, short/medium-haul economy incl. radiative forcing (DEFRA).
FLIGHT_FACTOR_PER_HOUR: Final[float] = 90.0

# Diet: annual kg CO2e for the food component (Our World in Data / Poore & Nemecek).
DIET_FACTORS: Final[dict[Diet, float]] = {
    "meat_heavy": 2500.0,
    "meat_medium": 1900.0,
    "pescatarian": 1500.0,
    "vegetarian": 1200.0,
    "vegan": 1000.0,
}

# Home energy.
GRID_FACTOR_PER_KWH: Final[float] = 0.710  # CEA India national average, kg CO2e/kWh.
LPG_FACTOR_PER_CYLINDER: Final[float] = 42.0  # 14.2 kg domestic cylinder (IPCC 2006).

# Consumption / shopping: kg CO2e per INR 1000 spent (spend-based proxy).
CONSUMPTION_FACTOR_PER_1000_INR: Final[float] = 22.0

# +/-band applied to ACHIEVED SAVINGS (not the whole footprint) to reflect behavioural
# adherence and factor variance; see app/actions/simulator.py.
ADHERENCE_BAND: Final[float] = 0.10

# Reference points, kg CO2e per person per year.
GLOBAL_AVERAGE_KG: Final[float] = 4700.0  # global mean per-capita (OWID).
INDIA_AVERAGE_KG: Final[float] = 1900.0  # India mean per-capita (OWID).
PARIS_ALIGNED_TARGET_KG: Final[float] = 2000.0  # ~1.5C-aligned 2030 per-capita target.


# ---------------------------------------------------------------------------
# Provenance for every factor above. Values are kept in code (not a database)
# deliberately: real-time calculation loops need O(1) lookups, and committing
# the coefficients makes them auditable in version control.
#
# Each entry: factor -> (authority, year, scope, methodology).
# ---------------------------------------------------------------------------
SOURCES: Final[dict[str, dict[str, str]]] = {
    "grid_electricity": {
        "value_ref": "GRID_FACTOR_PER_KWH = 0.710 kgCO2e/kWh",
        "authority": "Central Electricity Authority (CEA), India - CO2 Baseline Database",
        "year": "2024",
        "scope": "Scope 2 (indirect, purchased electricity)",
        "methodology": "IPCC 2006/2019 GWP-100",
    },
    "transport": {
        "value_ref": "TRANSPORT_FACTORS (kgCO2e per passenger-km)",
        "authority": "UK DEFRA GHG Conversion Factors; IPCC AR6",
        "year": "2024",
        "scope": "Scope 1 (direct combustion) / Scope 2 for EV charging",
        "methodology": "Well-to-wheel where available, tank-to-wheel otherwise",
    },
    "flight": {
        "value_ref": "FLIGHT_FACTOR_PER_HOUR = 90 kgCO2e/hr",
        "authority": "UK DEFRA (short/medium-haul economy, incl. radiative forcing)",
        "year": "2024",
        "scope": "Scope 3 (category 6, business/personal travel)",
        "methodology": "Distance-based, RFI-adjusted",
    },
    "diet": {
        "value_ref": "DIET_FACTORS (annual kgCO2e for the food component)",
        "authority": "Our World in Data / Poore & Nemecek (2018), Science",
        "year": "2018-2023",
        "scope": "Scope 3 (cradle-to-retail food lifecycle)",
        "methodology": "Life-cycle assessment, global meta-analysis",
    },
    "lpg": {
        "value_ref": "LPG_FACTOR_PER_CYLINDER = 42 kgCO2e per 14.2 kg cylinder",
        "authority": "IPCC 2006 Guidelines, Vol. 2 (Energy), stationary combustion",
        "year": "2006/2019 refinement",
        "scope": "Scope 1 (direct combustion)",
        "methodology": "Fuel-mass x net calorific value x emission factor",
    },
    "consumption": {
        "value_ref": "CONSUMPTION_FACTOR_PER_1000_INR = 22 kgCO2e per INR 1000",
        "authority": "Environmentally-Extended Input-Output (EEIO) approximation, India",
        "year": "2023",
        "scope": "Scope 3 (purchased goods & services)",
        "methodology": "Spend-based EEIO estimate (illustrative; replace for production)",
    },
}
