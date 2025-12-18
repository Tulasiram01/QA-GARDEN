# Bug Triage Engine - Project Overview

## What This Project Does

An **AI-powered automated bug triage system** that analyzes Playwright test failures and generates detailed bug reports with:
- AI-generated bug titles and descriptions
- Clickable links to failing code lines
- Error analysis and root cause suggestions
- HTTP API for integration with CI/CD pipelines

---

## Key Features

### 🤖 AI-Powered Analysis
- **LLM Integration**: Uses Ollama (Gemma:2b) to generate human-readable bug descriptions
- **Smart Title Generation**: Detects Playwright assertion types and creates specific titles
  - Example: "Page title does not match expected value" instead of generic "Test failed"
- **Detailed Descriptions**: 160-220 word explanations with expected vs actual behavior, root cause, and impact

### 🔗 Playwright Integration
- **Clickable Script URLs**: `file:///path/to/test.spec.js#L25` - click to jump to exact line
- **Script Server**: HTTP API to view/download test scripts
- **Test URL Extraction**: Identifies which page was being tested
- **ANSI Code Stripping**: Removes color codes from error messages for clean output

### 📊 Intelligent Error Extraction
- **Multi-level Fallback**: Extracts error line numbers from stack trace → error message → logs → default
- **File Path Detection**: Prioritizes test files, filters out system files
- **Stack Trace Truncation**: Keeps relevant info, removes noise

### 🌐 RESTful API
- `POST /api/triage` - Submit test failures
- `GET /api/triage/latest` - Get most recent result
- `GET /api/triage` - Get all results
- `GET /api/triage/{id}` - Get specific result

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Playwright Tests (demo.spec.js)                            │
│  ↓ Fails → Generates playwright-report.json                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  demo_playwright_failures.py                                │
│  • Parses JSON report                                       │
│  • Strips ANSI codes                                        │
│  • Sends to triage API                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Triage Engine API (Port 8003)                              │
│  • Extracts error line & file path                          │
│  • Calls Ollama LLM for bug description                     │
│  • Generates clickable URLs                                 │
│  • Returns structured JSON                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Output: Structured Bug Report                              │
│  • Title: "Page title does not match expected value"        │
│  • Description: AI-generated explanation                    │
│  • Error Line: 13                                           │
│  • Script URL: file:///c:/tests/demo.spec.js#L13            │
│  • Test URL: https://example.com                            │
└─────────────────────────────────────────────────────────────┘
```

**Supporting Services:**
- **BERT Server** (Port 8001): Classification service for external integrations
- **Script Server** (Port 8005): HTTP API to serve Playwright test scripts
- **Ollama** (Port 11434): Local LLM for text generation

---

## Technology Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Testing**: Playwright (JavaScript)
- **AI/ML**: Ollama (Gemma:2b), BERT (optional)
- **Data**: Pydantic for validation, JSON for storage
- **HTTP**: Requests library

---

## Quick Start

### 1. Start Triage Engine
```bash
cd c:\bug-triage-engine
python main.py
```

### 2. Run Tests & Triage
```bash
python demo_playwright_failures.py
```

### 3. View Results
```bash
# Latest result
python view_results.py

