"""Tests for hydrogen bus simulator."""

import pytest

from src.hydrogen_bus_sim import (
    HydrogenBus,
    BusRoute,
    PassengerLoad,
    FuelCellSystem,
    BusState,
)


def test_passenger_load_total_mass():
    """Test passenger load mass calculation."""
    load = PassengerLoad(passengers=30, luggage_kg=300)
    expected = 30 * 75 + 300
    assert load.total_load_kg() == expected


def test_passenger_load_energy_multiplier():
    """Test that load increases energy multiplier."""
    empty_load = PassengerLoad(passengers=0, luggage_kg=0)
    full_load = PassengerLoad(passengers=50, luggage_kg=500)
    
    assert empty_load.energy_multiplier() == pytest.approx(1.0)
    assert full_load.energy_multiplier() > 1.0


def test_bus_route_duration():
    """Test route duration calculation."""
    route = BusRoute(distance_km=20.0, avg_speed_kmh=20.0)
    assert route.duration_hours() == pytest.approx(1.0)


def test_bus_route_dwell_time():
    """Test stop dwell time calculation (30 sec per stop)."""
    route = BusRoute(stops=12)
    # 12 stops * 30 seconds = 360 seconds = 0.1 hours
    assert route.stop_dwell_time_hours() == pytest.approx(0.1, abs=0.01)


def test_hydrogen_bus_calculate_route_energy():
    """Test energy calculation for a route."""
    bus = HydrogenBus()
    route = BusRoute(distance_km=10.0, stops=6, elevation_gain_m=0)
    load = PassengerLoad(passengers=30, luggage_kg=300)
    
    energy = bus.calculate_route_energy(route, load)
    assert energy > 0
    assert energy < 100  # Should be reasonable for 10 km


def test_hydrogen_bus_run_route():
    """Test running a complete route."""
    bus = HydrogenBus(
        state=BusState(hydrogen_kg=35.0, battery_kwh=150.0)
    )
    route = BusRoute(distance_km=10.0, stops=6)
    load = PassengerLoad(passengers=30)
    
    energy = bus.run_route(route, load)
    assert bus.state.total_distance_km == pytest.approx(10.0)
    assert bus.state.hydrogen_kg < 35.0
    assert bus.state.passengers == 30


def test_hydrogen_bus_insufficient_hydrogen():
    """Test error when hydrogen is insufficient."""
    bus = HydrogenBus(
        state=BusState(hydrogen_kg=0.5, battery_kwh=150.0)
    )
    route = BusRoute(distance_km=100.0)
    load = PassengerLoad(passengers=30)
    
    with pytest.raises(RuntimeError, match="Insufficient hydrogen"):
        bus.run_route(route, load)


def test_hydrogen_bus_fuel_economy():
    """Test fuel economy calculation."""
    bus = HydrogenBus()
    route = BusRoute(distance_km=20.0)
    load = PassengerLoad(passengers=30)
    
    bus.run_route(route, load)
    fuel_economy = bus.fuel_economy()
    
    assert fuel_economy > 0
    # Typical bus should get ~4-5 km/kg
    assert 3.0 < fuel_economy < 8.0


def test_hydrogen_bus_remaining_range():
    """Test remaining range calculation."""
    bus = HydrogenBus(
        state=BusState(hydrogen_kg=35.0, battery_kwh=150.0)
    )
    
    # Simulate one route to establish fuel economy
    route = BusRoute(distance_km=20.0)
    load = PassengerLoad(passengers=30)
    bus.run_route(route, load)
    
    range_km = bus.remaining_range_km()
    assert range_km > 0
    # After 20 km with 35 kg tank, should have range > 100 km
    assert range_km > 100


def test_hydrogen_bus_status():
    """Test status string generation."""
    bus = HydrogenBus(
        state=BusState(hydrogen_kg=30.0, battery_kwh=140.0, passengers=45)
    )
    status = bus.status()
    
    assert "Hydrogen" in status
    assert "Battery" in status
    assert "Range" in status
    assert "30.00 kg" in status
    assert "45" in status


def test_fuel_cell_hydrogen_consumption():
    """Test hydrogen consumption calculation."""
    fc = FuelCellSystem()
    # 200 kW for 1 hour = 200 kWh
    # At 55% efficiency: 200 / (0.55 * 33.3) ≈ 10.95 kg
    hydrogen = fc.hydrogen_consumption(200.0)
    assert hydrogen == pytest.approx(10.95, rel=0.01)


def test_regenerative_braking_effect():
    """Test that regenerative braking reduces energy consumption."""
    bus1 = HydrogenBus()
    bus2 = HydrogenBus()
    
    route = BusRoute(distance_km=15.0, stops=8)
    load = PassengerLoad(passengers=30)
    
    energy_with_regen = bus1.calculate_route_energy(route, load, regenerative_braking_factor=0.7)
    energy_no_regen = bus2.calculate_route_energy(route, load, regenerative_braking_factor=0.0)
    
    assert energy_with_regen < energy_no_regen


def test_elevation_gain_increases_energy():
    """Test that elevation gain increases energy consumption."""
    bus1 = HydrogenBus()
    bus2 = HydrogenBus()
    
    flat_route = BusRoute(distance_km=15.0, elevation_gain_m=0)
    hilly_route = BusRoute(distance_km=15.0, elevation_gain_m=200)
    load = PassengerLoad(passengers=30)
    
    flat_energy = bus1.calculate_route_energy(flat_route, load)
    hilly_energy = bus2.calculate_route_energy(hilly_route, load)
    
    assert hilly_energy > flat_energy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
