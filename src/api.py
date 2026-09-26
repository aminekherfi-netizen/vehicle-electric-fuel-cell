"""REST API for hydrogen bus fleet management."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import List

from src.dashboard import DashboardDataGenerator, RouteMetrics
from src.energy_simulation import Segment, simulate_route, BusParameters
from src.infrastructure_planning import BusDepotDesign


app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for web frontend

# Initialize generator
generator = DashboardDataGenerator(fleet_size=10)


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "hydrogen-bus-api"}), 200


@app.route("/api/fleet/status", methods=["GET"])
def fleet_status():
    """Get current fleet status."""
    status = generator.fleet_status(
        in_service=request.args.get("in_service", 8, type=int),
        charging=request.args.get("charging", 1, type=int),
        refueling=request.args.get("refueling", 1, type=int),
    )
    return jsonify({
        "timestamp": status.timestamp,
        "total_buses": status.total_buses,
        "buses_in_service": status.buses_in_service,
        "buses_charging": status.buses_charging,
        "buses_refueling": status.buses_refueling,
        "buses_in_maintenance": status.buses_in_maintenance,
        "hydrogen_on_hand_kg": round(status.total_hydrogen_on_hand_kg, 1),
        "battery_soc_percent": status.total_battery_soc_percent,
        "daily_hydrogen_consumption_kg": round(status.daily_hydrogen_consumption_kg, 1),
        "alerts": status.alerts,
    }), 200


@app.route("/api/route/analyze", methods=["POST"])
def analyze_route():
    """Analyze a route and return energy metrics."""
    data = request.json
    
    # Parse route segments
    segments = []
    for seg in data.get("segments", []):
        segments.append(Segment(
            distance_km=seg["distance_km"],
            average_speed_kmh=seg["average_speed_kmh"],
            grade_percent=seg.get("grade_percent", 0.0),
            stops=seg.get("stops", 0),
        ))
    
    passengers = data.get("passengers", 40)
    
    # Simulate route
    metrics = generator.route_analysis(segments, passengers)
    
    return jsonify({
        "route_name": metrics.route_name,
        "distance_km": round(metrics.distance_km, 1),
        "duration_minutes": metrics.estimated_duration_minutes,
        "energy_kwh": round(metrics.estimated_energy_kwh, 1),
        "hydrogen_kg": round(metrics.estimated_hydrogen_kg, 2),
        "fuel_economy_km_per_kg": round(metrics.fuel_economy_km_per_kg, 2),
        "thermal_risk": metrics.thermal_risk,
        "safety_margin_percent": round(metrics.safety_margin_percent, 1),
    }), 200


@app.route("/api/route/compare-scenarios", methods=["POST"])
def compare_scenarios():
    """Compare route metrics across passenger load scenarios."""
    data = request.json
    
    # Parse route segments
    segments = []
    for seg in data.get("segments", []):
        segments.append(Segment(
            distance_km=seg["distance_km"],
            average_speed_kmh=seg["average_speed_kmh"],
            grade_percent=seg.get("grade_percent", 0.0),
            stops=seg.get("stops", 0),
        ))
    
    # Generate scenarios
    scenarios = generator.comparison_scenarios(segments)
    
    result = {}
    for scenario_name, metrics in scenarios.items():
        result[scenario_name] = {
            "energy_kwh": round(metrics.estimated_energy_kwh, 1),
            "hydrogen_kg": round(metrics.estimated_hydrogen_kg, 2),
            "fuel_economy_km_per_kg": round(metrics.fuel_economy_km_per_kg, 2),
            "thermal_risk": metrics.thermal_risk,
            "safety_margin_percent": round(metrics.safety_margin_percent, 1),
        }
    
    return jsonify(result), 200


@app.route("/api/depot/overview", methods=["GET"])
def depot_overview():
    """Get depot infrastructure overview."""
    depot_data = generator.depot_overview()
    return jsonify(depot_data), 200


@app.route("/api/depot/roi", methods=["GET"])
def depot_roi():
    """Get depot ROI analysis."""
    roi = generator.depot.roi_analysis()
    return jsonify({
        "capital_cost_usd": round(roi["capital_cost"], 0),
        "annual_opex_usd": round(roi["annual_opex"], 0),
        "annual_savings_usd": round(roi["annual_savings"], 0),
        "payback_years": round(roi["payback_years"], 1),
        "cumulative_profit_10yr": round(roi["cumulative_profit_10yr"], 0),
        "roi_percent": round(roi["roi_percent"], 1),
    }), 200


@app.route("/api/busses/<int:bus_id>/status", methods=["GET"])
def bus_status(bus_id: int):
    """Get status of a specific bus (simulated)."""
    # Simulated bus data
    return jsonify({
        "bus_id": bus_id,
        "status": "in_service",
        "hydrogen_kg": 28.5,
        "battery_soc_percent": 72,
        "temperature_c": 58,
        "location": f"Route {bus_id % 3 + 1}",
        "passengers": 32,
        "estimated_range_km": 142,
    }), 200


@app.route("/api/alerts", methods=["GET"])
def alerts():
    """Get active alerts across the fleet."""
    status = generator.fleet_status()
    return jsonify({
        "timestamp": status.timestamp,
        "critical_alerts": [],
        "warnings": status.alerts,
        "info": ["Fleet operating normally"],
    }), 200


if __name__ == "__main__":
    print("Starting Hydrogen Bus Fleet API...")
    print("Available endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/fleet/status")
    print("  POST /api/route/analyze")
    print("  POST /api/route/compare-scenarios")
    print("  GET  /api/depot/overview")
    print("  GET  /api/depot/roi")
    print("  GET  /api/busses/<bus_id>/status")
    print("  GET  /api/alerts")
    print()
    app.run(debug=True, port=5000)
