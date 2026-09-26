# Hydrogen Bus Technical Specifications

This document outlines the baseline specifications for the hydrogen fuel-cell electric bus simulator.

## Vehicle dimensions and capacity

| Parameter | Value |
|---|---:|
| Bus length | 12 m (standard city bus) |
| Bus width | 2.5 m |
| Bus height | 3.4 m |
| Seating capacity | 50 passengers + 1 driver |
| Wheelchair accessible seats | 2 |
| Standing room | ~20 people |
| Curb weight (unladen) | 12,000 kg |
| Gross Vehicle Weight Rating (GVWR) | 18,000 kg |
| Max payload | 6,000 kg |
| Wheelbase | 6.1 m |

## Fuel-cell system

| Parameter | Value |
|---|---:|
| Fuel-cell type | PEM (Proton Exchange Membrane) |
| Rated power | 200 kW |
| Max continuous power | 180 kW |
| Peak power (30 sec) | 220 kW |
| Operating temperature | 50-80°C |
| Electrical efficiency | 50-60% (55% nominal) |
| System voltage (DC bus) | 600-700 V |
| Current rating | 300-400 A |
| Hydrogen inlet pressure | 300-350 bar |
| Water management | Passive humidification |
| Stack lifetime | 25,000+ operating hours |

## Hydrogen storage system

| Parameter | Value |
|---|---:|
| Tank material | Carbon fiber composite with plastic liner (Type IV) |
| Tank volume | ~160 liters |
| Operating pressure | 350 bar (5,000 psi) |
| Nominal hydrogen capacity | 35 kg |
| Max hydrogen capacity | 40 kg |
| Tank weight | ~60 kg (empty) |
| Fill time | 3-5 minutes |
| Safety relief pressure | 375 bar |
| Pressure drop rate (per month) | <1% (sealed) |
| Thermal management | Passive cooling |
| Mounting location | Roof-mounted for center of gravity |
| Qty tanks | 2x (17.5 kg each) or 1x (35 kg) |

## Battery system (buffer)

| Parameter | Value |
|---|---:|
| Type | Lithium-ion (LFP preferred for safety) |
| Nominal voltage | 600 V |
| Capacity | 150 kWh |
| Usable energy | 120-135 kWh (80-90% DoD) |
| Max charging power | 60 kW |
| Max discharge power | 150 kW |
| Energy density | ~120 Wh/kg |
| Total weight | ~1,200 kg |
| Thermal management | Liquid cooling |
| Temperature range | -20°C to +60°C |
| Cell voltage | 3.0-3.65 V (LFP nominal 3.2 V) |
| Module qty | 2x (75 kWh, 300 V each in series) |
| BMS | Multi-layer: cell, module, system |
| Cycle life | 3,000+ cycles at 80% DoD |

## Electric motor and drivetrain

| Parameter | Value |
|---|---:|
| Motor type | AC induction or permanent magnet AC |
| Rated power | 150 kW |
| Peak power | 200 kW (15-30 sec) |
| Max torque | 850 Nm |
| Operating speed range | 0-3,000 rpm |
| Efficiency at rated power | 93-96% |
| Cooling | Liquid cooled |
| Motor weight | ~80 kg |
| Transmission | Single-speed reducer (8.5:1 typical) |
| Reduction efficiency | 95% |
| Differential | Open or limited-slip |
| Regenerative braking | Yes (70-80% recovery typical) |

## Performance characteristics

### Acceleration
- 0-50 km/h: ~12 seconds (fully loaded)
- 0-100 km/h: ~30 seconds (fully loaded)

### Gradability
- Max grade (full load) at 20 km/h: 15%
- Sustained grade (steady state): 8-10%

### Range (baseline)
- Ideal highway (50% load): 450-500 km
- Mixed city driving (75% load): 350-400 km
- Urban stop-and-go (full load): 300-350 km

### Fuel economy
- Best case (highway, minimal stops): 6.5-7.0 km/kg
- Average (mixed): 5.0-5.5 km/kg
- Worst case (urban peak hours): 3.5-4.5 km/kg
