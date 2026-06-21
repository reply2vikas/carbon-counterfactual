# Carbon Methodology & Emission-Factor Provenance

This project does not invent numbers. Every emission factor in
`backend/app/carbon/factors.py` is centralised, auditable, and aligned to a published
authority. Values are India-oriented where a national figure exists.

## Sources

| Domain | Authority |
| --- | --- |
| Electricity grid intensity (India) | Central Electricity Authority (CEA), *CO₂ Baseline Database for the Indian Power Sector* — national grid factor ≈ 0.71 kg CO₂e/kWh |
| Transport & flight factors | UK DEFRA / BEIS *Greenhouse gas reporting: conversion factors* (per passenger-km, economy short/medium-haul incl. radiative forcing) |
| Diet footprints | Our World in Data / Poore & Nemecek (2018), *Science* — annualised dietary CO₂e by pattern |
| LPG combustion | IPCC 2006 Guidelines, Vol. 2 (stationary combustion), 14.2 kg domestic cylinder |
| Global warming potential | IPCC AR6 GWP-100 |

## Scope boundaries

- **Scope 2 (indirect):** home electricity, computed from CEA grid intensity.
- **Scope 1 (direct):** LPG cooking combustion.
- **Scope 3 (value chain):** transport (passenger-km, well-to-wheel), diet, and
  discretionary consumption.

These are clearly separated in the calculator so a footprint is never a black box.

## Limitations (stated honestly)

- Grid intensity uses the national average; regional state grids vary (thermal-heavy
  West vs. hydro in the North-East). A regional refinement is future work.
- Consumption uses a spend-based (INR → CO₂e) proxy, which is coarser than
  product-level life-cycle data.
- Factors are reviewed annually against the sources above.
