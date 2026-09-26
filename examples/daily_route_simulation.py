"""Example: Simulate a complete day of hydrogen bus operations."""

from src.hydrogen_bus_sim import HydrogenBus, BusRoute, PassengerLoad


def simulate_daily_operation():
    """Simulate a typical day of city bus operations."""
    
    print("=" * 70)
    print("HYDROGEN BUS DAILY OPERATION SIMULATION")
    print("=" * 70)
    print()
    
    # Create bus at start of day with full tanks
    bus = HydrogenBus(
        # hydrogen_kg=35.0 (default)
        # battery_kwh=150.0 (default)
    )
    
    routes = [
        # Early morning pre-service (empty bus to depot)
        ("Pre-service to depot", BusRoute(name="Depot run", distance_km=5.0, stops=2, elevation_gain_m=20),
         PassengerLoad(passengers=0, luggage_kg=0), "No passengers"),
        
        # Morning rush hour (6:00 AM - 9:00 AM)
        ("Morning rush - Route 42 (North)", BusRoute(name="Route 42-A", distance_km=15.0, stops=10, elevation_gain_m=80),
         PassengerLoad(passengers=48, luggage_kg=500), "Peak capacity"),
        
        ("Morning rush - Return", BusRoute(name="Route 42-B", distance_km=15.0, stops=10, elevation_gain_m=50),
         PassengerLoad(passengers=45, luggage_kg=480), "Peak capacity"),
        
        # Mid-morning service
        ("Mid-morning - Route 5 (Downtown)", BusRoute(name="Route 5", distance_km=12.0, stops=8, elevation_gain_m=40),
         PassengerLoad(passengers=32, luggage_kg=350), "Light-moderate"),
        
        # Late morning
        ("Late morning - Route 9 (Hospital)", BusRoute(name="Route 9", distance_km=8.0, stops=6, elevation_gain_m=20),
         PassengerLoad(passengers=20, luggage_kg=200), "Light"),
        
        # Afternoon service
        ("Afternoon - Route 5 (Downtown)", BusRoute(name="Route 5", distance_km=12.0, stops=8, elevation_gain_m=40),
         PassengerLoad(passengers=28, luggage_kg=300), "Moderate"),
        
        ("Afternoon - Route 42 (North)", BusRoute(name="Route 42-C", distance_km=15.0, stops=10, elevation_gain_m=80),
         PassengerLoad(passengers=35, luggage_kg=380), "Moderate-heavy"),
        
        # Evening rush hour (4:00 PM - 7:00 PM)
        ("Evening rush - Route 1 (East)", BusRoute(name="Route 1", distance_km=18.0, stops=11, elevation_gain_m=100),
         PassengerLoad(passengers=50, luggage_kg=550), "Peak capacity"),
        
        ("Evening rush - Return", BusRoute(name="Route 1-B", distance_km=18.0, stops=11, elevation_gain_m=80),
         PassengerLoad(passengers=42, luggage_kg=450), "Peak capacity"),
        
        # Late evening
        ("Late evening - Route 9 (Hospital)", BusRoute(name="Route 9", distance_km=8.0, stops=6, elevation_gain_m=20),
         PassengerLoad(passengers=18, luggage_kg=180), "Light"),
        
        # End of day return to depot
        ("Return to depot", BusRoute(name="Depot return", distance_km=5.0, stops=2, elevation_gain_m=20),
         PassengerLoad(passengers=5, luggage_kg=50), "Almost empty"),
    ]
    
    print("ROUTE SCHEDULE:")
    print("-" * 70)
    
    for i, (description, route, load, note) in enumerate(routes, 1):
        # Skip idle and zero-distance routes
        if route.distance_km == 0:
            print(f"{i:2d}. {description:<35} | {note}")
            continue
        
        try:
            energy = bus.run_route(route, load, regenerative_braking_factor=0.7)
            fuel_eco = bus.fuel_economy()
            
            print(f"{i:2d}. {description:<35} | {route.distance_km:5.1f} km | {energy:6.1f} kWh | {fuel_eco:4.2f} km/kg | {note}")
        except RuntimeError as e:
            print(f"{i:2d}. {description:<35} | ERROR: {e}")
            break
    
    print()
    print("=" * 70)
    print("DAILY SUMMARY")
    print("=" * 70)
    print(bus.status())
    print()
    print(f"Total distance traveled:        {bus.state.total_distance_km:8.1f} km")
    print(f"Total energy consumed:          {bus.state.cumulative_energy_kwh:8.1f} kWh")
    print(f"Hydrogen consumed:              {bus.hydrogen_consumed_kg:8.3f} kg")
    print(f"Fuel economy (average):         {bus.fuel_economy():8.2f} km/kg")
    print(f"Energy intensity (avg):         {bus.state.cumulative_energy_kwh / bus.state.total_distance_km:8.2f} kWh/km")
    print()
    print(f"Remaining hydrogen:             {bus.state.hydrogen_kg:8.2f} kg")
    print(f"Remaining battery:              {bus.state.battery_kwh:8.1f} kWh")
    print(f"Estimated range remaining:      {bus.remaining_range_km():8.1f} km")
    print()
    print("STATUS: {}".format("READY FOR NEXT DAY" if bus.remaining_range_km() > 100 else "NEEDS REFUELING"))
    print()
    
    # Fleet analysis
    print("=" * 70)
    print("FLEET ANALYSIS (assuming 10 buses with this usage pattern)")
    print("=" * 70)
    
    fleet_size = 10
    total_hydrogen = bus.hydrogen_consumed_kg * fleet_size
    total_distance = bus.state.total_distance_km * fleet_size
    total_energy = bus.state.cumulative_energy_kwh * fleet_size
    
    print(f"Daily hydrogen consumption:     {total_hydrogen:8.1f} kg/day")
    print(f"Daily distance coverage:        {total_distance:8.1f} km/day")
    print(f"Daily energy consumption:       {total_energy:8.1f} kWh/day")
    print()
    
    # Assuming hydrogen costs $8-10 per kg
    hydrogen_cost_per_kg = 9.0
    daily_fuel_cost = total_hydrogen * hydrogen_cost_per_kg
    print(f"Daily fuel cost (@ ${hydrogen_cost_per_kg}/kg):       ${daily_fuel_cost:8.0f}")
    print(f"Annual fuel cost (250 work days): ${daily_fuel_cost * 250:10,.0f}")
    print()
    
    # Compare to diesel
    diesel_mpg_equiv = 5.0  # Typical diesel bus: 5 mpg
    diesel_miles_per_day = total_distance * 0.621371  # Convert km to miles
    diesel_gallons_needed = diesel_miles_per_day / diesel_mpg_equiv
    diesel_cost_per_gallon = 3.50
    diesel_fuel_cost = diesel_gallons_needed * diesel_cost_per_gallon
    
    print(f"Equivalent diesel cost:         ${diesel_fuel_cost:8.0f}/day")
    print(f"Hydrogen savings vs diesel:     ${diesel_fuel_cost - daily_fuel_cost:8.0f}/day")
    print(f"Annual savings (250 work days): ${(diesel_fuel_cost - daily_fuel_cost) * 250:10,.0f}")
    print()


if __name__ == "__main__":
    simulate_daily_operation()
