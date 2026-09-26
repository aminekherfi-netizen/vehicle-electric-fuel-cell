# Electric Fuel Cell Vehicle

A starter project for designing and simulating an electric vehicle powered by a hydrogen fuel-cell system.

## Goals

- Model the fuel-cell power system
- Estimate vehicle energy consumption and range
- Monitor hydrogen level, battery state of charge, and system efficiency
- Provide a foundation for hardware integration and control software

## System overview

```text
Hydrogen tank -> Fuel-cell stack -> DC/DC converter -> Battery buffer -> Inverter -> Electric motor
                                                        ^
                                                        |
                                              Regenerative braking
```

## Project structure

```text
.
├── docs/
│   └── architecture.md
├── src/
│   └── fuel_cell_sim.py
├── tests/
│   └── test_fuel_cell_sim.py
└── pyproject.toml
```

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
python -m src.fuel_cell_sim
```

## Safety notice

This repository is for simulation, education, and early-stage engineering. Hydrogen systems, high-voltage batteries, fuel-cell stacks, and vehicle propulsion systems require qualified engineering review, certified components, ventilation, pressure protection, electrical isolation, and compliance testing before any physical implementation.

## Roadmap

- [ ] Add vehicle longitudinal dynamics
- [ ] Add hydrogen tank pressure and temperature model
- [ ] Add battery thermal model
- [ ] Add motor and inverter efficiency maps
- [ ] Add CAN telemetry interface
- [ ] Add hardware-in-the-loop tests
- [ ] Document component selection and safety requirements

## License

License to be selected.
