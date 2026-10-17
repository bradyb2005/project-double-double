# Project Double Double

COSC 310 Final Project.
Version: M1 - First Vertical Slice

### Required Python Version

* `3.12+`

### Quick start (one command)

```bash
git clone https://github.com/bradyb2005/project-double-double.git
cd project-double-double
./start.sh
```

`start.sh` installs anything missing (Python 3.12+, Node 20.19+, a `.venv`, the backend and frontend dependencies), then starts both servers:

 - Backend at http://127.0.0.1:8000 (API docs at `/docs`)
 - Frontend at http://localhost:5173

Press Ctrl+C to stop both. Use `./start.sh --setup-only` to install without starting. Works on macOS, Linux and Windows (Git Bash / WSL).

### Setup Instructions (manual)

Prerequisites: Python 3.12+ and Node.js 20.19+ (with npm), plus Git.

1. Clone the repo:

   ```bash
   git clone https://github.com/bradyb2005/project-double-double.git
   cd project-double-double
   ```
2. Create the virtual environment (from the repo root)

   macOS / Linux:
   ```bash
   python3 -m venv .venv
   ```

   Windows (PowerShell or Command Prompt):
   ```powershell
   py -m venv .venv
   ```
3. Activate it

   macOS / Linux (bash / zsh):
   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and retry.

   Windows Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```

   Windows Git Bash:
   ```bash
   source .venv/Scripts/activate
   ```
4. Install backend dependencies (same command on every platform)

   ```bash
   pip install -r backend/app/requirements.txt
   ```
5. Install frontend dependencies (same command on every platform)

   ```bash
   cd frontend
   npm install
   cd ..
   ```

### How to start the application

Use two terminals, both starting at the repo root. Activate the venv (step 3 above) in the backend terminal.

**Terminal 1, backend (run in the `backend/` directory):**
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 2, frontend (run in the `frontend/` directory):**
```bash
cd frontend
npm run dev
```

The frontend is at http://localhost:5173 and proxies `/api/*` to the backend, so start the backend first.

**API endpoint paths:**

 - API is available at http://127.0.0.1:8000
 - Health Check Endpoint at http://127.0.0.1:8000/health (Returns HTTP 200)
 - Restaurant List Endpoint at http://127.0.0.1:8000/restaurants
 - Docs path is available at http://127.0.0.1:8000/docs

**Location of representative data:**
Stored inside 'backend/data/restaurants.json'

### How to run tests:

Run in the `backend/` directory:

```bash
cd backend
python -m pytest
```

### Brief repository structure
```text
project-double-double/
├── backend/              # FastAPI backend (run uvicorn and pytest from here)
│   ├── app/              # Main application package
│   │   ├── api/          # API router handling
│   │   │   └── routes/   # Endpoint paths (/health, /restaurants)
│   │   ├── core/         # App configuration settings (Currently not in use)
│   │   ├── repositories/ # Data access layer (File reading logic)
│   │   ├── schemas/      # Data transfer objects and Pydantic models
│   │   ├── services/     # Business & application logic layer
│   │   ├── main.py       # Application entry point
│   │   └── pyproject.toml # Application configurations and dependencies
│   ├── data/             # Data persistence layer
│   │   └── restaurants.json # Database file
│   ├── tests/            # Test suite modules
│   │   └── test_main.py  # Automated test specifications
│   └── pytest.ini        # Pytest configuration
├── docs/                 # Documentation and provenance log
└── README.md             # Setup and developer documentation
```
