# Running Playwright Tests - Command Reference

## 📁 Test Files Created

```
c:\bug-triage-engine\tests\
├── login.spec.js       # Login & authentication tests (4 tests, 2 will fail)
├── checkout.spec.js    # E-commerce checkout flow (6 tests, 3 will fail)
├── search.spec.js      # Search & filters (5 tests, 3 will fail)
├── profile.spec.js     # User profile management (6 tests, 3 will fail)
└── navigation.spec.js  # Site navigation & menus (7 tests, 4 will fail)
```

**Total: 28 tests across 5 files (15 will fail for triage testing)**

---

## 🚀 Commands to Run Tests

### Run Individual Test Files

```bash
# Run login tests only
npx playwright test tests/login.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py

# Run checkout tests only
npx playwright test tests/checkout.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py

# Run search tests only
npx playwright test tests/search.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py

# Run profile tests only
npx playwright test tests/profile.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py

# Run navigation tests only
npx playwright test tests/navigation.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py
```

---

### Run All Tests at Once

```bash
# Run all tests in tests/ directory
npx playwright test tests/ --reporter=json > playwright-report.json
python demo_playwright_failures.py
```

---

### Run Multiple Specific Files

```bash
# Run login and checkout tests
npx playwright test tests/login.spec.js tests/checkout.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py

# Run search and navigation tests
npx playwright test tests/search.spec.js tests/navigation.spec.js --reporter=json > playwright-report.json
python demo_playwright_failures.py
```

---

### Run Tests with Filters

```bash
# Run only tests with "fail" in the name
npx playwright test tests/ --grep "fail" --reporter=json > playwright-report.json
python demo_playwright_failures.py

# Run tests from specific describe block
npx playwright test tests/login.spec.js --grep "Login Functionality" --reporter=json > playwright-report.json
python demo_playwright_failures.py
```

---

## 🔧 Alternative: Use Playwright Config

Update `playwright.config.js` to use JSON reporter by default:

```javascript
module.exports = {
  reporter: [
    ['list'],
    ['json', { outputFile: 'playwright-report.json' }]
  ],
  // ... other config
};
```

Then simply run:

```bash
# Run any test - JSON report is automatic
npx playwright test tests/login.spec.js
python demo_playwright_failures.py

# Run all tests
npx playwright test
python demo_playwright_failures.py
```

---

## 📊 View Triage Results

After running tests and triaging:

```bash
# View latest triage result
python view_results.py

# View all triage results
python view_results.py all
```

---

## 🎯 Quick Test Workflow

**Complete workflow in 3 commands:**

```bash
# 1. Start triage engine (in one terminal)
python main.py

# 2. Run tests and triage (in another terminal)
npx playwright test tests/ --reporter=json > playwright-report.json
python demo_playwright_failures.py

# 3. View results
python view_results.py
```

---

## 💡 Pro Tips

### Run Specific Test by Name

```bash
# Run only the "should fail - incorrect password" test
npx playwright test tests/login.spec.js --grep "incorrect password" --reporter=json > playwright-report.json
```

### Run in Headed Mode (See Browser)

```bash
# Watch tests run in browser
npx playwright test tests/login.spec.js --headed --reporter=json > playwright-report.json
```

### Run in Debug Mode

```bash
# Debug tests step-by-step
npx playwright test tests/login.spec.js --debug
```

### Parallel Execution

```bash
# Run tests in parallel (faster)
npx playwright test tests/ --workers=4 --reporter=json > playwright-report.json
```

---

## 📝 Expected Triage Labels

Based on the test files, you should see these labels:

**Login Tests:**
- "Assertion: Text Mismatch"
- "Assertion: Element Not Visible"

**Checkout Tests:**
- "Assertion: Text Mismatch"
- "Assertion: Element Not Disabled"
- "Assertion: Count Mismatch"

**Search Tests:**
- "Assertion: URL Mismatch"
- "Assertion: Element Not Visible"
- "Assertion: Count Mismatch"

**Profile Tests:**
- "Assertion: Element Not Visible"
- "Assertion: Element Not Enabled"
- "Assertion: Title Mismatch"

**Navigation Tests:**
- "Assertion: Element Not Visible"
- "Assertion: Count Mismatch"
- "Assertion: Text Mismatch"
- "Assertion: URL Mismatch"

---

## 🔄 Continuous Testing

Set up a watch mode for continuous testing:

```bash
# Watch for file changes and re-run tests
npx playwright test tests/ --reporter=json --watch
```

Then manually run triage when tests complete:

```bash
python demo_playwright_failures.py
```
