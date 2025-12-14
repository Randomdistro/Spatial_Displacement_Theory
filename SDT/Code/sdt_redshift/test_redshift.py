import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdt_redshift import RedshiftCalculator  # noqa: E402


def test_sigma_matches_baseline():
    calc = RedshiftCalculator(H0=70.0, params=None)
    expected = 70.0 / 299_792.458
    assert math.isclose(calc.sigma(0.0), expected, rel_tol=1e-9)


def test_luminosity_distance_monotonic():
    calc = RedshiftCalculator()
    z = np.array([0.1, 0.5, 1.0])
    distances = calc.luminosity_distance(z)
    assert np.all(np.diff(distances) > 0)


def test_distance_relation():
    calc = RedshiftCalculator()
    z = 0.5
    d_l = calc.luminosity_distance(z)
    d_a = calc.angular_diameter_distance(z)
    assert math.isclose(d_l / d_a, (1.0 + z) ** 2, rel_tol=1e-6)


def test_lookback_time_zero():
    calc = RedshiftCalculator()
    assert calc.lookback_time(0.0) == 0.0


def _run_all():
    test_sigma_matches_baseline()
    test_luminosity_distance_monotonic()
    test_distance_relation()
    test_lookback_time_zero()
    print("All SDT redshift tests passed.")


if __name__ == "__main__":
    _run_all()

