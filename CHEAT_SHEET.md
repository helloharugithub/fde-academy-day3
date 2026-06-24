# DAY 3 PYTHON FUNDAMENTALS - QUICK REFERENCE CHEAT SHEET

## 🔧 Most Used Code Snippets

### EXERCISE 1: CSV CLEANER

#### Load and drop empty rows
```python
import pandas as pd
df = pd.read_csv('file.csv', encoding='utf-8')
df = df.dropna(how='all')  # Drop completely empty rows
```

#### String normalization
```python
row['carrier'] = str(row['carrier']).strip().upper()    # "  dhl  " → "DHL"
row['status'] = str(row['status']).strip().lower()      # "IN_TRANSIT" → "in_transit"
row['origin'] = str(row['origin']).strip().title()      # "MUMBAI" → "Mumbai"
```

#### Safe number conversion
```python
row['delay_days'] = pd.to_numeric(row['delay_days'], errors='coerce')  # "abc" → NaN
row['cost_usd'] = pd.to_numeric(row['cost_usd'], errors='coerce')
```

#### Check for None/NaN
```python
if pd.isna(row['shipment_id']):
    errors.append('shipment_id empty')

if pd.notna(row['carrier']):  # Not null
    process(row)
```

#### Split into clean and rejected
```python
clean_rows = []
rejected_rows = []

for idx, row in df.iterrows():
    errors = validate_row(row)
    if errors:
        row['rejection_reasons'] = ', '.join(errors)
        rejected_rows.append(row)
    else:
        clean_rows.append(row)

clean_df = pd.DataFrame(clean_rows)
rejected_df = pd.DataFrame(rejected_rows)
```

---

### EXERCISE 2: JSON PARSER

#### Safe nested access - MOST IMPORTANT!
```python
# ❌ WRONG - Crashes if key missing
email = shipment['carrier']['contact']['email']

# ✅ RIGHT - Returns None if key missing
email = (shipment.get('carrier', {})
         .get('contact', {})
         .get('email'))

# ✅ Also works (assign intermediate values)
carrier = shipment.get('carrier', {})
contact = carrier.get('contact', {})
email = contact.get('email')
```

#### Get last element from array
```python
events = shipment.get('events', [])  # Default to [] if missing

# Get last event (safe)
last_event = events[-1] if events else {}
last_type = last_event.get('type')  # None if no events
```

#### List comprehension for transforms
```python
# One-liner to transform all shipments
records = [extract_shipment_record(s) for s in shipments]

# Equivalent for loop (when logic is complex)
records = []
for shipment in shipments:
    record = extract_shipment_record(shipment)
    records.append(record)
```

#### Accumulate stats in a dict
```python
stats = {}

for record in records:
    code = record['carrier_code']
    
    if code not in stats:
        stats[code] = {
            'shipment_count': 0,
            'total_revenue': 0.0,
            'delayed_count': 0,
        }
    
    # Accumulate
    stats[code]['shipment_count'] += 1
    stats[code]['total_revenue'] += record['charge_total']
    if record['delay_days'] > 0:
        stats[code]['delayed_count'] += 1
```

#### Sort dicts by value
```python
# Sort by total_revenue descending
sorted_list = sorted(stats_list, 
                     key=lambda x: x['total_revenue'], 
                     reverse=True)
```

---

### EXERCISE 3: REPORT GENERATOR

#### GroupBy with aggregations
```python
kpi = (
    df.groupby('carrier')
    .agg(
        total_shipments=('shipment_id', 'count'),
        delivered=('status', lambda x: (x == 'delivered').sum()),
        avg_delay_days=('delay_days', 'mean'),
        max_delay_days=('delay_days', 'max'),
        total_revenue=('cost_usd', 'sum'),
    )
    .reset_index()  # Convert back to normal DataFrame
)
```

#### Calculate percentages
```python
# OTIF = On-Time In-Full %
on_time_delivered = len(df[(df['status'] == 'delivered') & (df['delay_days'] == 0)])
total = len(df)
otif_pct = (on_time_delivered / total * 100) if total > 0 else 0
```

#### Create derived columns
```python
df['route'] = df['origin'] + ' -> ' + df['destination']
# Result: "Mumbai -> Delhi", "Chennai -> Bangalore", etc.

df['flagged'] = df['delay_days'] > 3
# Result: True/False for each row
```

#### Get most common value
```python
# Get the carrier with most shipments on a route
carrier_counts = route_df['carrier'].value_counts()
most_used = carrier_counts.index[0]  # First = highest count
```

#### Filter and iterate
```python
# Get all delayed shipments
delayed = df[df['delay_days'] > 0]

# Print them
for _, row in delayed.iterrows():
    print(f"{row['shipment_id']} delay={row['delay_days']}d")
```

#### Formatted output with f-strings
```python
# Header
print(f"{'Carrier':<15} {'Shipments':>10} {'OTIF%':>8}")
print("-" * 40)

# Data rows
for _, row in kpi.iterrows():
    print(
        f"{row['carrier']:<15} "
        f"{int(row['total_shipments']):>10} "
        f"{row['otif_pct']:>7.1f}%"
    )

# Results in:
# Carrier         Shipments    OTIF%
# ------------------------------------
# DHL                       3    33.3%
# FEDEX                     2    50.0%
```

