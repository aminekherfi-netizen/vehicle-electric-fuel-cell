"""Small, dependency-free fuel-cell vehicle energy model."""

from dataclasses import dataclass


@dataclass
class VehicleState:
    hydrogen_kg: float = 5.0
    battery_kwh: float = 18.0


@dataclass(frozen=True)
class FuelCellSystem:
    max_power_kw: float = 80.0
    efficiency: float = 0.55
    hydrogen_lhv_kwh_per_kg: float = 33.3
    drivetrain_efficiency: float = 0.90

    def hydrogen_consumption(self, electrical_energy_kwh: float) -> float:
        """Return hydrogen mass needed for electrical energy from the stack."""
        if electrical_energy_kwh < 0:
            raise ValueError("Electrical energy cannot be negative")
        if not 0 < self.efficiency <= 1:
            raise ValueError("Efficiency must be between 0 and 1")
        return electrical_energy_kwh / (self.efficiency * self.hydrogen_lhv_kwh_per_kg)

    def deliver(self, requested_power_kw: float, duration_hours: float, state: VehicleState) -> float:
        """Deliver traction energy and update hydrogen and battery state.

        The battery supplies demand above the stack limit. This intentionally
        simple model is a baseline, not a real-time vehicle controller.
        """
        if requested_power_kw < 0 or duration_hours < 0:
            raise ValueError("Power and duration must be non-negative")
        stack_power = min(requested_power_kw, self.max_power_kw)
        stack_energy = stack_power * duration_hours
        hydrogen = self.hydrogen_consumption(stack_energy)
        if hydrogen > state.hydrogen_kg:
            raise RuntimeError("Insufficient hydrogen")
        state.hydrogen_kg -= hydrogen

        battery_power = max(0.0, requested_power_kw - stack_power)
        battery_energy = battery_power * duration_hours / self.drivetrain_efficiency
        if battery_energy > state.battery_kwh:
            raise RuntimeError("Insufficient battery energy")
        state.battery_kwh -= battery_energy
        return requested_power_kw * duration_hours


if __name__ == "__main__":
    system = FuelCellSystem()
    state = VehicleState()
    energy = system.deliver(60.0, 0.5, state)
    print(f"Delivered: {energy:.1f} kWh")
    print(f"Hydrogen remaining: {state.hydrogen_kg:.3f} kg")
    print(f"Battery remaining: {state.battery_kwh:.1f} kWh")
