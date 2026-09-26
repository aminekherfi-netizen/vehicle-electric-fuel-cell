"""Web dashboard for hydrogen bus fleet monitoring and simulation."""

import json
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict

from src.energy_simulation import Segment, simulate_route, BusParameters
from src.infrastructure_planning import HydrogenRefuelingStation, BusDepotDesign


@dataclass
class FleetStatus:
    """Real-time fleet status snapshot."""
    timestamp: str
    total_buses: int
    buses_in_service: int
    buses_charging: int
    buses_refueling: int
    buses_in_maintenance: int
    total_hydrogen_on_hand_kg: float
    total_battery_soc_percent: float
    next_refuel_time: str
    average_fuel_economy_km_per_kg: float
    daily_hydrogen_consumption_kg: float
    alerts: List[str]


@dataclass
class RouteMetrics:
    """Performance metrics for a single route."""
    route_name: str
    distance_km: float
    estimated_energy_kwh: float
    estimated_hydrogen_kg: float
    estimated_duration_minutes: int
    fuel_economy_km_per_kg: float
    thermal_risk: str  # LOW, MEDIUM, HIGH
    safety_margin_percent: float  # Remaining range vs. distance


class DashboardDataGenerator:
    """Generate dashboard data for web frontend."""
    
    def __init__(self, fleet_size: int = 10, depot: BusDepotDesign | None = None):
        self.fleet_size = fleet_size
        self.depot = depot or BusDepotDesign(num_buses=fleet_size)
        self.bus_params = BusParameters()
    
    def fleet_status(self, in_service: int = 8, charging: int = 1, refueling: int = 1) -> FleetStatus:
        """Generate current fleet status."""
        hydrogen_capacity = 35.0
        avg_hydrogen = hydrogen_capacity * 0.6  # Assume 60% full on average
        total_hydrogen = avg_hydrogen * self.fleet_size
        
        total_battery = 150.0  # kWh per bus
        avg_soc = 0.75
        total_battery_kwh = total_battery * avg_soc * self.fleet_size
        total_battery_percent = 75
        
        daily_consumption = 6.5 * self.fleet_size  # kg per bus
        
        alerts = []
        if total_hydrogen < daily_consumption * 1.2:
            alerts.append("⚠️ Hydrogen reserve below 20% daily consumption")
        if in_service < self.fleet_size * 0.7:
            alerts.append("⚠️ More than 30% of fleet not in service")
        
        return FleetStatus(
            timestamp=datetime.now().isoformat(),
            total_buses=self.fleet_size,
            buses_in_service=in_service,
            buses_charging=charging,
            buses_refueling=refueling,
            buses_in_maintenance=self.fleet_size - in_service - charging - refueling,
            total_hydrogen_on_hand_kg=total_hydrogen,
            total_battery_soc_percent=total_battery_percent,
            next_refuel_time="06:00 AM (tomorrow)",
            average_fuel_economy_km_per_kg=5.2,
            daily_hydrogen_consumption_kg=daily_consumption,
            alerts=alerts
        )
    
    def route_analysis(self, route_segments: List[Segment], passengers: int = 40) -> RouteMetrics:
        """Analyze a route and return performance metrics."""
        result = simulate_route(route_segments, passengers, self.bus_params)
        
        # Estimate thermal risk based on total energy and duration
        avg_power_kw = result.total_energy_kwh / result.duration_hours if result.duration_hours > 0 else 0
        if avg_power_kw > 80:
            thermal_risk = "HIGH"
        elif avg_power_kw > 60:
            thermal_risk = "MEDIUM"
        else:
            thermal_risk = "LOW"
        
        # Safety margin: compare range to route distance
        hydrogen_tank_kg = 35.0
        remaining_hydrogen = hydrogen_tank_kg - result.hydrogen_kg
        remaining_range_km = remaining_hydrogen * result.fuel_economy_km_per_kg
        safety_margin = (remaining_range_km / result.distance_km * 100) if result.distance_km > 0 else 0
        
        return RouteMetrics(
            route_name=f"Route {len(route_segments)}-stop",
            distance_km=result.distance_km,
            estimated_energy_kwh=result.total_energy_kwh,
            estimated_hydrogen_kg=result.hydrogen_kg,
            estimated_duration_minutes=int(result.duration_hours * 60),
            fuel_economy_km_per_kg=result.fuel_economy_km_per_kg,
            thermal_risk=thermal_risk,
            safety_margin_percent=max(0, safety_margin)
        )
    
    def comparison_scenarios(self, base_route: List[Segment]) -> Dict[str, RouteMetrics]:
        """Compare route metrics across different passenger loads."""
        scenarios = {
            "Light Load (20 passengers)": self.route_analysis(base_route, 20),
            "Medium Load (40 passengers)": self.route_analysis(base_route, 40),
            "Heavy Load (55 passengers)": self.route_analysis(base_route, 55),
        }
        return scenarios
    
    def depot_overview(self) -> Dict:
        """Generate depot infrastructure overview."""
        roi = self.depot.roi_analysis()
        space = self.depot.space_requirements_m2()
        
        return {
            "fleet_size": self.fleet_size,
            "refueling_stations": self.depot.refueling_stations,
            "chargers": self.depot.num_chargers,
            "maintenance_bays": self.depot.maintenance_bays,
            "space_requirements_m2": space,
            "capital_cost_usd": roi["capital_cost"],
            "annual_opex_usd": roi["annual_opex"],
            "payback_years": roi["payback_years"],
            "roi_10yr_percent": roi["roi_percent"],
            "daily_hydrogen_consumption_kg": 6.5 * self.fleet_size,
            "monthly_hydrogen_cost_usd": 6.5 * self.fleet_size * 9.0 * 22,  # 22 work days
        }
    
    def export_json(self, filename: str = "dashboard_data.json") -> None:
        """Export dashboard data as JSON."""
        data = {
            "fleet_status": asdict(self.fleet_status()),
            "sample_route": asdict(self.route_analysis([
                Segment(8.0, 28.0, 1.0, 5),
                Segment(6.0, 22.0, -0.5, 4),
                Segment(7.0, 25.0, 2.0, 4),
            ])),
            "depot_overview": self.depot_overview(),
            "generated_at": datetime.now().isoformat(),
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Dashboard data exported to {filename}")


if __name__ == "__main__":
    generator = DashboardDataGenerator(fleet_size=10)
    
    print("="*70)
    print("HYDROGEN BUS FLEET DASHBOARD")
    print("="*70)
    print()
    
    # Fleet status
    status = generator.fleet_status(in_service=8, charging=1, refueling=1)
    print(f"Fleet Status (as of {status.timestamp[:19]})")
    print("-" * 70)
    print(f"In service: {status.buses_in_service}/{status.total_buses}")
    print(f"Hydrogen on hand: {status.total_hydrogen_on_hand_kg:.1f} kg")
    print(f"Battery SoC: {status.total_battery_soc_percent:.0f}%")
    print(f"Daily consumption: {status.daily_hydrogen_consumption_kg:.1f} kg")
    if status.alerts:
        print(f"Alerts:")
        for alert in status.alerts:
            print(f"  {alert}")
    print()
    
    # Route analysis
    test_route = [
        Segment(8.0, 28.0, 1.0, 5),
        Segment(6.0, 22.0, -0.5, 4),
        Segment(7.0, 25.0, 2.0, 4),
    ]
    route_metrics = generator.route_analysis(test_route, passengers=40)
    print("Route Performance (Sample)")
    print("-" * 70)
    print(f"Distance: {route_metrics.distance_km:.1f} km")
    print(f"Duration: {route_metrics.estimated_duration_minutes} minutes")
    print(f"Energy: {route_metrics.estimated_energy_kwh:.1f} kWh")
    print(f"Hydrogen: {route_metrics.estimated_hydrogen_kg:.2f} kg")
    print(f"Fuel economy: {route_metrics.fuel_economy_km_per_kg:.2f} km/kg")
    print(f"Thermal risk: {route_metrics.thermal_risk}")
    print(f"Safety margin: {route_metrics.safety_margin_percent:.0f}%")
    print()
    
    # Depot overview
    depot = generator.depot_overview()
    print("Depot Infrastructure")
    print("-" * 70)
    print(f"Fleet size: {depot['fleet_size']} buses")
    print(f"Refueling stations: {depot['refueling_stations']}")
    print(f"Fast chargers: {depot['chargers']}")
    print(f"Capital cost: ${depot['capital_cost_usd']:,.0f}")
    print(f"Annual OpEx: ${depot['annual_opex_usd']:,.0f}")
    print(f"Payback period: {depot['payback_years']:.1f} years")
    print(f"10-year ROI: {depot['roi_10yr_percent']:.0f}%")
    print()
    
    # Export to JSON for web frontend
    generator.export_json()