---

## 📋 Type Hints & Docstrings Template

```python
from typing import Optional

def my_function(
    arg1: str,
    arg2: int,
    arg3: Optional[float] = None,
) -> dict:
    """
    Short description of what the function does.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        arg3: Description of arg3. Defaults to None.
    
    Returns:
        Description of what the function returns.
    
    Examples:
        >>> my_function("hello", 5)
        {'result': ...}
    """
    # Your code here
    return result
```

---

## 🐍 Common Type Hints

```python
# Basic types
x: str              # String
x: int              # Integer
x: float            # Float
x: bool             # Boolean

# Collections
x: list[str]        # List of strings
x: dict[str, int]   # Dict with string keys, int values
x: tuple[str, int]  # Tuple with exactly 2 elements

# Optional (can be None)
x: Optional[str]    # Either str or None
x: str | None       # Same as above (Python 3.10+)

# Union types
x: str | int        # Either str or int

# Functions
x: Callable[[int], str]  # Function that takes int, returns str

# Any type
x: Any              # Any type (use sparingly!)

# Functions return
def func() -> None:     # Returns nothing
def func() -> int:      # Returns an integer
def func() -> str | None:  # Returns string or None
```

---

## 🎯 Common Mistakes & Fixes

### Mistake 1: Direct dict access crashes
```python
# ❌ WRONG
email = data['carrier']['contact']['email']  # KeyError if missing!

# ✅ RIGHT
email = data.get('carrier', {}).get('contact', {}).get('email')
```

### Mistake 2: int() crashes on non-numeric strings
```python
# ❌ WRONG
delay = int(row['delay_days'])  # ValueError on "abc"

# ✅ RIGHT
delay = pd.to_numeric(row['delay_days'], errors='coerce')  # Returns NaN
```

### Mistake 3: Comparing to None with ==
```python
# ❌ WRONG
if value == None:  # Unreliable

# ✅ RIGHT
if value is None:  # Always use "is"
if pd.isna(value):  # For pandas NaN
```

### Mistake 4: Forgetting index=False when saving CSV
```python
# ❌ WRONG - Saves row numbers as first column
df.to_csv('file.csv')

# ✅ RIGHT
df.to_csv('file.csv', index=False)
```

### Mistake 5: Not specifying encoding
```python
# ❌ WRONG - May fail on special characters
df = pd.read_csv('file.csv')

# ✅ RIGHT
df = pd.read_csv('file.csv', encoding='utf-8')
```

---

## 🚀 Commands to Remember

```bash
# Run a Python file
python day3_ex1_cleaner.py

# Format with Black (makes code PEP 8 compliant)
black day3_ex*.py

# Type-check with mypy
mypy day3_ex*.py --ignore-missing-imports

# View CSV file in terminal
head -5 shipments_clean.csv
cat shipments_clean.csv

# Count rows in CSV
wc -l shipments_clean.csv

# Copy to GitHub
git add day3_ex*.py
git commit -m "feat: Day 3 exercises"
git push origin main
```

---

## 📊 Common pandas Operations

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame(list_of_dicts)
df = pd.read_csv('file.csv')

# Inspect
print(df.shape)              # (rows, cols)
print(df.dtypes)             # Column types
print(df.head(5))            # First 5 rows
print(df.isnull().sum())     # Null count per column
print(df.describe())         # Statistics

# Select
df['column']                 # Single column as Series
df[['col1', 'col2']]         # Multiple columns as DataFrame
df.loc[0]                    # Row by label
df.iloc[0]                   # Row by position

# Filter
df[df['age'] > 30]           # Condition
df[(df['age'] > 30) & (df['status'] == 'active')]  # AND
df[(df['age'] > 30) | (df['status'] == 'vip')]     # OR

# Transform
df['new_col'] = df['old_col'] * 2
df['upper'] = df['text'].str.upper()
df['year'] = pd.to_datetime(df['date']).dt.year

# GroupBy
df.groupby('category').agg({'amount': 'sum'})
df.groupby('category')['amount'].mean()

# Sort
df.sort_values('amount', ascending=False)
df.sort_values(['col1', 'col2'])

# Save
df.to_csv('output.csv', index=False)
```

---

## 💡 Debugging Tips

```python
# Print variable type
print(type(variable))
print(isinstance(variable, dict))

# Print with label
print(f"DEBUG: value = {value}")

# Check if key exists in dict
if 'key' in my_dict:
    print("Key exists!")

# Print dict nicely
import json
print(json.dumps(my_dict, indent=2))

# Debug pandas
print(df.info())
print(df[df['column'].isnull()])  # See nulls
```

---

## ✅ Pre-Commit Checklist

Before pushing to GitHub:

```bash
# 1. Format code
black day3_ex*.py

# 2. Type-check
mypy day3_ex*.py --ignore-missing-imports

# 3. Verify outputs
ls -la *.csv
head -1 shipments_clean.csv

# 4. Test one more time
python day3_ex1_cleaner.py
python day3_ex2_json_parser.py
python day3_ex3_report.py

# 5. Commit
git add .
git commit -m "feat: Day 3 complete - CSV cleaner, JSON parser, report"
git push origin main
```

---

**Bookmark this page!** You'll reference it again and again. 📌
