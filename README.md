## Day 3 FDE Academy Exercises - My Completion

This folder contains my completed exercises for FDE Academy Day 3.

**My Work:**
- day3_ex1_cleaner.py - CSV data cleaning
- day3_ex2_json_parser.py - JSON API response parsing
- day3_ex3_report.py - KPI report generation
- All CSV output files

**Reference Materials:** The other markdown files are guides provided to help me learn.

🎯 DAY 3 PYTHON FUNDAMENTALS - COMPLETE SOLUTION

## 📋 What You Have

✅ **3 Complete Working Exercises** with full explanations  
✅ **Complete Guide** with detailed step-by-step explanations  
✅ **All Code Formatted** with Black (production-ready)  
✅ **Sample Data Files** ready to test immediately  

---

## 📂 Files Included

```
day3_ex1_cleaner.py          ← Exercise 1: CSV Cleaner
day3_ex2_json_parser.py      ← Exercise 2: JSON Parser  
day3_ex3_report.py           ← Exercise 3: Report Generator
DAY3_COMPLETE_GUIDE.md       ← Detailed explanations (READ THIS!)
```

---

## 🚀 Quick Start (5 Minutes)

### **Step 1: Copy the sample data file**
```bash
# Create shipments_raw.csv with messy test data
cat > shipments_raw.csv << 'EOF'
shipment_id,carrier,status,origin,destination,delay_days,cost_usd
SH001,DHL ,	in_transit	, MUMBAI, DELHI, 2, 250.00
SH002, fedex,DELIVERED,Chennai,Bangalore,0,180.50
SH003,bluedart,	IN_TRANSIT,Pune,	Hyderabad ,abc,320.00
,DHL,in_transit,Mumbai,Delhi,1,90.00
SH005,FEDEX,unknown_status,Chennai,Mumbai,3,75.00
SH006,dhl,delivered,DELHI,mumbai,0,410.00
SH007,,in_transit,Bangalore,Chennai,2,
SH008,BlueDart,IN_TRANSIT,Hyderabad,Pune,-1,155.00
SH009,DHL,delivered,Mumbai,Delhi,1,200.00
SH010,FedEx,in_transit,Chennai,Bangalore,5,88.75
EOF
```

### **Step 2: Run the exercises**
```bash
# Exercise 1: Clean the messy CSV
python day3_ex1_cleaner.py

# Exercise 2: Parse nested JSON
python day3_ex2_json_parser.py

# Exercise 3: Generate report
python day3_ex3_report.py
```

### **Step 3: Check the outputs**
```bash
# Clean data ready for Foundry
cat shipments_clean.csv

# Rejected records with reasons
cat shipments_rejected.csv

# Parsed API response
cat shipments_parsed.csv

# Summary KPIs
cat shipments_summary.csv
```

---

## 📖 How to Use This Solution

### **If you want to UNDERSTAND the code:**
1. **Read `DAY3_COMPLETE_GUIDE.md`** first (15 minutes)
   - Explains each concept clearly
   - Shows examples and patterns
   - Includes all key ideas

2. **Then read the Python files** in this order:
   - `day3_ex1_cleaner.py` (simpler, foundational)
   - `day3_ex2_json_parser.py` (medium, nested structures)
   - `day3_ex3_report.py` (advanced, complex logic)

### **If you want to COPY and MODIFY:**
1. Copy the entire `day3_ex1_cleaner.py` to your project
2. Adapt the business rules (VALID_STATUSES, VALID_CARRIERS)
3. Modify input/output file paths
4. Run `black your_file.py` to format
5. Run `mypy your_file.py --ignore-missing-imports` to type-check

### **If you want to SUBMIT to GitHub:**
```bash
# Copy files to your Day 3 folder
cp day3_ex*.py ~/my-fde-academy/day3/

# Format with Black
black ~/my-fde-academy/day3/day3_ex*.py

# Commit
cd ~/my-fde-academy
git add day3/
git commit -m "feat: Day 3 exercises - CSV cleaner, JSON parser, report generator"
git push origin main
```

---

## 🎓 What Each Exercise Teaches

### **Exercise 1: CSV Cleaner** 
**Teaches:** pandas, string normalization, validation, data quality

**Real-world scenario:** First day at logistics company - ops team gives you messy TMS export

**Key skills:**
- ✅ Read CSV with pandas
- ✅ Clean strings (strip, upper, lower, title)
- ✅ Safe number conversion (pd.to_numeric)
- ✅ Validate against business rules
- ✅ Split into clean/rejected
- ✅ Generate quality report

**Time:** 45 minutes  
**Difficulty:** ⭐ Beginner

---

### **Exercise 2: JSON Parser**
**Teaches:** nested dictionaries, list comprehensions, safe access patterns

**Real-world scenario:** Pull tracking data from logistics carrier API, flatten it for Foundry

**Key skills:**
- ✅ Navigate deeply nested JSON safely (.get() chains)
- ✅ Handle missing values without crashes
- ✅ Extract from lists (get last event, etc.)
- ✅ Write fully typed and documented functions
- ✅ Use list comprehensions for transforms
- ✅ Group and aggregate data

**Time:** 45 minutes  
**Difficulty:** ⭐⭐ Intermediate

---

### **Exercise 3: Report Generator**
**Teaches:** pandas GroupBy, aggregations, formatting, multi-file output

**Real-world scenario:** Build daily report for client's 9 AM operations stand-up

**Key skills:**
- ✅ Use pandas GroupBy for aggregations
- ✅ Calculate KPIs (OTIF%, avg delay, revenue)
- ✅ Create derived columns
- ✅ Format console output with f-strings
- ✅ Save multiple CSV outputs
- ✅ Design clean, separable functions

