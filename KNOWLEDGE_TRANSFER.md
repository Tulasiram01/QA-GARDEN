# Bug Triage Engine - Knowledge Transfer (KT)

## 📋 What This System Does

**Automatically converts Playwright test failures into professional bug reports using AI**

**Input:** Failed test  
**Output:** Complete bug report with title, description, error location, and category label

**Time Saved:** 10-15 minutes → 30 seconds per bug

---

## 🏗️ System Components

### **1. Triage Engine (Port 8003)**
- Main service that coordinates everything
- Receives test failures and returns bug reports

### **2. BERT Server (Port 8001)**
- Classifies errors into categories
- Trained on 30,000 bug reports (27K training + 3K validation)
- Examples: "Assertion: Title Mismatch", "Timeout Error"

### **3. Ollama LLM (Port 11434)**
- Generates human-readable bug descriptions
- Uses Gemma:2b model
- Creates 160-220 word professional explanations

### **4. Test Runner**
- Runs Playwright tests
- Sends failures to triage engine
- Displays results

---

## 🚀 How to Start the System

**You need 3 terminals:**

**Terminal 1: Start Triage Engine**
```
python main.py
```

**Terminal 2: Start BERT Server**
```
python bert_server.py
```

**Terminal 3: Run Tests**
```
python run_all_tests.py
```

**View Results:**
```
python view_results.py
```

---

## 📁 Important Files

### **Main Scripts:**
- `main.py` - Starts triage engine
- `bert_server.py` - Starts BERT classification server
- `run_all_tests.py` - Runs all tests and triages failures
- `view_results.py` - Shows triage results

### **Test Files:**
- `tests/login.spec.js` - Login tests
- `tests/checkout.spec.js` - Checkout tests
- `tests/search.spec.js` - Search tests
- `tests/profile.spec.js` - Profile tests
- `tests/navigation.spec.js` - Navigation tests

### **Results:**
- `processed/*.json` - Stored bug reports

---

## 🎯 How It Works (Simple Flow)

1. **Run Tests** → Playwright tests execute
2. **Tests Fail** → Failures captured in JSON report
3. **Parse Failures** → Extract error details
4. **BERT Classifies** → Assigns category label
5. **Ollama Describes** → Generates bug description
6. **Save Result** → Stores complete bug report
7. **View Results** → Display via CLI or API

---

## 🔑 Key Concepts

### **BERT Classification**
- Uses your 30K trained model
- Analyzes error patterns
- Returns intelligent labels
- Examples: "Assertion: Element Not Visible", "Network Error"

### **Ollama Description**
- AI-powered text generation
- Explains what happened
- Suggests root cause
- Describes impact

### **Triage Labels**
Common labels you'll see:
- Assertion: Title Mismatch
- Assertion: Element Not Visible
- Assertion: URL Mismatch
- Assertion: Text Mismatch
- Assertion: Count Mismatch
- Timeout Error
- Network Error

---

## 🐛 Common Issues & Solutions

### **Issue 1: BERT Connection Failed**
**Problem:** "Failed to establish a new connection"  
**Solution:** 
- Check BERT server is running in Terminal 2
- Restart: Stop (Ctrl+C) and run `python bert_server.py` again

### **Issue 2: Shows Wrong Test Files**
**Problem:** Shows `demo.spec.js` instead of test files  
**Solution:**
- Delete old report file: `playwright-report.json`
- Use `python run_all_tests.py` (not demo_playwright_failures.py)

### **Issue 3: Ollama Timeout**
**Problem:** Takes too long or times out  
**Solution:**
- Check Ollama is running
- Verify Gemma:2b model is installed
- Wait up to 5 minutes for first request

### **Issue 4: No Failures Found**
**Problem:** "No failures found (all tests passed)"  
**Solution:**
- Tests might actually be passing
- Check test files are designed to fail
- Run tests manually to verify: `npx playwright test tests/`

---

## 📊 What You Get in Results

Each bug report includes:
- **Title** - Short description of the issue
- **Description** - Detailed 160-220 word explanation
- **Error Line** - Exact line number where it failed
- **File Path** - Which test file failed
- **Clickable Link** - Jump directly to failing code
- **Triage Label** - Category/type of error
- **Test URL** - Which page was being tested
- **Timestamp** - When it was triaged

---

## 🎓 For New Team Members

### **First Time Setup:**
1. Install Python 3.x
2. Install Node.js and Playwright
3. Install Ollama with Gemma:2b model
4. Clone the repository

### **Daily Usage:**
1. Start all 3 services (Terminals 1, 2, 3)
2. Run tests: `python run_all_tests.py`
3. View results: `python view_results.py`
4. Check `processed/` folder for stored reports

### **Understanding the Output:**
- Each test failure gets its own bug report
- Reports are stored as JSON files
- View latest with `python view_results.py`
- View all with `python view_results.py all`

---

## 🔧 Configuration

### **Network Addresses:**
- Triage Engine: `192.168.1.13:8003`
- BERT Server: `192.168.1.13:8001`
- Ollama: `localhost:11434`

### **Timeouts:**
- Triage API: 5 minutes
- BERT: 10 seconds
- Playwright: 5 seconds per test

---

## 📈 Performance

- **Average Time:** 30-60 seconds per bug report
- **BERT Response:** Under 1 second
- **Ollama Response:** 20-40 seconds
- **Storage:** ~5KB per report

---

## 🚧 Current Limitations

- No authentication (open access)
- File-based storage (not database)
- Processes one request at a time
- No automatic retry on failure
- Limited error logging

---

## 📞 Quick Reference

### **Start Everything:**
```
Terminal 1: python main.py
Terminal 2: python bert_server.py
Terminal 3: python run_all_tests.py
```

### **View Results:**
```
python view_results.py          # Latest result
python view_results.py all      # All results
```

### **Check What's Running:**
- Triage Engine: Should show "Uvicorn running on port 8003"
- BERT Server: Should show "Uvicorn running on port 8001"
- Ollama: Check separately with `ollama list`

---

## ✅ Quick Checklist

**Before Running Tests:**
- [ ] Triage Engine running (Terminal 1)
- [ ] BERT Server running (Terminal 2)
- [ ] Ollama running with Gemma:2b
- [ ] Test files exist in `tests/` folder

**After Running Tests:**
- [ ] Check terminal output for success/failure count
- [ ] View results with `python view_results.py`
- [ ] Check `processed/` folder for JSON files
- [ ] Verify triage labels are assigned

---

## 📚 Additional Documentation

- `HOW_TO_GET_SCRIPTS.md` - Getting test scripts from QA team
- `SIMPLE_COMMAND.md` - Quick command reference
- `RUN_ALL_TESTS.md` - Detailed testing guide

---

**Project Owner:** Tulasiram01  
**Repository:** QA-GARDEN  
**Location:** `c:\bug-triage-engine`

**Last Updated:** 2025-12-19
