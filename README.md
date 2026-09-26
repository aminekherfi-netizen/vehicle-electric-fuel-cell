# Hydrogen Fuel-Cell Electric Bus

An engineering project for designing and simulating a zero-emission public transit bus powered by hydrogen fuel-cell technology.

## Goals

- Model hydrogen fuel-cell power system for buses (40-60 passengers)
- Estimate bus energy consumption and daily operational range
- Monitor hydrogen level, battery state of charge, and system efficiency
- Track passenger load effects on energy consumption
- Provide foundation for fleet management and charging infrastructure planning
- Enable integration with public transit scheduling systems

## System overview

```text
Hydrogen tank (350-700 bar) -> Fuel-cell stack (150-250 kW) -> DC/DC converter -> Battery buffer (100-200 kWh) -> Inverter -> Electric motor (150-200 kW)
                                                                                      ^
                                                                                      |
                                                            Regenerative braking (bus stops, downhill)
```

## Bus specifications (baseline model)

| Parameter | Value |
|---|---:|
| Seating capacity | 50 passengers + driver |
| Fuel-cell power rating | 200 kW |
| Battery usable energy | 150 kWh |
| Hydrogen tank capacity | 35-40 kg |
| Estimated range (full tank, loaded) | 300-400 km |
| Weight (curb) | ~12,000 kg |
| Length | 12 m (standard city bus) |

## Project structure

```text
.
├── docs/
│   ├── architecture.md
│   ├── bus-specifications.md
│   ├── safety-requirements.md
│   └── charging-infrastructure.md
├── src/
│   ├── hydrogen_bus_sim.py
│   ├── passenger_load.py
│   └── fleet_telemetry.py
├── tests/
│   ├── test_hydrogen_bus_sim.py
│   └── test_passenger_load.py
├── examples/
│   └── daily_route_simulation.py
└── pyproject.toml
```

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/aminekherfi-netizen/vehicle-electric-fuel-cell
cd vehicle-electric-fuel-cell
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
python -m src.hydrogen_bus_sim
python examples/daily_route_simulation.py
```

## Safety notice

This repository is for simulation, education, and early-stage engineering only.

**Hydrogen systems require:**
- Certified fuel-cell stacks with pressure relief and isolation valves
- Reinforced hydrogen storage tanks (350+ bar, DOT-approved)
- High-voltage battery thermal management and isolation
- Ventilation and leak detection systems
- Electromagnetic compatibility (EMC) testing
- Functional safety assessment (ISO 26262)
- Regulatory compliance (EU 2014/94, FMVSS, local transit authority requirements)

**DO NOT attempt physical implementation without:**
- Professional engineering review by certified specialists
- Compliance testing by accredited laboratories
- Insurance and liability coverage
- Full safety case documentation

## Key features

✅ **Bus-specific power modeling** – 200+ kW fuel-cell for city acceleration and hill climbing  
✅ **Passenger load simulation** – Model weight and energy consumption changes  
✅ **Daily route planning** – Simulate complete bus routes with stops and schedules  
✅ **Energy efficiency analysis** – Track fuel economy (km per kg hydrogen)  
✅ **Regenerative braking** – Recover energy at bus stops and downhill sections  
✅ **Thermal management** – Monitor fuel-cell and battery temperatures  
✅ **Fleet telemetry** – Log energy, range, and operational metrics  

## Roadmap

- [ ] Add vehicle longitudinal dynamics (acceleration, deceleration, gradients)
- [ ] Add hydrogen tank pressure and temperature model
- [ ] Add battery thermal model with heating/cooling
- [ ] Add motor and inverter efficiency maps
- [ ] Add CAN telemetry interface for real-time monitoring
- [ ] Add route optimization for fuel consumption
- [ ] Add charging infrastructure cost calculator
- [ ] Add maintenance prediction model
- [ ] Add hardware-in-the-loop (HIL) simulation interface
- [ ] Document component selection and supplier recommendations

## Example use cases

```python
from src.hydrogen_bus_sim import HydrogenBus, BusRoute, PassengerLoad

# Create a bus with full hydrogen tank
bus = HydrogenBus(hydrogen_kg=35.0, battery_kwh=150.0)

# Define a city bus route (12 stops, 20 km)
route = BusRoute(
    name="Route 42 Downtown",
    distance_km=20.0,
    stops=12,
    elevation_gain_m=150
)

# Simulate full day with varying passenger loads
morning_load = PassengerLoad(passengers=45, luggage_kg=500)
midday_load = PassengerLoad(passengers=30, luggage_kg=300)

energy_used = bus.run_route(route, morning_load)
print(f"Energy consumed: {energy_used:.1f} kWh")
print(f"Fuel economy: {route.distance_km / bus.hydrogen_consumed:.1f} km/kg")
```

## Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Add tests for new functionality
3. Update documentation
4. Submit a pull request

## License

To be selected (consider: MIT, Apache 2.0, or GPL for open-source hydrogen tech)

## References

- ISO 14687 - Hydrogen fuel quality
- ISO 26262 - Functional Safety (Automotive)
- SAE J2601 - Hydrogen refueling protocols
- EN 14687 - Hydrogen purity requirements
- FMVSS 304 - Hydrogen fuel system safety (US)
