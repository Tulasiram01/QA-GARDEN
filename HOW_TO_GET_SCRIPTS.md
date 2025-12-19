# How to Get Playwright Scripts from Scripter

## 📝 Simple Explanation

When a QA/DevOps person writes Playwright tests, they need to give you the script so the triage engine can create clickable links to the exact failing line.

---

## 🔧 Two Ways to Get Scripts

### **Method 1: Manual (Simple)**

**QA/DevOps sends you the script file directly:**

1. QA writes test: `login.spec.js`
2. QA sends you the file (email, Slack, shared drive)
3. You save it to: `c:\bug-triage-engine\tests\login.spec.js`
4. Run tests: `python run_all_tests.py`
5. Triage engine creates clickable link: `file:///c:/bug-triage-engine/tests/login.spec.js#L25`

**That's it!** The file is local, so the link works.

---

### **Method 2: API (Automated)**

**QA/DevOps hosts scripts on a server, you fetch via API:**

#### **Step 1: QA Sets Up Script Server**

QA runs a simple HTTP server that serves Playwright scripts:

```bash
# QA runs this on their machine or server
python playwright_script_server.py
```

This starts a server at: `http://qa-machine:8005`

#### **Step 2: QA Provides Script URL**

When QA runs tests, they include the script endpoint:

```json
{
  "test_name": "login test",
  "file_path": "login.spec.js",
  "playwright_script_endpoint": "http://qa-machine:8005/api/scripts/login.spec.js"
}
```

#### **Step 3: You Fetch the Script (Optional)**

Your triage engine can fetch the script content:

```bash
# Get script info
curl http://qa-machine:8005/api/scripts/login.spec.js

# Download script
curl http://qa-machine:8005/api/scripts/login.spec.js/download
```

#### **Step 4: Triage Engine Stores the Link**

The triage result includes the endpoint:

```json
{
  "playwright_script": "file:///local/path/login.spec.js#L25",
  "playwright_script_endpoint": "http://qa-machine:8005/api/scripts/login.spec.js"
}
```

---

## 🎯 Which Method to Use?

| Scenario | Method | Why |
|----------|--------|-----|
| **Small team, same machine** | Manual | Simplest - just copy files |
| **Remote QA team** | API | QA keeps scripts on their server |
| **CI/CD pipeline** | API | Automated - no manual file transfer |
| **Quick testing** | Manual | Fastest setup |

---

## 💡 Real-World Example

### **Scenario: Remote QA Team**

**QA (on their machine):**
```bash
# 1. Write test
# tests/checkout.spec.js

# 2. Start script server
python playwright_script_server.py
# Server running at http://192.168.1.100:8005

# 3. Run tests with endpoint
npx playwright test tests/checkout.spec.js
```

**You (on your machine):**
```bash
# 1. QA sends you the test failure JSON with endpoint:
# {
#   "playwright_script_endpoint": "http://192.168.1.100:8005/api/scripts/checkout.spec.js"
# }

# 2. Your triage engine processes it
python run_all_tests.py

# 3. Result includes both local and remote links
# Local: file:///c:/bug-triage-engine/tests/checkout.spec.js#L42
# Remote: http://192.168.1.100:8005/api/scripts/checkout.spec.js
```

---

## 📌 Summary

**Manual = QA sends you files, you save them locally**
**API = QA runs script server, you fetch via HTTP**

**For most cases, Manual is easier!** Just have QA send you the `.spec.js` files and save them in your `tests/` folder.

The API method is only needed if:
- QA is remote and can't share files easily
- You're integrating with CI/CD
- You want automated script fetching