**Time:** 60 minutes  
**Difficulty:** ⭐⭐⭐ Advanced

---

## 📚 Learning Path

### **If you're NEW to Python:**
1. Read `DAY3_COMPLETE_GUIDE.md` - understand concepts first
2. Run the exercises - see them work
3. Modify one function at a time - learn by changing
4. Write your own version from scratch

### **If you know Python but not pandas:**
1. Skim the guide for pandas examples
2. Study `day3_ex1_cleaner.py` - pandas basics
3. Then move to `day3_ex3_report.py` - GroupBy/aggregations

### **If you know Python and pandas:**
1. Read the guide quickly
2. Review the code for patterns
3. Focus on: safe nested access, type hints, docstrings
4. Consider: how would you scale to 1M rows?

---

## 🔍 Key Code Patterns Explained

### **Pattern 1: Safe Nested Access**
```python
# ❌ WRONG - Crashes if key is missing
value = shipment['carrier']['contact']['email']

# ✅ RIGHT - Safe, returns None if missing
value = (shipment.get('carrier', {})
         .get('contact', {})
         .get('email'))
```

### **Pattern 2: Safe Number Conversion**
```python
# ❌ WRONG - Crashes on "abc"
number = int(value)

# ✅ RIGHT - Returns NaN, no crash
number = pd.to_numeric(value, errors='coerce')
```

### **Pattern 3: Guard at Entry**
```python
def process(record):
    # Return None early if invalid
    if not record.get('id'):
        return None
    # Rest of function only runs for valid records
    return result
```

### **Pattern 4: GroupBy Aggregation**
```python
summary = (
    df.groupby('column')
    .agg(
        count=('id', 'count'),
        total=('amount', 'sum'),
        average=('amount', 'mean'),
    )
    .reset_index()
)
```

### **Pattern 5: List Comprehension**
```python
# ✅ Good for single transformation
ids = [r['id'] for r in records]

# ❌ Bad for multiple steps - use for loop
processed = [complex_func(r) for r in records]
```

---

## 🛠️ Tools Used

| Tool | Purpose | Command |
|------|---------|---------|
| **pandas** | Read/write CSV, GroupBy, aggregations | `import pandas as pd` |
| **Black** | Auto-format Python code | `black file.py` |
| **mypy** | Type checking | `mypy file.py` |
| **json** | Parse JSON | `import json` |
| **pathlib** | File paths | `from pathlib import Path` |

---

## 🚨 Common Issues & Fixes

### **Issue: FileNotFoundError for shipments_raw.csv**
```bash
# Make sure you create the file first!
cat > shipments_raw.csv << 'EOF'
... paste CSV content ...
EOF
```

### **Issue: pandas.to_numeric says 'NaN' is invalid**
```python
# Use errors='coerce' to safely convert
value = pd.to_numeric(value, errors='coerce')  # ✅ Works
value = pd.to_numeric(value)  # ❌ Crashes on "abc"
```

### **Issue: mypy errors about None**
```python
# This is GOOD - it found a potential bug!
# Fix by adding explicit None checks:
if value is not None:
    result = some_operation(value)
else:
    result = default_value
```

### **Issue: Black changes my formatting**
```bash
# This is expected - Black enforces PEP 8
# Just run it and commit the changes
black file.py
git add file.py
git commit -m "style: Black formatting"
```

---

## ✅ Verification Checklist

Before submitting, verify:

- [ ] Exercise 1 creates `shipments_clean.csv` with 5 rows
- [ ] Exercise 1 creates `shipments_rejected.csv` with 5 rows
- [ ] Exercise 2 creates `shipments_parsed.csv` with 3 rows
- [ ] Exercise 3 creates `shipments_summary.csv` (per-carrier)
- [ ] Exercise 3 creates `route_report.csv` (per-route)
- [ ] All code is formatted with Black (0 changes needed)
- [ ] All files are pushed to GitHub
- [ ] Console output shows no errors

---

## 📞 Getting Help

### **I don't understand pandas GroupBy**
→ Read "Pattern 4" above, then `DAY3_COMPLETE_GUIDE.md`

### **My code crashes on None values**
→ Use `.get()` with defaults, not direct `dict['key']` access

### **Black is changing my code**
→ This is GOOD - it means your code will match TechStar standards

### **mypy says my types are wrong**
→ Add explicit None checks, or use `Optional[Type]` in type hints

---

## 🎯 Next Steps

After completing Day 3:

1. ✅ Commit all code to GitHub
2. ✅ Read the reflection questions in the guide
3. ✅ Think about: how would you handle 1M rows? Streaming?
4. ✅ Move to Day 4: Python OOP, Pydantic, Exception Handling

---

## 📚 Additional Resources

- **PEP 8 Style Guide:** https://pep8.org/
- **pandas Documentation:** https://pandas.pydata.org/docs/
- **Python typing:** https://docs.python.org/3/library/typing.html
- **Black formatter:** https://black.readthedocs.io/

---

## 📝 Summary

You now have:
- ✅ 3 production-ready Python scripts
- ✅ Complete understanding of data cleaning, JSON parsing, reporting
- ✅ Real-world FDE engagement patterns
- ✅ Code formatted with Black (professional standard)
- ✅ Full type hints and docstrings

**Time to master:** 150 minutes (2.5 hours)  
**Effort level:** Medium - good mix of concepts  
**Real-world applicable:** YES - use this in every client engagement  

---

**Good luck! You're building real FDE skills.** 🚀

*FDE Academy - TechStar Group Palantir COE*
