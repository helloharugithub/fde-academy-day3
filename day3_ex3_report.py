"""
Automated Summary Report Generator - Exercise 3
FDE Academy Day 3

Daily shipment operations report for AutoFinance Bank.
Reads cleaned CSV, computes KPIs, generates reports.
"""

import pandas as pd
from pathlib import Path
from datetime import date

# File paths
INPUT_FILE = "shipments_clean.csv"
SUMMARY_CSV = "shipments_summary.csv"
ROUTES_CSV = "route_report.csv"


# ■■ TASK 2A: Compute carrier-level KPIs ■■
def compute_carrier_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-carrier KPIs from the cleaned shipments DataFrame.

    Args:
        df: DataFrame with columns: shipment_id, carrier, status, delay_days, cost_usd

    Returns:
        DataFrame with one row per carrier and columns:
        - carrier: carrier name
        - total_shipments: count of all shipments
        - delivered: count where status == "delivered"
        - in_transit: count where status == "in_transit"
        - otif_pct: on-time delivery % (delivered with delay_days==0), 1 decimal
        - avg_delay_days: mean delay, 1 decimal
        - max_delay_days: worst delay
        - total_revenue: sum of cost_usd
        - avg_cost_per_ship: mean cost_usd, 2 decimals

        Sorted by total_shipments descending.
    """
    # Group by carrier and compute aggregations
    kpi = (
        df.groupby("carrier")
        .agg(
            total_shipments=("shipment_id", "count"),
            delivered=("status", lambda x: (x == "delivered").sum()),
            in_transit=("status", lambda x: (x == "in_transit").sum()),
            avg_delay_days=("delay_days", "mean"),
            max_delay_days=("delay_days", "max"),
            total_revenue=("cost_usd", "sum"),
            avg_cost_per_ship=("cost_usd", "mean"),
        )
        .reset_index()
    )

    # Compute OTIF% (on-time, in-full)
    # OTIF = (delivered with delay_days == 0) / total_shipments * 100
    def calculate_otif(group_df):
        """Calculate OTIF for a carrier."""
        # Count delivered shipments with 0 delay
        on_time_delivered = len(
            group_df[
                (group_df["status"] == "delivered") & (group_df["delay_days"] == 0)
            ]
        )
        total = len(group_df)
        otif = (on_time_delivered / total * 100) if total > 0 else 0
        return otif

    # Create a new column for OTIF using apply
    otif_values = []
    for carrier in kpi["carrier"]:
        carrier_df = df[df["carrier"] == carrier]
        otif = calculate_otif(carrier_df)
        otif_values.append(round(otif, 1))

    kpi["otif_pct"] = otif_values

    # Round numeric columns
    kpi["avg_delay_days"] = kpi["avg_delay_days"].round(1)
    kpi["max_delay_days"] = kpi["max_delay_days"].astype(int)
    kpi["total_revenue"] = kpi["total_revenue"].round(2)
    kpi["avg_cost_per_ship"] = kpi["avg_cost_per_ship"].round(2)

    # Sort by total_shipments descending
    kpi = kpi.sort_values("total_shipments", ascending=False).reset_index(drop=True)

    return kpi


# ■■ TASK 2B: Compute route-level report ■■
def compute_route_report(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Compute a route-level report grouped by (origin, destination) pair.

    Args:
        df: DataFrame with shipment data.
        top_n: Return only top N routes by shipment count.

    Returns:
        DataFrame with columns:
        - route: "Mumbai -> Delhi" format
        - shipment_count: number of shipments on this route
        - avg_delay_days: mean delay, 1 decimal
        - total_revenue: sum of costs, 2 decimals
        - most_used_carrier: carrier with highest count on this route
    """
    # Create a route column
    df_route = df.copy()
    df_route["route"] = df_route["origin"] + " -> " + df_route["destination"]

    # Group by route
    route_stats = (
        df_route.groupby("route")
        .agg(
            shipment_count=("shipment_id", "count"),
            avg_delay_days=("delay_days", "mean"),
            total_revenue=("cost_usd", "sum"),
        )
        .reset_index()
    )

    # Find the most-used carrier per route
    def get_most_used_carrier(route_name):
        """Get the carrier with most shipments on a route."""
        route_df = df_route[df_route["route"] == route_name]
        carrier_counts = route_df["carrier"].value_counts()
        return carrier_counts.index[0] if len(carrier_counts) > 0 else None

    route_stats["most_used_carrier"] = route_stats["route"].apply(get_most_used_carrier)

    # Round numeric columns
    route_stats["avg_delay_days"] = route_stats["avg_delay_days"].round(1)
    route_stats["total_revenue"] = route_stats["total_revenue"].round(2)

    # Sort by shipment_count descending and take top_n
    route_stats = route_stats.sort_values(
        "shipment_count", ascending=False
    ).reset_index(drop=True)
    route_stats = route_stats.head(top_n)

    return route_stats


