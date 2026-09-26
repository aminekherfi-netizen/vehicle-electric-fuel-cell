"""Route-level hydrogen bus energy simulation.

This intentionally transparent model is for planning and education. It is not a
vehicle controller, safety system, or substitute for certified test data.
"""

from dataclasses import dataclass
from math import sin, radians


@dataclass(frozen=True)
class Segment:
    distance_km: float
    average_speed_kmh: float
    grade_percent: float = 0.0
    stops: int = 0


@dataclass(frozen=True)
class BusParameters:
    curb_mass_kg: float = 12_000.0
    passenger_mass_kg: float = 75.0
    frontal_area_m2: float = 9.5
    drag_coefficient: float = 0.55
    rolling_coefficient: float = 0.015
    air_density_kg_m3: float = 1.225
    drivetrain_efficiency: float = 0.90
    auxiliary_power_kw: float = 8.0
    fuel_cell_efficiency: float = 0.55
    hydrogen_lhv_kwh_per_kg: float = 33.3
    regenerative_recovery: float = 0.65
    stop_dwell_seconds: float = 30.0


@dataclass(frozen=True)
class TripResult:
    distance_km: float
    traction_energy_kwh: float
    auxiliary_energy_kwh: float
    total_energy_kwh: float
    hydrogen_kg: float
    fuel_economy_km_per_kg: float
    duration_hours: float


def validate_inputs(parameters: BusParameters, passengers: int) -> None:
    if passengers < 0:
        raise ValueError("passengers must be non-negative")
    if parameters.drivetrain_efficiency <= 0 or parameters.fuel_cell_efficiency <= 0:
        raise ValueError("efficiencies must be positive")
    if not 0 <= parameters.regenerative_recovery <= 1:
        raise ValueError("regenerative_recovery must be between 0 and 1")


def segment_energy_kwh(segment: Segment, passengers: int, p: BusParameters) -> tuple[float, float]:
    """Return traction energy and duration for one route segment."""
    if segment.distance_km < 0 or segment.average_speed_kmh <= 0:
        raise ValueError("distance must be non-negative and speed must be positive")

    mass = p.curb_mass_kg + passengers * p.passenger_mass_kg
    speed_ms = segment.average_speed_kmh / 3.6
    duration_h = segment.distance_km / segment.average_speed_kmh

    rolling_n = p.rolling_coefficient * mass * 9.81
    drag_n = 0.5 * p.air_density_kg_m3 * p.drag_coefficient * p.frontal_area_m2 * speed_ms**2
    grade_n = mass * 9.81 * sin(radians(segment.grade_percent))
    wheel_energy_kwh = max(0.0, (rolling_n + drag_n + grade_n) * segment.distance_km * 1000 / 3_600_000)
    electrical_traction_kwh = wheel_energy_kwh / p.drivetrain_efficiency

    # A simple stop-related recovery estimate, bounded to avoid creating energy.
    stop_braking_kwh = 0.05 * segment.stops
    recovery_kwh = min(electrical_traction_kwh, stop_braking_kwh * p.regenerative_recovery)
    return max(0.0, electrical_traction_kwh - recovery_kwh), duration_h + segment.stops * p.stop_dwell_seconds / 3600


def simulate_route(segments: list[Segment], passengers: int, p: BusParameters | None = None) -> TripResult:
    """Simulate a route and return energy, hydrogen, and economy metrics."""
    p = p or BusParameters()
    validate_inputs(p, passengers)
    traction_kwh = 0.0
    duration_h = 0.0
    distance_km = 0.0

    for segment in segments:
        energy, duration = segment_energy_kwh(segment, passengers, p)
        traction_kwh += energy
        duration_h += duration
        distance_km += segment.distance_km

    auxiliary_kwh = p.auxiliary_power_kw * duration_h
    total_kwh = traction_kwh + auxiliary_kwh
    hydrogen_kg = total_kwh / (p.fuel_cell_efficiency * p.hydrogen_lhv_kwh_per_kg)
    economy = distance_km / hydrogen_kg if hydrogen_kg else 0.0
    return TripResult(distance_km, traction_kwh, auxiliary_kwh, total_kwh, hydrogen_kg, economy, duration_h)


if __name__ == "__main__":
    route = [
        Segment(8.0, 28.0, 1.0, 5),
        Segment(6.0, 22.0, -0.5, 4),
        Segment(7.0, 25.0, 2.0, 4),
    ]
    for load in (20, 45):
        result = simulate_route(route, load)
        print(f"Passengers: {load}")
        print(f"Distance: {result.distance_km:.1f} km")
        print(f"Energy: {result.total_energy_kwh:.1f} kWh")
        print(f"Hydrogen: {result.hydrogen_kg:.2f} kg")
        print(f"Fuel economy: {result.fuel_economy_km_per_kg:.2f} km/kg")
        print()
