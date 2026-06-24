"""
Supply Chain CSV Cleaner - Exercise 1
FDE Academy Day 3
"""

import pandas as pd
from pathlib import Path

# ■■ Valid values for business rules ■■
VALID_STATUSES = {"in_transit", "delivered", "pending", "exception"}
VALID_CARRIERS = {"DHL", "FEDEX", "BLUEDART"}


# ■■ TASK 2A: Load and drop blank rows ■■
def load_shipments(file_path: str) -> pd.DataFrame:
    """
    Load a shipments CSV file into a pandas DataFrame.
    Drop completely empty rows after loading.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame with blank rows removed.
    """
    df = pd.read_csv(file_path, encoding="utf-8")
    # Drop rows where all values are NaN
    df = df.dropna(how="all")
    return df


# ■■ TASK 2B: Normalize/clean each row ■■
def normalise_row(row: pd.Series) -> pd.Series:
    """
    Normalise string fields in a single row:
    - shipment_id: strip whitespace
    - carrier: strip, convert to UPPER
    - status: strip, convert to lower
    - origin: strip, convert to Title Case
    - destination: strip, convert to Title Case
    - delay_days: coerce to int; set to None if not numeric
    - cost_usd: coerce to float; set to None if not numeric

    Args:
        row: A pandas Series representing one CSV row.

    Returns:
        The modified row with cleaned values.
    """
    # Clean shipment_id
    if pd.notna(row.get("shipment_id")):
        row["shipment_id"] = str(row["shipment_id"]).strip()

    # Clean carrier: strip and UPPERCASE
    if pd.notna(row.get("carrier")):
        row["carrier"] = str(row["carrier"]).strip().upper()

    # Clean status: strip and lowercase
    if pd.notna(row.get("status")):
        row["status"] = str(row["status"]).strip().lower()

    # Clean origin: strip and Title Case
    if pd.notna(row.get("origin")):
        row["origin"] = str(row["origin"]).strip().title()

    # Clean destination: strip and Title Case
    if pd.notna(row.get("destination")):
        row["destination"] = str(row["destination"]).strip().title()

    # Coerce delay_days to int (safe - returns NaN if invalid)
    row["delay_days"] = pd.to_numeric(row.get("delay_days"), errors="coerce")

    # Coerce cost_usd to float (safe - returns NaN if invalid)
    row["cost_usd"] = pd.to_numeric(row.get("cost_usd"), errors="coerce")

    return row


# ■■ TASK 2C: Validate against business rules ■■
def validate_row(row: pd.Series) -> list[str]:
    """
    Validate a (already normalised) row against business rules.
    Return a list of error strings. Empty list means the row is valid.

    Rules:
    - shipment_id must not be null or empty string
    - carrier must be in VALID_CARRIERS
    - status must be in VALID_STATUSES
    - delay_days must not be None and must be >= 0
    - cost_usd must not be None and must be > 0

    Args:
        row: A pandas Series with cleaned values.

    Returns:
        List of error strings (empty = valid).
    """
    errors = []

    # Rule 1: shipment_id must not be empty
    shipment_id = row.get("shipment_id")
    if pd.isna(shipment_id) or str(shipment_id).strip() == "":
        errors.append("shipment_id must not be empty")

    # Rule 2: carrier must be valid
    carrier = row.get("carrier")
    if pd.isna(carrier) or carrier not in VALID_CARRIERS:
        errors.append(f"carrier must be in {VALID_CARRIERS}")

    # Rule 3: status must be valid
    status = row.get("status")
    if pd.isna(status) or status not in VALID_STATUSES:
        errors.append(f"status must be in {VALID_STATUSES}")

    # Rule 4: delay_days must be >= 0
    delay = row.get("delay_days")
    if pd.isna(delay) or delay < 0:
        errors.append("delay_days must be >= 0")

    # Rule 5: cost_usd must be > 0
    cost = row.get("cost_usd")
    if pd.isna(cost) or cost <= 0:
        errors.append("cost_usd must be > 0")

    return errors


# ■■ TASK 3: Main cleaning pipeline ■■
def clean_shipments(
    input_path: str,
    clean_output_path: str,
    rejected_output_path: str,
) -> dict:
    """
    Run the full cleaning pipeline:
    - Load CSV using load_shipments()
    - Apply normalise_row() to every row
    - Apply validate_row() to every row
    - Split into clean_df (no errors) and rejected_df (has errors)
    - Write clean_df to clean_output_path
    - Write rejected_df to rejected_output_path with rejection_reasons column
    - Return a summary dict

    Args:
        input_path: Path to raw CSV file.
        clean_output_path: Path to write clean CSV.
        rejected_output_path: Path to write rejected CSV.

    Returns:
        Summary dict with stats.
    """
    # Load data
    df = load_shipments(input_path)

    # Normalize each row
    df = df.apply(normalise_row, axis=1)

    # Validate and split
    clean_rows = []
    rejected_rows = []
    rejection_reasons_set = set()

    for idx, row in df.iterrows():
        errors = validate_row(row)
        if errors:
            # This row is rejected
            row["rejection_reasons"] = ", ".join(errors)
            rejected_rows.append(row)
            # Track all unique error reasons
            for error in errors:
                rejection_reasons_set.add(error)
        else:
            # This row is clean
            clean_rows.append(row)

    # Create DataFrames
    clean_df = pd.DataFrame(clean_rows) if clean_rows else pd.DataFrame()
    rejected_df = pd.DataFrame(rejected_rows) if rejected_rows else pd.DataFrame()

    # Write outputs
    if not clean_df.empty:
        clean_df.to_csv(clean_output_path, index=False, encoding="utf-8")

    if not rejected_df.empty:
        rejected_df.to_csv(rejected_output_path, index=False, encoding="utf-8")

    # Create summary
    total_input = len(df)
    clean_count = len(clean_df)
    rejected_count = len(rejected_df)
    rejection_rate = (rejected_count / total_input * 100) if total_input > 0 else 0

    summary = {
        "total_input": total_input,
        "clean_count": clean_count,
        "rejected_count": rejected_count,
        "rejection_rate_pct": round(rejection_rate, 1),
        "rejection_reasons": sorted(list(rejection_reasons_set)),
    }

    return summary


# ■■ Main entry point ■■
if __name__ == "__main__":
    summary = clean_shipments(
        input_path="shipments_raw.csv",
        clean_output_path="shipments_clean.csv",
        rejected_output_path="shipments_rejected.csv",
    )

    print("\n=== Data Quality Report ===")
    for key, value in summary.items():
        print(f"{key:<25} {value}")
