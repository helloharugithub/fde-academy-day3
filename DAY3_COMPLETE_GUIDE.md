# Day 3 Python Fundamentals - Complete Guide
## FDE Academy - Easy to Understand Version

---

## 📚 **What You're Learning Today**

You'll master **real-world Python skills** that FDEs use on Day 1 of client engagements:

1. **CSV Cleaning** - Take messy data and make it usable
2. **JSON Parsing** - Flatten nested API responses  
3. **Report Generation** - Create summaries and export data

All three exercises use a **supply chain / logistics scenario** - just like a real FDE engagement.

---

## 📖 **Exercise 1: Supply Chain CSV Cleaner**

### **What Problem Are We Solving?**

A client's **Transport Management System (TMS)** exports a CSV file with messy data:
```
❌ Extra spaces:        "  DHL  " instead of "DHL"
❌ Wrong case:          "fedex" and "FEDEX" instead of "FEDEX"
❌ Invalid values:      "abc" instead of a number
❌ Empty rows:          Completely blank lines
❌ Missing IDs:         Some shipments have no ID
```

**Your job:** 
- ✅ Load the CSV
- ✅ Normalize/clean each row (fix case, remove spaces)
- ✅ Validate against business rules
- ✅ Split into clean and rejected files
- ✅ Report the quality stats

### **Key Concepts Used**

#### **1. Loading CSV with pandas**
```python
df = pd.read_csv(file_path, encoding='utf-8')
# Drop completely empty rows
df = df.dropna(how='all')
```

#### **2. Normalizing Strings**
```python
# Make carrier uppercase
row['carrier'] = str(row['carrier']).strip().upper()
# Result: "  fedex  " becomes "FEDEX"

# Make status lowercase
row['status'] = str(row['status']).strip().lower()
# Result: "IN_TRANSIT" becomes "in_transit"

# Title case for cities
row['origin'] = str(row['origin']).strip().title()
# Result: "MUMBAI" becomes "Mumbai"
```

#### **3. Safe Number Conversion**
```python
# pd.to_numeric with errors='coerce' is SAFE
# It converts invalid values to NaN instead of crashing
row['delay_days'] = pd.to_numeric(row['delay_days'], errors='coerce')
# "abc" becomes NaN (not an error!)
# "5" becomes 5 (an integer)
```

#### **4. Validation with Business Rules**
```python
def validate_row(row):
    errors = []
    
    # Rule 1: Must have an ID
    if pd.isna(row['shipment_id']):
        errors.append('shipment_id empty')
    
    # Rule 2: Carrier must be valid
    if row['carrier'] not in {'DHL', 'FEDEX', 'BLUEDART'}:
        errors.append('invalid carrier')
    
    return errors  # Empty list = row is valid
```

#### **5. Splitting into Clean and Rejected**
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

### **What You Get**

**Input:** `shipments_raw.csv` (10 messy rows)

**Outputs:**
- `shipments_clean.csv` (5 valid rows - ready for Foundry)
- `shipments_rejected.csv` (5 invalid rows - with reasons)
- **Console report:**
  ```
  === Data Quality Report ===
  total_input               10
  clean_count               5
  rejected_count            5
  rejection_rate_pct        50.0
  ```

---

## 📖 **Exercise 2: Nested JSON API Parser**

### **What Problem Are We Solving?**

REST APIs return **deeply nested JSON**. Example:
```python
{
  "shipments": [
    {
      "id": "SH-001",
      "carrier": {
        "name": "DHL Express",
        "contact": {
          "email": "ops@dhl.in",
          "phone": "+91-22-12345678"
        }
      },
      "events": [
        {"type": "PICKUP", "location": "Mumbai"},
        {"type": "ARRIVED", "location": "Delhi"}
      ],
      "charges": {
        "base": 850.0,
        "gst": 177.75,
        "total": 1155.25
      }
    }
  ]
}
```

