# Run All Tests - Quick Reference

## 📊 Simplified Test Structure

```
tests/
├── login.spec.js       (2 tests - both will fail)
├── checkout.spec.js    (2 tests - both will fail)
├── search.spec.js      (2 tests - both will fail)
├── profile.spec.js     (2 tests - both will fail)
└── navigation.spec.js  (2 tests - both will fail)

Total: 10 tests across 5 files (all will fail for triage testing)
```

---

## 🚀 Run All Tests at Once

### Single Command to Run Everything:

```bash
npx playwright test tests/ --reporter=json > playwright-report.json && python demo_playwright_failures.py
```

This will:
1. Run all 10 tests from all 5 files
2. Generate JSON report
3. Automatically send failures to triage engine
4. Display results with triage labels

---

## 📋 Step-by-Step

If you prefer to run separately:

```bash
# Step 1: Run all tests
npx playwright test tests/ --reporter=json > playwright-report.json

# Step 2: Triage failures
python demo_playwright_failures.py

# Step 3: View results
python view_results.py
```

---

## 🎯 Expected Results

**All 10 tests will fail with these labels:**

1. **login.spec.js**
   - "Assertion: Title Mismatch"
   - "Assertion: Element Not Visible"

2. **checkout.spec.js**
   - "Assertion: Text Mismatch"
   - "Assertion: Element Not Enabled"

3. **search.spec.js**
   - "Assertion: URL Mismatch"
   - "Assertion: Count Mismatch"

4. **profile.spec.js**
   - "Assertion: Element Not Visible"
   - "Assertion: Title Mismatch"

5. **navigation.spec.js**
   - "Assertion: Element Not Visible"
   - "Assertion: Count Mismatch"

---

## ⚡ Quick Workflow

**Complete workflow in 2 commands:**

```bash
# Terminal 1: Start triage engine
python main.py

# Terminal 2: Run all tests and triage
npx playwright test tests/ --reporter=json > playwright-report.json && python demo_playwright_failures.py
```

Done! View results with `python view_results.py`
