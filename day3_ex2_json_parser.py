"""
Nested JSON API Parser - Exercise 2
FDE Academy Day 3
"""

import json
import pandas as pd
from typing import Optional

# ■■ Mock API Response (paste this at top of your file) ■■
API_RESPONSE = {
    "meta": {"request_id": "REQ-2024-001", "total_records": 3, "page": 1},
    "shipments": [
        {  # SH-001
            "id": "SH-001",
            "reference": "PO-AFB-2024-441",
            "status": {
                "code": "IN_TRANSIT",
                "description": "Package in transit to destination hub",
                "updated_at": "2024-01-20T08:15:00Z",
            },
            "carrier": {
                "name": "DHL Express",
                "code": "DHL",
                "service_type": "EXPRESS",
                "contact": {"email": "ops@dhl.in", "phone": "+91-22-12345678"},
            },
            "route": {
                "origin": {"city": "Mumbai", "state": "MH", "pin": "400001"},
                "destination": {"city": "Delhi", "state": "DL", "pin": "110001"},
                "estimated_delivery": "2024-01-22",
                "distance_km": 1450,
            },
            "events": [
                {
                    "ts": "2024-01-18T10:00:00Z",
                    "location": "Mumbai Warehouse",
                    "type": "PICKUP",
                },
                {
                    "ts": "2024-01-19T06:30:00Z",
                    "location": "Nagpur Hub",
                    "type": "IN_TRANSIT",
                },
                {
                    "ts": "2024-01-20T08:15:00Z",
                    "location": "Delhi Hub",
                    "type": "ARRIVED",
                },
            ],
            "charges": {
                "base": 850.0,
                "fuel_surcharge": 127.5,
                "gst": 177.75,
                "total": 1155.25,
            },
            "delay_days": 0,
        },
        {  # SH-002
            "id": "SH-002",
            "reference": "PO-AFB-2024-442",
            "status": {
                "code": "DELAYED",
                "description": "Delayed due to customs clearance",
                "updated_at": "2024-01-20T07:00:00Z",
            },
            "carrier": {
                "name": "FedEx India",
                "code": "FEDEX",
                "service_type": "STANDARD",
                "contact": {"email": "support@fedex.in"},
            },
            "route": {
                "origin": {"city": "Chennai", "state": "TN", "pin": "600001"},
                "destination": {"city": "Bangalore", "state": "KA", "pin": "560001"},
                "estimated_delivery": "2024-01-21",
                "distance_km": 346,
            },
            "events": [
                {
                    "ts": "2024-01-18T14:00:00Z",
                    "location": "Chennai Port",
                    "type": "PICKUP",
                },
                {
                    "ts": "2024-01-20T07:00:00Z",
                    "location": "Customs Delhi",
                    "type": "HELD",
                },
            ],
            "charges": {
                "base": 320.0,
                "fuel_surcharge": 48.0,
                "gst": 66.24,
                "total": 434.24,
            },
            "delay_days": 3,
        },
        {  # SH-003
            "id": "SH-003",
            "reference": None,
            "status": {"code": "DELIVERED", "updated_at": "2024-01-19T16:00:00Z"},
            "carrier": {
                "name": "BlueDart",
                "code": "BLUEDART",
                "service_type": "ECONOMY",
            },
            "route": {
                "origin": {"city": "Pune"},
                "destination": {"city": "Hyderabad", "state": "TS", "pin": "500001"},
                "estimated_delivery": "2024-01-19",
                "distance_km": 559,
            },
            "events": [
                {
                    "ts": "2024-01-17T09:00:00Z",
                    "location": "Pune Depot",
                    "type": "PICKUP",
                },
                {
                    "ts": "2024-01-19T16:00:00Z",
                    "location": "Hyderabad Depot",
                    "type": "DELIVERED",
                },
            ],
            "charges": {"base": 180.0, "gst": 32.4, "total": 212.4},
            "delay_days": 0,
        },
    ],
}


