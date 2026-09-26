from src.energy_simulation import BusParameters, Segment, simulate_route


def test_route_result_is_positive():
    result = simulate_route([Segment(10.0, 25.0, 1.0, 8)], passengers=40)
    assert result.distance_km == 10.0
    assert result.total_energy_kwh > 0
    assert result.hydrogen_kg > 0
    assert result.fuel_economy_km_per_kg > 0


def test_more_passengers_require_more_energy():
    route = [Segment(20.0, 25.0, 0.0, 10)]
    light = simulate_route(route, passengers=10)
    heavy = simulate_route(route, passengers=50)
    assert heavy.total_energy_kwh > light.total_energy_kwh


def test_custom_efficiency_changes_hydrogen_use():
    route = [Segment(20.0, 25.0)]
    efficient = simulate_route(route, 30, BusParameters(fuel_cell_efficiency=0.60))
    baseline = simulate_route(route, 30, BusParameters(fuel_cell_efficiency=0.55))
    assert efficient.hydrogen_kg < baseline.hydrogen_kg
