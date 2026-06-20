from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import CarbonInput


def test_rejects_negative_distance() -> None:
    with pytest.raises(ValidationError):
        CarbonInput(car_km_week=-1)


def test_rejects_unknown_diet() -> None:
    with pytest.raises(ValidationError):
        CarbonInput(diet="carnivore")  # type: ignore[arg-type]


def test_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        CarbonInput(unexpected=5)  # type: ignore[call-arg]
