# 10-Bus Hydrogen Depot Concept

## Scope

This is a preliminary planning concept for a depot serving ten 12 m fuel-cell city buses. It is intended to support site selection, duty-cycle analysis, and supplier discussions. It is not a construction, hazardous-area, or permitting package.

## Planning assumptions

| Item | Baseline assumption |
|---|---:|
| Fleet size | 10 buses |
| Daily distance per bus | 200 km |
| Hydrogen use per bus | 5–8 kg/day; use 6.5 kg for planning |
| Fleet hydrogen demand | 65 kg/day |
| Planning reserve | 30% |
| Design supply capacity | At least 85 kg/day |
| Storage pressure | Select certified cascade configuration for the selected dispenser and bus tanks |
| Refueling window | 4 hours overnight, with optional daytime top-up |
| Bus fuel capacity | Approximately 35 kg, subject to final vehicle design |
| Expansion | Space and utilities reserved for 20 buses |

Actual demand should be calculated from measured route data, HVAC load, temperature, passenger load, detours, and the required reserve policy.

## Functional layout

```text
Public road
    |
Entry/exit -- inspection and emergency access
    |
Bus parking and dispatch area
    |
One-way fueling lane --> dispensers --> hydrogen cascade storage / compressor / delivery connection
    |
Maintenance building -- HV isolation area -- workshop -- parts and training
    |
Electrical service / transformer -- controls room -- secure data network
```

Hydrogen equipment should be separated from occupied buildings and ignition sources according to the locally applicable fire, pressure, hazardous-area, and hydrogen-station requirements. A qualified station designer must determine setbacks, ventilation, vent-stack routing, grounding, and classified electrical equipment.

## Hydrogen capacity and throughput

For the baseline fleet:

- Daily hydrogen: `10 × 6.5 = 65 kg/day`
- With 30% reserve: `65 × 1.30 = 84.5 kg/day`
- A practical initial supply target is 85–100 kg/day.
- If each bus receives 35 kg, ten full fills require 350 kg of delivered hydrogen, but most buses will normally return with residual fuel. Storage inventory must therefore be sized from the actual fueling schedule and delivery reliability rather than simply multiplying tank capacity.

Recommended concept equipment:

- Two dispensers or two fueling posts, subject to queue simulation
- Cascade storage sized by the station supplier
- Compressor sized for the delivery method and peak refill window
- Pre-cooling and temperature monitoring where required by the selected fueling protocol
- Delivery connection for tube trailers or another approved hydrogen supply method
- Metering, isolation valves, pressure relief, vent stack, leak detection, and emergency shutdown

A four-hour overnight window with two posts can serve ten buses if refueling appointments are staggered and the station throughput is validated. Provide a daytime contingency slot for route recovery and delayed buses.

## Electrical and utility planning

The electrical design should account for compressor motors, cooling, lighting, workshop loads, HVAC, battery service equipment, and future expansion. Obtain a utility interconnection study before fixing equipment ratings. If on-site electrolysis is considered, separately model electrolyzer power, water treatment, compression, storage, renewable supply, and backup operation; do not assume it is cheaper or simpler than delivered hydrogen.

The depot should include:

- Dedicated electrical switchgear and emergency isolation
- Grounding and bonding designed for hydrogen equipment
- Backup power for controls, alarms, communications, and safe shutdown
- Water and drainage provisions where required by the selected equipment
- Weather protection and corrosion control
- Secure network segmentation for station controls and fleet telemetry

## Safety systems

The final safety design must be based on a hazard analysis and the applicable local regulations. Concept-level provisions include:

- Hydrogen detection in enclosed or potentially accumulating areas
- Forced and natural ventilation designed by a specialist
- Pressure relief devices and safe vent discharge locations
- Emergency-stop stations at entrances, dispensers, equipment, and control room
- Automatic isolation of supply, compressor, and dispenser on critical alarms
- Fire detection and extinguishing strategy approved by the authority having jurisdiction
- Vehicle collision protection around dispensers and storage
- Restricted access, signage, exclusion zones, and hot-work controls
- Safe maintenance isolation and lockout/tagout procedures
- Emergency-response plan, responder training, and periodic drills

Alarm levels, sensor placement, ventilation rates, pressure limits, and separation distances must not be copied from this concept; they require competent fire, process-safety, and pressure-system engineering.

## Operations model

1. Inspect the bus and verify no active hydrogen, HV, or thermal faults.
2. Park and bond the bus according to the approved fueling procedure.
3. Authenticate the vehicle and start the dispenser self-check.
4. Fill using the certified protocol and monitor pressure, temperature, leak status, and mass delivered.
5. Confirm the fill record and move the bus to the dispatch queue.
6. Record hydrogen inventory, compressor state, alarms, maintenance, and emergency events.

Use a station-management system to schedule buses, prevent queue congestion, reconcile mass meters, and maintain an auditable maintenance record.

## Preliminary space schedule

| Area | Planning allowance |
|---|---:|
| Bus parking and circulation | 1,500–2,500 m² |
| Fueling lane and equipment exclusion zones | 300–500 m² |
| Maintenance and HV service | 300–500 m² |
| Hydrogen equipment and delivery access | Specialist layout |
| Administration, training, and control | 100–200 m² |
| Emergency access and expansion margin | Site-specific |

These values are early planning allowances, not a site plan. Turning radii, fire access, drainage, prevailing wind, neighboring properties, flood risk, and emergency-service access must be surveyed.

## Cost and procurement plan

Do not rely on generic cost estimates for approval. Request budgetary quotations for:

- Hydrogen supply and delivery equipment
- Storage cascade and compressor
- Dispensers and metering
- Cooling and electrical systems
- Civil works and fire protection
- Controls, telemetry, cybersecurity, and commissioning
- Training, spares, inspections, insurance, and maintenance

Use stage gates: feasibility, site and utility study, preliminary hazard analysis, 30% design, permitting, detailed design, construction, commissioning, and operational validation.

## Recommended next actions

1. Collect one month of route GPS, elevation, speed, passenger, HVAC, and weather data.
2. Run the repository simulator for each route and establish 95th-percentile daily hydrogen demand.
3. Confirm bus tank pressure and fueling protocol with vehicle and station suppliers.
4. Commission a formal site, fire, process-safety, and hazardous-area assessment.
5. Obtain utility, hydrogen supplier, and equipment budgetary proposals.
6. Prepare emergency procedures and train transit, maintenance, and emergency-response staff.
7. Validate the depot with queue simulation before selecting the number of dispensers.