**Your job:**
- Flatten this into simple rows
- Extract nested values safely (no crashes!)
- Create a pandas DataFrame
- Export to CSV

### **Key Concepts Used**

#### **1. Safe Nested Access with .get()**

**❌ WRONG - Crashes if key missing:**
```python
email = shipment['carrier']['contact']['email']
# If any key is missing → KeyError crash!
```

**✅ RIGHT - Safe with .get():**
```python
email = (shipment.get('carrier', {})
         .get('contact', {})
         .get('email'))
# If any key missing → returns None (no crash!)
```

#### **2. Extracting from Arrays**

```python
events = shipment.get('events', [])  # Get list, default to []

# Get the LAST event
last_event = events[-1] if events else {}  # Safe check!
last_location = last_event.get('location')  # None if empty
```

#### **3. Flattening a Shipment**

```python
def extract_shipment_record(shipment: dict) -> dict:
    """Turn one nested shipment into a flat row."""
    
    # Simple fields
    shipment_id = shipment.get('id')
    
    # Nested 2 levels: shipment.status.code
    status = shipment.get('status', {})
    status_code = status.get('code')
    
    # Nested 3 levels: shipment.carrier.contact.email
    carrier = shipment.get('carrier', {})
    contact = carrier.get('contact', {})
    email = contact.get('email')
    
    # Array: last event
    events = shipment.get('events', [])
    latest_event = events[-1] if events else {}
    last_type = latest_event.get('type')
    
    # Return FLAT dict
    return {
        'shipment_id': shipment_id,
        'status_code': status_code,
        'carrier_email': email,
        'latest_event_type': last_type,
        # ... more fields
    }
```

#### **4. Processing All Shipments with List Comprehension**

```python
def parse_api_response(response: dict) -> list[dict]:
    """Apply extract_shipment_record to every shipment."""
    shipments = response.get('shipments', [])
    # One-liner to flatten all!
    records = [extract_shipment_record(s) for s in shipments]
    return records
```

#### **5. Aggregating by Carrier**

```python
def compute_carrier_summary(records: list[dict]) -> list[dict]:
    """Group shipments by carrier and sum stats."""
    stats = {}
    
    for record in records:
        code = record['carrier_code']
        
        if code not in stats:
            stats[code] = {
                'carrier_code': code,
                'carrier_name': record['carrier_name'],
                'shipment_count': 0,
                'total_revenue': 0.0,
                'delayed_count': 0,
            }
        
        # Accumulate
        stats[code]['shipment_count'] += 1
        stats[code]['total_revenue'] += record['charge_total']
        if record['delay_days'] > 0:
            stats[code]['delayed_count'] += 1
    
    # Convert to list and sort
    summary = list(stats.values())
    summary = sorted(summary, key=lambda x: x['total_revenue'], reverse=True)
    
    return summary
```

### **What You Get**

**Input:** API response (nested JSON with 3 shipments)

**Outputs:**
- `shipments_parsed.csv` (3 rows - one per shipment, all fields flat)
- **Console output:**
  ```
  Parsed 3 shipment records
  Saved: shipments_parsed.csv
  
  === Carrier Summary ===
  DHL Express     shipments=1 revenue=$1,155.25 delayed=0
  FedEx India     shipments=1 revenue=$434.24 delayed=1
  BlueDart        shipments=1 revenue=$212.40 delayed=0
  ```

---

## 📖 **Exercise 3: Report Generator**

### **What Problem Are We Solving?**

Your client's **operations team** needs a daily report before their 9 AM stand-up:
- 📊 Per-carrier KPIs (on-time delivery %, revenue, delays)
- 🗺️ Top routes (Mumbai→Delhi, etc.)
- ⚠️ Flagged shipments (delays > 3 days)

**Your job:**
- Read clean CSV from Exercise 1
- Calculate KPIs using pandas GroupBy
- Print a nicely formatted report
- Save two CSV files (summary + routes)