# ■■ TASK 2A: Flatten one shipment ■■
def extract_shipment_record(shipment: dict) -> dict:
    """
    Flatten a single shipment dict from the API response into a flat record.

    Safe nested access using .get() - never raises KeyError.

    Args:
        shipment: One shipment dict from API_RESPONSE['shipments'].

    Returns:
        A flat dict with keys:
        - shipment_id, reference, status_code, status_desc
        - carrier_name, carrier_code, service_type, carrier_email
        - origin_city, origin_state, dest_city, dest_state
        - est_delivery, distance_km
        - event_count, latest_event_type, latest_event_loc
        - charge_base, charge_gst, charge_total
        - delay_days
    """
    # Level 1: Top-level fields
    shipment_id = shipment.get("id")
    reference = shipment.get("reference")

    # Level 2: Status object
    status = shipment.get("status", {})
    status_code = status.get("code")
    status_desc = status.get("description")

    # Level 2: Carrier object
    carrier = shipment.get("carrier", {})
    carrier_name = carrier.get("name")
    carrier_code = carrier.get("code")
    service_type = carrier.get("service_type")

    # Level 3: Carrier contact (nested in carrier)
    contact = carrier.get("contact", {})
    carrier_email = contact.get("email")

    # Level 2: Route object
    route = shipment.get("route", {})
    origin = route.get("origin", {})
    origin_city = origin.get("city")
    origin_state = origin.get("state")

    destination = route.get("destination", {})
    dest_city = destination.get("city")
    dest_state = destination.get("state")

    est_delivery = route.get("estimated_delivery")
    distance_km = route.get("distance_km")

    # Level 2: Events list
    events = shipment.get("events", [])
    event_count = len(events)
    # Get the LAST event
    latest_event = events[-1] if events else {}
    latest_event_type = latest_event.get("type")
    latest_event_loc = latest_event.get("location")

    # Level 2: Charges object
    charges = shipment.get("charges", {})
    charge_base = charges.get("base")
    charge_gst = charges.get("gst")
    charge_total = charges.get("total")

    # Top level: delay
    delay_days = shipment.get("delay_days", 0)

    # Return flat dict
    return {
        "shipment_id": shipment_id,
        "reference": reference,
        "status_code": status_code,
        "status_desc": status_desc,
        "carrier_name": carrier_name,
        "carrier_code": carrier_code,
        "service_type": service_type,
        "carrier_email": carrier_email,
        "origin_city": origin_city,
        "origin_state": origin_state,
        "dest_city": dest_city,
        "dest_state": dest_state,
        "est_delivery": est_delivery,
        "distance_km": distance_km,
        "event_count": event_count,
        "latest_event_type": latest_event_type,
        "latest_event_loc": latest_event_loc,
        "charge_base": charge_base,
        "charge_gst": charge_gst,
        "charge_total": charge_total,
        "delay_days": delay_days,
    }


# ■■ TASK 2B: Parse all shipments ■■
def parse_api_response(response: dict) -> list[dict]:
    """
    Extract all shipment records from the full API response.

    Args:
        response: The complete API response dict.

    Returns:
        List of flat shipment record dicts. Empty list if 'shipments' key missing.
    """
    shipments_list = response.get("shipments", [])
    # Use list comprehension to apply extract_shipment_record to each shipment
    records = [extract_shipment_record(shipment) for shipment in shipments_list]
    return records


# ■■ TASK 2C: Compute carrier summary ■■
def compute_carrier_summary(records: list[dict]) -> list[dict]:
    """
    Group parsed records by carrier_code and compute per-carrier stats.

    Args:
        records: List of flat shipment records from parse_api_response().

    Returns:
        List of dicts (one per carrier), sorted by total_revenue descending.
        Each dict contains:
        - carrier_code, carrier_name
        - shipment_count, total_revenue, delayed_count, avg_delay_days
    """
    # Build a dict keyed by carrier_code
    stats = {}

    for record in records:
        code = record.get("carrier_code")
        name = record.get("carrier_name")
        revenue = record.get("charge_total") or 0.0
        delay = record.get("delay_days", 0)

        if code not in stats:
            stats[code] = {
                "carrier_code": code,
                "carrier_name": name,
                "shipment_count": 0,
                "total_revenue": 0.0,
                "delayed_count": 0,
                "total_delay_days": 0,
            }

        # Accumulate stats
        stats[code]["shipment_count"] += 1
        stats[code]["total_revenue"] += revenue
        if delay > 0:
            stats[code]["delayed_count"] += 1
        stats[code]["total_delay_days"] += delay

    # Convert to list and compute avg_delay_days
    summary_list = []
    for code, stat in stats.items():
        stat["avg_delay_days"] = round(
            stat["total_delay_days"] / stat["shipment_count"], 1
        )
        # Remove intermediate field
        del stat["total_delay_days"]
        summary_list.append(stat)

    # Sort by total_revenue descending
    summary_list = sorted(summary_list, key=lambda x: x["total_revenue"], reverse=True)

    return summary_list


# ■■ Main entry point ■■
if __name__ == "__main__":
    records = parse_api_response(API_RESPONSE)
    print(f"Parsed {len(records)} shipment records")

    # Save to CSV
    df = pd.DataFrame(records)
    df.to_csv("shipments_parsed.csv", index=False)
    print("Saved: shipments_parsed.csv")

    # Print carrier summary
    summary = compute_carrier_summary(records)
    print("\n=== Carrier Summary ===")
    for row in summary:
        print(
            f"\t{row['carrier_name']:<15} "
            f"shipments={row['shipment_count']} "
            f"revenue=${row['total_revenue']:,.2f} "
            f"delayed={row['delayed_count']} "
            f"avg_delay={row['avg_delay_days']}d"
        )
