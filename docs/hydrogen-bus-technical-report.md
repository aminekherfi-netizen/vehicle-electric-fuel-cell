# Hydrogen Fuel-Cell City Bus: Technical Report

**Project:** Hydrogen Fuel-Cell Electric Bus  
**Version:** 1.0 — concept-stage engineering document  
**Status:** Pre-feasibility and simulation baseline

## 1. Executive summary

This report defines a concept for a 12 m hydrogen fuel-cell electric city bus. The bus uses a proton-exchange membrane (PEM) fuel-cell system as its primary energy source and a high-voltage battery as a transient-power buffer. Hydrogen is converted to electricity on board; the only direct exhaust products are water and heat.

The concept targets urban routes with frequent stops, variable passenger loading, moderate hills, and a daily operating distance of approximately 150–300 km. The baseline configuration uses a 180–200 kW fuel-cell system, a 100–150 kWh usable battery, and approximately 35 kg of hydrogen storage. These are design assumptions for simulation and must be replaced by certified supplier data during detailed design.

The project is not a production design. Pressure vessels, high-voltage systems, fuel-cell stacks, controls, and depot equipment require qualified engineering, hazard analysis, certification, and authority approval before construction or operation.

## 2. Design requirements

| Requirement | Concept target |
|---|---:|
| Vehicle length | 12 m |
| Passenger capacity | 40–60 passengers plus driver |
| Gross vehicle mass | Up to approximately 18,000 kg |
| Fuel-cell net power | 180–200 kW |
| Battery usable energy | 100–150 kWh |
| Hydrogen storage | 35–40 kg; pressure selected by certified system supplier |
| Daily operating distance | 150–300 km |
| Target range | 300–400 km, route and climate dependent |
| Refueling time | Approximately 10–20 minutes for a bus-depot operation, subject to station design |
| Drive system | Electric traction motor with regenerative braking |

## 3. System architecture

```text
Hydrogen tanks
     |
Shutoff valves, pressure regulation, leak detection
     |
PEM fuel-cell stack --> DC/DC converter --> High-voltage DC bus --> Inverter --> Traction motor
                                               ^       |
                                               |       +--> Auxiliary DC/DC --> 24 V loads
                                        Battery + BMS
                                               ^
                                        Regenerative braking
```

The energy-management controller should operate the fuel cell in an efficient and thermally stable region whenever possible. The battery supplies short-duration peak power, absorbs regenerative energy, and provides limited limp-home capability according to the safety case.

## 4. Major components

### 4.1 PEM fuel-cell system

The fuel-cell system includes the stack, air compressor, humidification and water-management equipment, hydrogen regulation, cooling loop, sensors, and supervisory controller. A 180–200 kW net rating is a suitable concept starting point for a 12 m bus, but the final rating must be verified against acceleration, gradeability, HVAC, and auxiliary-load requirements.

Important design parameters include net power, efficiency map, start-up time, operating temperature, reactant stoichiometry, pressure limits, degradation rate, and service life. The simulator uses 55% electrical efficiency as a nominal assumption; actual efficiency varies with load and operating conditions.

### 4.2 Hydrogen storage

Hydrogen storage should use certified automotive pressure vessels, isolation valves, pressure and temperature sensors, pressure-relief devices, and controlled vent routing. Roof mounting may improve packaging and crash separation, but it affects center of gravity, rollover analysis, roof structure, and maintenance access.

Storage capacity must be determined from the duty cycle, reserve policy, ambient conditions, degradation margin, and refueling availability. A nominal 35 kg tank is an initial modeling assumption, not a procurement specification.

### 4.3 Battery buffer

The battery provides power during launch and hill climbing and stores recovered braking energy. A liquid-cooled pack with a robust battery-management system should monitor cell voltage, temperature, current, isolation, state of charge, and state of health. Usable energy should be limited by an operating window rather than the nameplate capacity.

Battery sizing is a trade-off: a larger battery reduces fuel-cell transients but adds mass, cost, and thermal load. A preliminary 100–150 kWh usable range is appropriate for this concept.

### 4.4 Electric drivetrain

A 150–200 kW liquid-cooled motor with a single-speed reduction gear is a reasonable starting point. The design must validate wheel torque, launch performance, sustained gradeability, maximum speed, axle loads, braking balance, and regenerative-braking limits under full passenger load.

### 4.5 Thermal management

Separate but coordinated cooling loops may be required for the fuel-cell stack, battery, inverter, motor, and cabin HVAC. The fuel cell rejects significant heat because not all hydrogen chemical energy becomes electricity. Thermal controls should include coolant flow, radiator fans, pump monitoring, temperature derating, and safe shutdown.

## 5. Energy model

For each route segment, the traction model estimates:

- Rolling resistance: `F_roll = Crr × m × g`
- Aerodynamic drag: `F_drag = 0.5 × rho × Cd × A × v²`
- Grade force: `F_grade = m × g × grade`
- Acceleration force: `F_accel = m × a`
- Wheel power: `P_wheel = (F_roll + F_drag + F_grade + F_accel) × v`
- Electrical energy: wheel energy divided by drivetrain efficiency, minus bounded regenerative recovery
- Hydrogen use: fuel-cell electrical energy divided by `efficiency × hydrogen lower-heating-value`

The model should include auxiliary energy for HVAC, doors, pumps, lighting, and controls. City-bus HVAC can materially change consumption, especially in hot or cold climates.

## 6. Controls and operating strategy

1. Precondition the battery and fuel-cell system where depot facilities permit.
2. Start the fuel cell through a monitored sequence and verify hydrogen, coolant, air, and isolation status.
3. Request battery power for fast transients within current, state-of-charge, and temperature limits.
4. Operate the fuel cell near its efficient region during steady travel.
5. Limit regenerative braking when the battery is full, cold, hot, or faulted.
6. Apply torque, speed, and power derating on thermal, pressure, isolation, or hydrogen-leak warnings.
7. On a critical fault, isolate hydrogen and high voltage, notify the driver, and place the bus in a defined safe state.

## 7. Safety concept

The safety case should be developed using a hazard analysis and risk assessment. Hazards include hydrogen release, fire or explosion, high voltage, electrical isolation loss, pressure-vessel failure, thermal runaway, loss of braking, unintended propulsion, collision damage, and emergency-responder exposure.

Recommended protection layers include:

- Hydrogen sensors in tank, roof, passenger, and underbody zones as appropriate
- Automatic hydrogen isolation and controlled venting
- Pressure relief and excess-flow protection
- High-voltage interlock loop and insulation monitoring
- Battery contactors with welded-contactor detection
- Cell-level battery monitoring and thermal-event detection
- Crash-triggered energy and hydrogen isolation
- Clearly defined emergency stop points and responder information
- Ventilation that prevents accumulation in enclosed spaces
- Fire detection and extinguishing provisions selected by the safety engineer
- Preventive maintenance, inspection, and leak-test procedures

Never use the numerical alarm thresholds in an early simulator as certified setpoints. Setpoints must come from the applicable regulations, sensor characteristics, hazard analysis, and authority approval.

## 8. Depot and refueling

A 10-bus depot should be designed around the real duty cycle, not only tank capacity. The site study should define daily hydrogen demand, reserve inventory, delivery method, compression and storage, dispenser throughput, queueing, electrical service, hazardous-area classification, ventilation, emergency access, separation distances, and future expansion.

A preliminary 10-bus fleet consuming 5–8 kg per bus per operating day requires approximately 50–80 kg/day before reserve and seasonal margins. A concept design should normally include delivery and storage capacity for at least the planned operating window plus an agreed contingency margin.

## 9. Verification and validation plan

### Simulation

- Unit-test resistance, grade, acceleration, braking, thermal, and hydrogen calculations.
- Run route simulations using measured GPS, speed, elevation, passenger, and weather data.
- Compare predicted energy and hydrogen use with instrumented vehicle data.

### Hardware and system tests

- Component-level electrical, cooling, pressure, and communications tests
- Software-in-the-loop and hardware-in-the-loop tests
- Fault-injection tests for sensors, contactors, coolant, hydrogen, and isolation
- Environmental, EMC, vibration, ingress, crash, and abuse tests as required
- Controlled commissioning with a documented safety case

## 10. Standards and approvals

The applicable standards depend on the country and vehicle classification. The engineering team should confirm the current editions and legal applicability with the relevant authority. Candidate references include ISO 26262 for functional safety, ISO 19880-1 for hydrogen refueling stations, ISO 14687 for hydrogen quality, SAE J2601 where applicable to the fueling protocol, and applicable UNECE, FMVSS, national pressure-vessel, electrical, fire, and public-transit requirements.

## 11. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Hydrogen supply interruption | Dual sourcing, reserve inventory, delivery contingency |
| Cold-weather performance | Thermal preconditioning and validated cold-start strategy |
| Battery thermal event | Cell monitoring, cooling, isolation, propagation testing |
| Excessive route energy | Validate route data; reserve power and hydrogen margin |
| High station utilization | Queue simulation, additional posts, staged fueling |
| Stack degradation | Supplier lifetime data, diagnostics, replacement plan |
| Public and responder safety | Training, signage, emergency procedures, drills |
| Cost overrun | Stage-gated design and supplier quotations |

## 12. Conclusion

A hydrogen fuel-cell electric bus is technically suitable for long daily urban duty cycles where rapid refueling and long range are valuable. The concept should proceed in stages: define the duty cycle, calibrate the energy model, select certified components, design the depot, perform hazard analysis, and complete regulated vehicle validation. The code in this repository is a planning and education tool; it must not be used as a control system or as evidence of compliance.