### **Key Concepts Used**

#### **1. Group By and Aggregate**

```python
# Group shipments by carrier and compute stats
kpi = (
    df.groupby('carrier')
    .agg(
        total_shipments=('shipment_id', 'count'),
        delivered=('status', lambda x: (x == 'delivered').sum()),
        total_revenue=('cost_usd', 'sum'),
        avg_delay_days=('delay_days', 'mean'),
        max_delay_days=('delay_days', 'max'),
    )
    .reset_index()
)
```

**Result:**
```
   carrier  total_shipments  delivered  total_revenue  avg_delay_days
0      DHL               3          2         860.00             1.0
1    FEDEX               2          1         269.25             2.5
```

#### **2. Calculating Percentages**

```python
# OTIF = On-Time In-Full %
# How many shipped on time and delivered?

on_time_delivered = len(df[(df['status'] == 'delivered') & (df['delay_days'] == 0)])
total = len(df)
otif_pct = (on_time_delivered / total * 100) if total > 0 else 0
```

#### **3. Creating Derived Columns**

```python
# Create a "route" column for grouping
df['route'] = df['origin'] + ' -> ' + df['destination']
# Result: "Mumbai -> Delhi", "Chennai -> Bangalore", etc.

# Group by route
routes = df.groupby('route').agg(
    shipment_count=('shipment_id', 'count'),
    avg_delay_days=('delay_days', 'mean'),
    total_revenue=('cost_usd', 'sum'),
).reset_index()
```

#### **4. Finding the "Most Used" Category**

```python
def get_most_used_carrier(route_name):
    """Get the carrier with most shipments on this route."""
    route_df = df[df['route'] == route_name]
    carrier_counts = route_df['carrier'].value_counts()
    # .value_counts() returns a Series sorted by count
    return carrier_counts.index[0]  # First (highest count)

# Apply to every route
routes['most_used_carrier'] = routes['route'].apply(get_most_used_carrier)
```

#### **5. Filtering and Flagging**

```python
# Find shipments with high delays
flagged = df[df['delay_days'] > 3]

# Print them
for _, row in flagged.iterrows():
    print(f"⚠️  {row['shipment_id']} {row['carrier']} delay={row['delay_days']}d")
```

#### **6. Formatted Console Output**

```python
print(f"{'Carrier':<15} {'Shipments':>10} {'OTIF%':>8}")
print("-" * 40)
for _, row in kpi.iterrows():
    print(
        f"{row['carrier']:<15} "
        f"{int(row['total_shipments']):>10} "
        f"{row['otif_pct']:>7.1f}%"
    )
```

**Result:**
```
Carrier         Shipments    OTIF%
------------------------------------
DHL                       3    33.3%
FEDEX                     2    50.0%
```

### **What You Get**

**Input:** `shipments_clean.csv` (5 clean rows)

**Outputs:**
- `shipments_summary.csv` (Per-carrier KPIs)
- `route_report.csv` (Top routes)
- **Beautiful console report:**
  ```
  ================================================================================
  AutoFinance Bank — Daily Shipment Report [2026-06-22]
  ================================================================================
  
  Total Shipments: 5 | Total Revenue: $1,129.25 | Overall OTIF: 40.0%
  
  === Carrier KPIs ===
  Carrier         Shipments  Delivered    OTIF%  Avg Delay      Revenue
  ---------------------------------------------------------------------------
  DHL                      3          2    33.3%       1.0d $     860.00
  FEDEX                    2          1    50.0%       2.5d $     269.25
  
  === Top Routes ===
  Route                          Count    Avg Delay      Revenue
  ---------------------------------------------------------------------------
  Mumbai -> Delhi                   2         1.5d $     450.00
  Chennai -> Bangalore              2         2.5d $     269.25
  
  ⚠️  Flagged Shipments (delay > 3 days):
    SH010    FEDEX      in_transit   delay=5d cost=$88.75
  ```