# ■■ TASK 2C: Print formatted console report ■■
def print_console_report(
    df: pd.DataFrame,
    carrier_kpis: pd.DataFrame,
    route_report: pd.DataFrame,
) -> None:
    """
    Print a formatted operations report to the console.

    Includes:
    - Report header with today's date
    - Overall KPIs
    - Per-carrier KPI table
    - Top routes table
    - Flagged shipments (delay > 3 days)

    Args:
        df: Full shipment DataFrame.
        carrier_kpis: Result from compute_carrier_kpis().
        route_report: Result from compute_route_report().
    """
    today = date.today().strftime("%Y-%m-%d")

    # Header
    print(f"\n{'='*80}")
    print(f"AutoFinance Bank — Daily Shipment Report [{today}]")
    print(f"{'='*80}\n")

    # Overall KPIs
    total_shipments = len(df)
    total_revenue = df["cost_usd"].sum()

    # Overall OTIF: count on-time delivered / total * 100
    on_time_delivered = len(df[(df["status"] == "delivered") & (df["delay_days"] == 0)])
    overall_otif = (
        (on_time_delivered / total_shipments * 100) if total_shipments > 0 else 0
    )

    avg_delay = df["delay_days"].mean()

    print(
        f"Total Shipments: {total_shipments} | "
        f"Total Revenue: ${total_revenue:,.2f} | "
        f"Overall OTIF: {overall_otif:.1f}% | "
        f"Avg Delay: {avg_delay:.1f} days\n"
    )

    # Carrier KPI table
    print("=== Carrier KPIs ===")
    print(
        f"{'Carrier':<15} {'Shipments':>10} {'Delivered':>10} {'OTIF%':>8} "
        f"{'Avg Delay':>10} {'Revenue':>12}"
    )
    print("-" * 75)
    for _, row in carrier_kpis.iterrows():
        print(
            f"{row['carrier']:<15} "
            f"{int(row['total_shipments']):>10} "
            f"{int(row['delivered']):>10} "
            f"{row['otif_pct']:>7.1f}% "
            f"{row['avg_delay_days']:>9.1f}d "
            f"${row['total_revenue']:>11,.2f}"
        )
    print()

    # Route report table
    print("=== Top Routes ===")
    print(
        f"{'Route':<30} {'Count':>8} {'Avg Delay':>12} {'Revenue':>12} {'Top Carrier':<15}"
    )
    print("-" * 75)
    for _, row in route_report.iterrows():
        print(
            f"{row['route']:<30} "
            f"{int(row['shipment_count']):>8} "
            f"{row['avg_delay_days']:>11.1f}d "
            f"${row['total_revenue']:>11,.2f} "
            f"{row['most_used_carrier']:<15}"
        )
    print()

    # Flagged shipments (delay > 3 days)
    flagged = df[df["delay_days"] > 3]
    if len(flagged) > 0:
        print("⚠️  Flagged Shipments (delay > 3 days):")
        for _, row in flagged.iterrows():
            print(
                f"  {row['shipment_id']:<8} {row['carrier']:<10} "
                f"{row['status']:<12} delay={int(row['delay_days'])}d "
                f"cost=${row['cost_usd']:,.2f}"
            )
    else:
        print("✓ No flagged shipments (all delays <= 3 days)")

    print(f"\n{'='*80}\n")


# ■■ TASK 3: Main pipeline ■■
def main() -> None:
    """
    Run the full report generation pipeline.

    Steps:
    1. Load cleaned CSV
    2. Quality gate: check required columns and data
    3. Compute KPIs
    4. Save CSV outputs
    5. Print console report
    """
    # Step 1: Load data
    if not Path(INPUT_FILE).exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    # Step 2: Quality gate
    required_cols = {"shipment_id", "carrier", "status", "delay_days", "cost_usd"}
    missing = required_cols - set(df.columns)

    if missing:
        print(f"ERROR: Missing required columns: {missing}")
        return

    if len(df) == 0:
        print("ERROR: Input file contains no data rows")
        return

    # Step 3: Compute KPIs
    carrier_kpis = compute_carrier_kpis(df)
    route_report = compute_route_report(df, top_n=5)

    # Step 4: Save CSV outputs
    carrier_kpis.to_csv(SUMMARY_CSV, index=False)
    route_report.to_csv(ROUTES_CSV, index=False)

    # Step 5: Print report
    print_console_report(df, carrier_kpis, route_report)
    print(f"Saved: {SUMMARY_CSV} | {ROUTES_CSV}")


# ■■ Entry point ■■
if __name__ == "__main__":
    main()
