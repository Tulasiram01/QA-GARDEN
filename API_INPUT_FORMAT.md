# Triage API Input Format

## POST Endpoint
`http://192.168.1.13:8003/api/triage`

## Required Fields

```json
{
  "test_name": "",
  "file_path": "",
  "error_message": "",
  "stack_trace": "",
  "logs": "",
  "llm_model": "gemma:2b",
  "bert_url": "http://127.0.0.1:8001",
  "labels": [],
  "test_url": "",
  "playwright_script_url": "",
  "playwright_script_endpoint": ""
}
```

## Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `test_name` | string | Yes | Test name |
| `file_path` | string | Yes | File path |
| `error_message` | string | Yes | Error message |
| `stack_trace` | string | Yes | Stack trace |
| `logs` | string | Optional | Test logs |
| `llm_model` | string | Yes | Use: `"gemma:2b"` |
| `bert_url` | string | Yes | Use: `"http://127.0.0.1:8001"` |
| `labels` | array | Optional | Labels/tags |
| `test_url` | string | Optional | URL being tested |
| `playwright_script_url` | string | Optional | Playwright script URL |
| `playwright_script_endpoint` | string | Optional | External Playwright script service endpoint |

---

## GET Endpoints

### Get Latest Test Result
`GET http://192.168.1.13:8003/api/triage/latest`

Returns the most recently executed test result.

### Get All Test Results
`GET http://192.168.1.13:8003/api/triage`

Returns all stored test results (newest first).

### Get Specific Test Result
`GET http://192.168.1.13:8003/api/triage/{result_id}`

Returns a specific test result by ID.

---

**Note:** 
- The `playwright_script_url` field is for local file paths (e.g., `file:///C:/tests/login.spec.js#L25`)
- The `playwright_script_endpoint` field is for external service URLs that provide/execute Playwright scripts (e.g., `http://playwright-service.com/api/scripts/login-test`)

