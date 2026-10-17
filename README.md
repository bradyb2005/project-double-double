# Project Double Double

COSC 310 Final Project.
Version: M1 - First Vertical Slice

### Required Python Version

* `3.12+`

### Setup Instructions

1. Clone the repo:

   ```bash
   git clone https://github.com/bradyb2005/project-double-double.git
   cd project-double-double
   ```
2. Create and activate virtual enviroment

   ```bash
   python -m venv .venv
   ```

   For MacOS / Linux:
   ```bash
   source .venv/bin/activate.ps1
   ```

   For Windows:
   ```bash
   .venv/Scripts/activate.ps1
   ```
3. Install dependencies

   ```bash
   pip install -r backend/app/requirements.txt
   ```

### How to start the application

**Run in the `backend/` directory:**
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```
    
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
