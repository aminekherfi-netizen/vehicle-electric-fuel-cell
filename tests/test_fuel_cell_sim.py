import pytest

from src.fuel_cell_sim import FuelCellSystem, VehicleState


def test_hydrogen_consumption():
    system = FuelCellSystem()
    assert system.hydrogen_consumption(18.315) == pytest.approx(1.0)


def test_delivery_updates_state():
    system = FuelCellSystem()
    state = VehicleState()
    delivered = system.deliver(60.0, 0.5, state)
    assert delivered == pytest.approx(30.0)
    assert state.hydrogen_kg < 5.0
    assert state.battery_kwh == pytest.approx(18.0)


def test_peak_power_uses_battery():
    system = FuelCellSystem()
    state = VehicleState()
    system.deliver(100.0, 1.0, state)
    assert state.battery_kwh < 18.0


def test_negative_power_is_rejected():
    with pytest.raises(ValueError):
        FuelCellSystem().deliver(-1.0, 1.0, VehicleState())
