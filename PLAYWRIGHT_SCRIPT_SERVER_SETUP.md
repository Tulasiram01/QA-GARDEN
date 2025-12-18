# Playwright Script Server Setup

## What is this?

A real, working API server that serves your Playwright test scripts via HTTP endpoints. This allows external services (like your triage engine) to retrieve and view test scripts programmatically.

## Quick Start

### Step 1: Start the Script Server

Open a **new terminal** and run:

```bash
cd c:\bug-triage-engine
python playwright_script_server.py
```

You should see:
```
================================================================================
Playwright Script Server
================================================================================
Starting server on http://localhost:8005
Serving scripts from: c:\bug-triage-engine

Available endpoints:
  - List all scripts:    http://localhost:8005/api/scripts
  - Get script info:     http://localhost:8005/api/scripts/demo.spec.js
  - Get script content:  http://localhost:8005/api/scripts/demo.spec.js/content
  - Download script:     http://localhost:8005/api/scripts/demo.spec.js/download
================================================================================
```

### Step 2: Test the Endpoints

**List all available scripts:**
```bash
curl http://localhost:8005/api/scripts
```

**Get script info:**
```bash
curl http://localhost:8005/api/scripts/demo.spec.js
```

**Get script content:**
```bash
curl http://localhost:8005/api/scripts/demo.spec.js/content
```

**Download script:**
```bash
curl http://localhost:8005/api/scripts/demo.spec.js/download -o downloaded_script.js
```

### Step 3: Run Your Tests

Now when you run `demo_playwright_failures.py`, it will automatically use the real script server endpoint:

```bash
python demo_playwright_failures.py
```

The `playwright_script_endpoint` field will be populated with:
```
http://localhost:8005/api/scripts/demo.spec.js
```

---

## API Endpoints

### 1. List All Scripts
**GET** `/api/scripts`

**Response:**
```json
{
  "total": 1,
  "scripts": [
    {
      "name": "demo.spec.js",
      "size": 1822,
      "endpoint": "http://localhost:8005/api/scripts/demo.spec.js"
    }
  ]
}
```

### 2. Get Script Info
**GET** `/api/scripts/{filename}`

**Example:** `http://localhost:8005/api/scripts/demo.spec.js`

**Response:**
```json
{
  "script_name": "demo.spec.js",
  "script_path": "c:\\bug-triage-engine\\demo.spec.js",
  "file_size": 1822,
  "exists": true,
  "endpoint_url": "http://localhost:8005/api/scripts/demo.spec.js",
  "download_url": "http://localhost:8005/api/scripts/demo.spec.js/download"
}
```

### 3. Get Script Content
**GET** `/api/scripts/{filename}/content`

**Example:** `http://localhost:8005/api/scripts/demo.spec.js/content`

**Response:**
```json
{
  "script_name": "demo.spec.js",
  "content": "const { test, expect } = require('@playwright/test');\n\n...",
  "file_size": 1822,
  "lines": 44
}
```

### 4. Download Script
**GET** `/api/scripts/{filename}/download`

**Example:** `http://localhost:8005/api/scripts/demo.spec.js/download`

Downloads the actual `.spec.js` file.

---

## Integration with Triage Engine

### How It Works

1. **Script Server** runs on port `8005` and serves your Playwright scripts
2. **Triage Engine** runs on port `8003` and processes test failures
3. When a test fails, `demo_playwright_failures.py` sends:
   ```json
   {
     "playwright_script_endpoint": "http://localhost:8005/api/scripts/demo.spec.js"
   }
   ```
4. Anyone viewing the triage result can click the endpoint to view/download the script

### Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  Terminal 1: Playwright Script Server (Port 8005)          │
│  python playwright_script_server.py                         │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ Serves scripts
                           │
┌─────────────────────────────────────────────────────────────┐
│  Terminal 2: Triage Engine API (Port 8003)                 │
│  python main.py                                              │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ Receives failures
                           │
┌─────────────────────────────────────────────────────────────┐
│  Terminal 3: Run Tests                                      │
│  python demo_playwright_failures.py                          │
│                                                              │
│  Sends:                                                      │
│  {                                                           │
│    "test_name": "...",                                       │
│    "playwright_script_endpoint":                            │
│      "http://localhost:8005/api/scripts/demo.spec.js"       │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Features

- **File Type Restriction**: Only `.spec.js` files are served
- **Directory Restriction**: Only serves files from the configured directory
- **No Path Traversal**: Prevents accessing files outside the scripts directory

---

## Configuration

Edit `playwright_script_server.py` to customize:

```python
# Change the port
PORT = 8005

# Change the scripts directory
SCRIPTS_DIR = "c:/path/to/your/scripts"
```

---

## Testing the Integration

### Full Test:

**Terminal 1:**
```bash
python playwright_script_server.py
```

**Terminal 2:**
```bash
python main.py
```

**Terminal 3:**
```bash
python demo_playwright_failures.py
```

**Terminal 4 (or browser):**
```bash
# Get the latest triage result
curl http://localhost:8003/api/triage/latest

# You should see:
# "playwright_script_endpoint": "http://localhost:8005/api/scripts/demo.spec.js"

# Now fetch the actual script
curl http://localhost:8005/api/scripts/demo.spec.js/content
```

---

## Summary

✅ **Real API server** - Not hardcoded, actual working endpoints  
✅ **Serves Playwright scripts** - Via HTTP API  
✅ **Multiple endpoints** - List, info, content, download  
✅ **Secure** - Only serves .spec.js files  
✅ **Integrated** - Works with your triage engine  

Now you have a complete system where test failures link to actual, retrievable Playwright scripts!
