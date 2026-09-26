"""Hydrogen fuel-cell bus energy simulator with passenger load modeling."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BusState:
    """Current state of the bus energy system."""
    hydrogen_kg: float = 35.0
    battery_kwh: float = 150.0
    total_distance_km: float = 0.0
    cumulative_energy_kwh: float = 0.0
    passengers: int = 0
    

@dataclass(frozen=True)
class FuelCellSystem:
    """Hydrogen fuel-cell system parameters."""
    max_power_kw: float = 200.0  # 200 kW for city bus
    efficiency: float = 0.55      # 55% electrical efficiency
    hydrogen_lhv_kwh_per_kg: float = 33.3  # Lower heating value
    drivetrain_efficiency: float = 0.90
    
    def hydrogen_consumption(self, electrical_energy_kwh: float) -> float:
        """Calculate hydrogen mass needed for electrical energy."""
        if electrical_energy_kwh < 0:
            raise ValueError("Electrical energy cannot be negative")
        if not 0 < self.efficiency <= 1:
            raise ValueError("Efficiency must be between 0 and 1")
        return electrical_energy_kwh / (self.efficiency * self.hydrogen_lhv_kwh_per_kg)
    
    def deliver(self, requested_power_kw: float, duration_hours: float, state: BusState) -> float:
        """Deliver traction energy and update hydrogen and battery state."""
        if requested_power_kw < 0 or duration_hours < 0:
            raise ValueError("Power and duration must be non-negative")
        
        stack_power = min(requested_power_kw, self.max_power_kw)
        stack_energy = stack_power * duration_hours
        hydrogen = self.hydrogen_consumption(stack_energy)
        
        if hydrogen > state.hydrogen_kg:
            raise RuntimeError(f"Insufficient hydrogen: need {hydrogen:.3f} kg, have {state.hydrogen_kg:.3f} kg")
        
        state.hydrogen_kg -= hydrogen
        
        # Battery supplies power above stack limit
        battery_power = max(0.0, requested_power_kw - stack_power)
        battery_energy = battery_power * duration_hours / self.drivetrain_efficiency
        
        if battery_energy > state.battery_kwh:
            raise RuntimeError(f"Insufficient battery energy: need {battery_energy:.1f} kWh, have {state.battery_kwh:.1f} kWh")
        
        state.battery_kwh -= battery_energy
        total_energy = stack_energy + battery_energy
        state.cumulative_energy_kwh += total_energy
        
        return total_energy


@dataclass
class PassengerLoad:
    """Model passenger load and its effect on bus weight and energy."""
    passengers: int = 30
    luggage_kg: float = 300.0
    avg_passenger_weight_kg: float = 75.0
    
    def total_load_kg(self) -> float:
        """Total payload mass (passengers + luggage)."""
        return self.passengers * self.avg_passenger_weight_kg + self.luggage_kg
    
    def energy_multiplier(self) -> float:
        """Energy multiplier due to added load."""
        curb_weight_kg = 12000
        loaded_weight = curb_weight_kg + self.total_load_kg()
        return loaded_weight / curb_weight_kg


@dataclass
class BusRoute:
    """Define a bus route for simulation."""
    name: str = "Downtown Loop"
    distance_km: float = 20.0
    stops: int = 12
    elevation_gain_m: float = 150
    avg_speed_kmh: float = 20.0  # Typical city bus speed
    
    def duration_hours(self) -> float:
        """Estimated route duration."""
        return self.distance_km / self.avg_speed_kmh
    
    def stop_dwell_time_hours(self) -> float:
        """Total time spent at stops (assume 30 seconds per stop)."""
        return self.stops * 0.5 / 3600.0


@dataclass
class HydrogenBus:
    """Complete hydrogen fuel-cell bus model."""
    state: BusState = field(default_factory=BusState)
    fuel_cell: FuelCellSystem = field(default_factory=FuelCellSystem)
    hydrogen_consumed_kg: float = 0.0
    
    def calculate_route_energy(
        self,
        route: BusRoute,
        load: PassengerLoad,
        regenerative_braking_factor: float = 0.7
    ) -> float:
        """
        Calculate energy needed for a complete route.
        
        Args:
            route: Bus route definition
            load: Passenger and luggage load
            regenerative_braking_factor: Fraction of braking energy recovered (0-1)
        
        Returns:
            Net energy consumed (kWh)
        """
        # Base energy for driving
        base_power_kw = 80  # Base traction power for acceleration, grade, rolling resistance
        driving_energy = base_power_kw * route.duration_hours()
        
        # Load factor increases energy consumption
        load_factor = load.energy_multiplier()
        loaded_energy = driving_energy * load_factor
        
        # Grade climbing energy (rough estimate: ~0.4 kWh per 100m elevation)
        grade_energy = route.elevation_gain_m * 0.004
        
        # Total energy before regeneration
        total_energy_gross = loaded_energy + grade_energy
        
        # Regenerative braking at stops
        braking_energy = base_power_kw * route.stop_dwell_time_hours() * 0.5
        regenerated_energy = braking_energy * regenerative_braking_factor
        
        # Net energy consumed
        net_energy = total_energy_gross - regenerated_energy
        
        return max(0.0, net_energy)
    
    def run_route(
        self,
        route: BusRoute,
        load: PassengerLoad,
        regenerative_braking_factor: float = 0.7
    ) -> float:
        """
        Simulate a complete bus route.
        
        Returns:
            Energy consumed (kWh)
        """
        energy_needed = self.calculate_route_energy(route, load, regenerative_braking_factor)
        avg_power = energy_needed / route.duration_hours() if route.duration_hours() > 0 else 0
        
        # Deliver the energy
        self.fuel_cell.deliver(avg_power, route.duration_hours(), self.state)
        self.state.total_distance_km += route.distance_km
        self.state.passengers = load.passengers
        
        self.hydrogen_consumed_kg += (self.fuel_cell.hydrogen_consumption(energy_needed))
        
        return energy_needed
    
    def fuel_economy(self) -> float:
        """Return fuel economy in km per kg of hydrogen."""
        if self.hydrogen_consumed_kg == 0:
            return 0.0
        return self.state.total_distance_km / self.hydrogen_consumed_kg
    
    def remaining_range_km(self) -> float:
        """Estimate remaining range with current hydrogen and battery."""
        if self.fuel_economy() == 0:
            return 0.0
        # Assume ~4 km per kWh battery efficiency
        battery_range = self.state.battery_kwh * 4.0
        hydrogen_range = self.state.hydrogen_kg * self.fuel_economy()
        return min(hydrogen_range, battery_range)
    
    def status(self) -> str:
        """Return current bus status as string."""
        return (
            f"Hydrogen: {self.state.hydrogen_kg:.2f} kg | "
            f"Battery: {self.state.battery_kwh:.1f} kWh | "
            f"Range: {self.remaining_range_km():.1f} km | "
            f"Distance traveled: {self.state.total_distance_km:.1f} km | "
            f"Passengers: {self.state.passengers}"
        )


if __name__ == "__main__":
    # Example: Simulate a typical city bus day
    bus = HydrogenBus()
    
    # Morning route - peak hours, full bus
    morning_route = BusRoute(name="Morning Peak", distance_km=25.0, stops=14, elevation_gain_m=100)
    morning_load = PassengerLoad(passengers=45, luggage_kg=500)
    morning_energy = bus.run_route(morning_route, morning_load)
    print(f"Morning: {morning_energy:.1f} kWh consumed")
    print(bus.status())
    print()
    
    # Midday route - lighter load
    midday_route = BusRoute(name="Midday Service", distance_km=20.0, stops=12, elevation_gain_m=80)
    midday_load = PassengerLoad(passengers=25, luggage_kg=250)
    midday_energy = bus.run_route(midday_route, midday_load)
    print(f"Midday: {midday_energy:.1f} kWh consumed")
    print(bus.status())
    print()
    
    # Evening route - evening peak
    evening_route = BusRoute(name="Evening Peak", distance_km=25.0, stops=14, elevation_gain_m=100)
    evening_load = PassengerLoad(passengers=40, luggage_kg=450)
    evening_energy = bus.run_route(evening_route, evening_load)
    print(f"Evening: {evening_energy:.1f} kWh consumed")
    print(bus.status())
    print()
    
    print(f"=== Daily Summary ===")
    print(f"Total distance: {bus.state.total_distance_km:.1f} km")
    print(f"Total energy: {bus.state.cumulative_energy_kwh:.1f} kWh")
    print(f"Fuel economy: {bus.fuel_economy():.2f} km/kg")
    print(f"Remaining range: {bus.remaining_range_km():.1f} km")
