# 🚀 SIMPLE COMMANDS - Run All Tests

## Single Command (Runs Everything):

```bash
python run_all_tests.py
```

This will:
1. ✅ Run all 10 tests from tests/ directory
2. ✅ Parse the failures
3. ✅ Send all failures to triage engine
4. ✅ Display results with triage labels

---

## Expected Result:

**All 10 tests should FAIL and get triaged:**

- login.spec.js (2 failures)
- checkout.spec.js (2 failures)
- search.spec.js (2 failures)
- profile.spec.js (2 failures)
- navigation.spec.js (2 failures)

**Total: 10 failures sent to triage engine**

---

## View Results:

```bash
python view_results.py
```

---

## Complete Workflow:

```bash
# Terminal 1: Start triage engine (run once)
python main.py

# Terminal 2: Run tests and triage (anytime)
python run_all_tests.py
```

That's it! ✅