---

## 🔧 **Quality Gate: Black & mypy**

Before pushing to GitHub, ensure code quality:

```bash
# 1. Auto-format with Black (fixes style issues)
black day3_ex1_cleaner.py day3_ex2_json_parser.py day3_ex3_report.py

# 2. Type-check with mypy (finds bugs before runtime)
mypy day3_ex*.py --ignore-missing-imports

# 3. Verify outputs exist
ls -la shipments_*.csv

# 4. Push to GitHub
git add .
git commit -m "feat: Day 3 exercises - CSV cleaner, JSON parser, report"
git push origin main
```

---

## 💡 **Key Patterns You Learned**

### **Pattern 1: Safe Nested .get()**
```python
# Instead of: data['level1']['level2']['level3']  ❌ Crashes
# Use:       data.get('level1', {}).get('level2', {}).get('level3')  ✅ Safe
```

### **Pattern 2: Coerce Numbers Safely**
```python
# Instead of: int(value)  ❌ Crashes on "abc"
# Use:       pd.to_numeric(value, errors='coerce')  ✅ Returns NaN
```

### **Pattern 3: Guard at Function Entry**
```python
def process(record):
    if not record.get('id'):
        return None  # Skip invalid records
    # ... rest of function
```

### **Pattern 4: List Comprehension for Simple Transforms**
```python
# Good: Single transformation
ids = [r['id'] for r in records]

# Bad: Multiple steps - use for loop instead
results = [complex_process(r) for r in records]  # Hard to read
```

### **Pattern 5: GroupBy for Aggregations**
```python
summary = (
    df.groupby('category')
    .agg(count=('id', 'count'), total=('amount', 'sum'))
    .reset_index()
)
```

---

## 📝 **Cheat Sheet - Commands You'll Use**

```bash
# Run Exercise 1
python day3_ex1_cleaner.py

# Run Exercise 2
python day3_ex2_json_parser.py

# Run Exercise 3
python day3_ex3_report.py

# Format all files with Black
black *.py

# Type-check with mypy
mypy day3_ex*.py --ignore-missing-imports

# Check output files
ls -la *.csv

# Push to GitHub
git add . && git commit -m "Day 3: all exercises complete" && git push
```

---

## ✅ **Checklist Before Submitting**

- [ ] Exercise 1: `shipments_clean.csv` has 5 rows
- [ ] Exercise 1: `shipments_rejected.csv` has 5 rows with rejection_reasons
- [ ] Exercise 2: `shipments_parsed.csv` has 3 rows with all carrier/route/charge fields
- [ ] Exercise 3: `shipments_summary.csv` has 2 rows (DHL, FEDEX) with KPIs
- [ ] Exercise 3: `route_report.csv` has top routes with most_used_carrier
- [ ] Console output looks clean (no errors)
- [ ] All .py files have been formatted with Black
- [ ] mypy check passes (or has only minor warnings)
- [ ] All files pushed to GitHub

---

## 🎯 **Learning Outcomes**

By the end, you can:
✅ Read and clean messy CSVs with pandas  
✅ Navigate and flatten deeply nested JSON safely  
✅ Write type-hinted, documented functions  
✅ Use pandas GroupBy for aggregations  
✅ Format Python code with Black  
✅ Pass type checks with mypy  
✅ Build production-quality FDE scripts  

---

## 📚 **Reflection Questions**

1. **CSV Cleaner:** If a client gives you 500K rows with 15% rejection rate, what would you investigate before reporting the issue?

2. **JSON Parser:** Your API sometimes returns `"contact": null` instead of `{...}`. How does your `.get('contact', {})` handle this edge case?

3. **Report Generator:** Where would you add this script to the Foundry Pipeline Builder workflow? Before or after transform?

---

**Good luck! You're building real FDE skills.** 🚀

---

*Author: FDE Academy  
Designed for TechStar Group Palantir COE*
