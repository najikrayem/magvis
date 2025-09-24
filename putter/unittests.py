import pytest
from decimal import Decimal

from equations import (
    circle_area,
    awg_to_d_mm,
    awg_to_area,
    coplanar_teslas,
    coil_inductance,
    wire_resistance,
    coil_reactance,
    time_constant,
    joule_loss,
    heat_dissipation
)

def test_circle_area():
    assert circle_area(1) == Decimal('3.14159265358979323846264338327950')
    assert circle_area(0) == Decimal('0')
    assert circle_area(2) == Decimal('12.56637061435917295385057353311800')

def test_awg_to_d_mm():
    assert awg_to_d_mm(22) == pytest.approx(Decimal('0.6438'), rel=1e-4)
    assert awg_to_d_mm(0) == pytest.approx(Decimal('8.251'), rel=1e-4)
    assert awg_to_d_mm(36) == pytest.approx(Decimal('0.127'), rel=1e-4)

def test_awg_to_area():
    assert awg_to_area(22) == pytest.approx(Decimal('3.257e-7'), rel=1e-4)
    assert awg_to_area(0) == pytest.approx(Decimal('5.067e-6'), rel=1e-4)
    assert awg_to_area(36) == pytest.approx(Decimal('1.267e-8'), rel=1e-4)

def test_coplanar_teslas():
    assert coplanar_teslas(10, 5, 0.23, 2) == pytest.approx(Decimal('1.2566370614359172953850573533118e-6'), rel=1e-4)

def test_coil_inductance():
    assert coil_inductance(10, 0.23, 0.03) == pytest.approx(Decimal('1.2566370614359172953850573533118e-6'), rel=1e-4)

def test_wire_resistance():
    assert wire_resistance(1.68e-8, 22, 10) == pytest.approx(Decimal('0.0516'), rel=1e-4)

def test_coil_reactance():
    assert coil_reactance(50, 1e-3) == pytest.approx(Decimal('0.31415926535897932384626433832795'), rel=1e-4)

def test_time_constant():
    assert time_constant(10, 1e-3) == pytest.approx(Decimal('0.0001'), rel=1e-4)

def test_joule_loss():
    assert joule_loss(2, 10) == pytest.approx(Decimal('40'), rel=1e-4)

def test_heat_dissipation():
    assert heat_dissipation(100, 30, 0.1) == pytest.approx(Decimal('33.333333333333333333333333333333'), rel=1e-4)