# All results
python view_results.py all
```

---

## Example Output

**Input** (Playwright test failure):
```javascript
// demo.spec.js:13
await expect(page).toHaveTitle('Welcome to Example Website');
// ❌ Fails: actual title is "Example Domain"
```

**Output** (Triaged bug report):
```json
{
  "title": "Page title does not match expected value",
  "description": "The test expects the page title to be 'Welcome to Example Website', but the actual title is 'Example Domain'. This indicates a mismatch in the expected page title assertion. The failure occurred during the automated UI test execution when validating the page title after navigation. This could be due to incorrect test expectations, a change in the application's title tag, or the test navigating to the wrong page. The development team should verify the correct page title and update either the test or the application accordingly.",
  "error_line": 13,
  "playwright_script": "file:///c:/bug-triage-engine/demo.spec.js#L13",
  "test_url": "https://example.com",
  "status": "failed"
}
```

---

## Project Improvements Made

### Code Cleanup (40% Reduction)
**Removed from `triage_service.py`**:
- ❌ Severity calculation (unused)
- ❌ Flakiness detection (unused)
- ❌ Confidence scoring (unused)
- ❌ Configuration dictionaries
- ❌ 200+ lines of dead code

**Result**: 508 lines → 311 lines (39% reduction)

### Bug Fixes
1. **ANSI Code Stripping**: Fixed gibberish in error messages
2. **Title Generation**: Enhanced Playwright assertion detection for specific titles
3. **Exception Handling**: Fixed HTTPError vs HTTPException bug
4. **Created Missing Files**: Added `view_results.py` for CLI result viewing

### Supported Playwright Assertions
- ✅ `toHaveTitle` → "Page title does not match expected value"
- ✅ `toBeVisible` → "Expected button element is not visible"
- ✅ `toHaveURL` → "Page URL does not match expected value"
- ✅ `toHaveText` → "Element text content does not match expected value"
- ✅ `toHaveCount` → "Element count does not match expected value"
- ✅ `toContainText`, `toBeEnabled`, `toBeDisabled`, `toBeChecked`

---

## File Structure

```
c:\bug-triage-engine/
├── app/
│   ├── api/routes.py              # API endpoints
│   ├── services/
│   │   ├── triage_service.py      # Main triage logic
│   │   ├── ollama_service.py      # LLM integration
│   │   └── storage_service.py     # Result storage
│   ├── utils/url_utils.py         # URL formatting
│   └── schemas.py                 # Pydantic models
├── main.py                        # Entry point
├── bert_server.py                 # BERT server (port 8001)
├── playwright_script_server.py    # Script server (port 8005)
├── demo_playwright_failures.py    # Test runner & parser
├── view_results.py                # Results viewer CLI
├── demo.spec.js                   # Demo Playwright tests
└── playwright.config.js           # Playwright config
```

---

## API Reference

### Submit Test Failure
```bash
POST http://192.168.1.13:8003/api/triage
Content-Type: application/json

{
  "test_name": "should fail - incorrect page title",
  "file_path": "demo.spec.js",
  "error_message": "expect(page).toHaveTitle(expected) failed",
  "stack_trace": "at demo.spec.js:13:5",
  "logs": "Test execution logs...",
  "llm_model": "gemma:2b",
  "bert_url": "http://localhost:8001/triage"
}
```

### Get Latest Result
```bash
GET http://192.168.1.13:8003/api/triage/latest
```

### Get All Results
```bash
GET http://192.168.1.13:8003/api/triage
```

---

## Configuration

### Ports
- **8003**: Triage Engine API
- **8001**: BERT Server
- **8005**: Playwright Script Server
- **11434**: Ollama LLM

### LLM Settings
- **Model**: gemma:2b
- **Temperature**: 0.7
- **Max Tokens**: 1200

---

## Use Cases

1. **CI/CD Integration**: Automatically triage test failures in pipelines
2. **QA Automation**: Reduce manual bug report writing time
3. **Developer Productivity**: Get instant analysis of test failures
4. **Bug Tracking**: Generate structured bug reports for JIRA/GitHub
5. **Test Maintenance**: Identify patterns in test failures

---

## Benefits

✅ **Time Savings**: No manual bug report writing  
✅ **Consistency**: Standardized bug report format  
✅ **AI-Powered**: Intelligent root cause analysis  
✅ **Developer-Friendly**: Clickable links to failing code  
✅ **API-First**: Easy integration with existing tools  
✅ **Clean Codebase**: 40% code reduction, easier maintenance

---

## Repository

**Owner**: Tulasiram01  
**Repo**: QA-GARDEN  
**Location**: `c:\bug-triage-engine`

---

## Future Enhancements

- Integration with JIRA/GitHub Issues
- Duplicate bug detection
- Historical trend analysis
- Screenshot/video attachment support
- Multi-language test support (Python, Java, etc.)
