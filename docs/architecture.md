# System architecture

## Energy flow

The fuel-cell stack converts hydrogen and oxygen into electrical power. A DC/DC converter regulates stack voltage and supplies the high-voltage DC bus. A battery provides transient power during acceleration and stores energy recovered during braking. The inverter drives the traction motor.

## Initial design assumptions

These values are simulation defaults only and must not be treated as production specifications:

| Parameter | Default |
|---|---:|
| Fuel-cell net power | 80 kW |
| Battery usable energy | 30 kWh |
| Battery state of charge | 60% |
| Hydrogen mass | 5 kg |
| Hydrogen energy | 33.3 kWh/kg (lower heating value) |
| Fuel-cell efficiency | 55% |
| Drivetrain efficiency | 90% |
|

## Control strategy

1. Keep the fuel-cell stack near its efficient operating range.
2. Use the battery for short power peaks and rapid transients.
3. Request regenerative braking when the battery has charging capacity.
4. Limit traction power when hydrogen, battery, temperature, or fault conditions exceed safe limits.
5. Shut down the high-voltage system on detected isolation, over-temperature, or hydrogen-leak faults.

## Next engineering work

- Define voltage, current, pressure, temperature, and communication interfaces.
- Create a requirements traceability matrix.
- Select applicable automotive and hydrogen safety standards for the target country.
- Validate all simulated values against supplier data and test measurements.
