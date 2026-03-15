# Week 5 — Flask Backend & Unit Testing

## Setup

### Install dependencies (first time only)

```bash
pip install -r requirements.txt
```

This installs `flask`, `flask-cors`, and `selenium`.

> If VS Code shows `Import "flask" could not be resolved`, press `Ctrl+Shift+P` → **Python: Select Interpreter** → pick the interpreter where you installed Flask.

---

## Running the servers

You need **two terminals** running at the same time. Both must be in the `week5/` directory.

### Terminal 1 — Backend (Flask API on port 8080)

```bash
cd week5
python -m backend.app
```

### Terminal 2 — Frontend (static files on port 8000)

```bash
cd week5
python -m http.server 8000 --directory ./frontend/
```

### Frontend pages

| URL | Page |
|-----|------|
| http://127.0.0.1:8000/index.html | Home page |
| http://127.0.0.1:8000/register.html | Registration form |
| http://127.0.0.1:8000/welcome.html | Welcome page |

> Note: you must include `.html` in the URL. `http://127.0.0.1:8000/register` will return 404 — the static file server serves files by their exact filename.

---

## Testing the API

The backend has one endpoint: `POST /welcome` — it accepts a JSON body with a `name` field and returns a greeting.

### Option A — Postman (recommended)

1. Open Postman, click `+` to create a new request
2. Set method to **POST**
3. Set URL to `http://127.0.0.1:8080/welcome`
4. Click **Body** tab → select **raw** → change dropdown to **JSON**
5. Enter the body:
   ```json
   {
       "name": "Alice"
   }
   ```
6. Click **Send**

Expected response:

```json
{
    "status": "success",
    "message": "Hello, Alice!"
}
```

### Option B — curl (Mac/Linux)

```bash
curl -X POST http://127.0.0.1:8080/welcome \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice"}'
```

### Option C — curl (Windows PowerShell)

PowerShell has a `curl` alias that is NOT real curl. Use `curl.exe` instead, and be careful with quotes:

```powershell
curl.exe -X POST http://127.0.0.1:8080/welcome -H "Content-Type: application/json" -d '{"name": "Alice"}'
```

If the above gives a JSON error, PowerShell is mangling the quotes. Write the body to a file first:

```powershell
'{"name": "Alice"}' | Out-File -Encoding utf8 body.json
curl.exe -X POST http://127.0.0.1:8080/welcome -H "Content-Type: application/json" -d @body.json
```

Or use PowerShell's native command:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8080/welcome -Method POST -ContentType "application/json" -Body '{"name": "Alice"}'
```

### Things to try

| Experiment | What happens | Why |
|-----------|--------------|-----|
| Send without `"name"` field: `{}` | Returns `"Hello, None!"` | `.get("name")` returns `None` when key is missing |
| Send a GET request to `/welcome` | `405 Method Not Allowed` | Route only accepts `POST` |
| Visit `/login` | `404 Not Found` | No route registered for `/login` |

---

## `debug=True` vs `debug=False`

In `app.py`, the server starts with:

```python
app.run(debug=True, host="127.0.0.1", port=8080)
```

| | `debug=True` | `debug=False` |
|---|---|---|
| **Auto-reload** | Server restarts automatically when you save a code change | You must manually stop (`Ctrl+C`) and restart the server after every change |
| **Error pages** | Shows detailed error messages in the browser with a full Python traceback | Shows a generic "Internal Server Error" message |
| **Interactive debugger** | Enables a Python debugger in the browser (the Debugger PIN in the terminal) — lets you execute code on the server | No debugger |
| **Performance** | Slower (runs extra monitoring processes) | Faster |
| **When to use** | During development | In production / when deploying to real users |

> **Security warning:** Never use `debug=True` in production. The interactive debugger allows anyone who can reach your server to execute arbitrary Python code — this is a critical security vulnerability.

---

## Running unit tests

All test commands must be run from the `week5/` directory. No need to start the backend server — tests run the code directly.

### Run all tests

```bash
python -m unittest backend.test_project_bidding
```

### Run a specific test

```bash
python -m unittest backend.test_project_bidding.TestAllocation.test_registration_success
```

The dotted path means: `backend` (package) → `test_project_bidding` (file) → `TestAllocation` (class) → `test_registration_success` (method).

### Run with verbose output

```bash
python -m unittest -v backend.test_project_bidding
```

### Normal vs verbose output

**Normal** — shows a dot per test, minimal detail:

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

Each `.` = pass, `F` = failure, `E` = error. With 3 dots you can't tell which test is which.

**Verbose (`-v`)** — shows every test name and its result:

```
test_allocation_success (backend.test_project_bidding.TestAllocation) ... ok
test_duplicated_registration_fail (backend.test_project_bidding.TestAllocation) ... ok
test_registration_success (backend.test_project_bidding.TestAllocation) ... ok
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

Use `-v` when debugging — if a test fails, you immediately see which one.

---

## Stopping servers

- Press `Ctrl+C` in the terminal where the server is running
- If the terminal was closed and the port is stuck:

**Windows:**
```powershell
netstat -ano | findstr :8080
taskkill /PID <PID_number> /F
```

**Mac/Linux:**
```bash
lsof -i :8080
kill -9 <PID>
```

---

## File overview

```
week5/
├── backend/
│   ├── __init__.py               ← Makes backend/ a Python package (empty file)
│   ├── app.py                    ← Flask server with POST /welcome endpoint
│   ├── project_bidding.py        ← Domain logic: User, Project, DB, Admin classes
│   └── test_project_bidding.py   ← Unit tests for the domain logic
└── frontend/
    ├── index.html                ← Home page
    ├── register.html             ← Registration form
    ├── register.js               ← Form handler (saves to sessionStorage)
    ├── welcome.html              ← Welcome page
    ├── welcome.js                ← Reads user from sessionStorage
    ├── logout.html               ← Logout confirmation
    ├── style.css                 ← Shared styles
    └── sunflower.jfif            ← Sample image
```

> Note: the frontend and backend are **not connected** in week 5. The frontend uses `sessionStorage` (browser-only). The backend API (`POST /welcome`) is standalone. They get connected in week 9 using `fetch()`.
