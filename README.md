# Project Double Double

COSC 310 Final Project.
Version: M0 - Foundational Gate

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
   pip install -r requirements.txt
   ```

### How to start the application

**Run in the root directory:**
    ```bash
    uvicorn app.main:app --reload
    ```
    
**API endpoint paths:**

 - API is available at http://127.0.0.1:8000
 - Health Check Endpoint at http://127.0.0.1:8000/health (Returns HTTP 200)
 - Restaurant List Endpoint at http://127.0.0.1:8000/restaurants
 - Docs path is available at http://127.0.0.1:8000/docs

**Location of representative data:**
Stored inside 'data/restaurants.json'

### How to run tests:

```bash
python -m pytest
```

### Brief repository structure
```text
project-double-double/
├── app/                  # Main application package
│   ├── api/              # API router handling
│   │   └── routes/       # Endpoint paths (/health, /restaurants)
│   ├── core/             # App configuration settings (Currently not in use)
│   ├── repositories/     # Data access layer (File reading logic)
│   ├── schemas/          # Data transfer objects and Pydantic models (Currently not in use)
│   ├── services/         # Business & application logic layer
│   ├── main.py           # Application entry point
│   └── pyproject.toml    # Application configurations and dependencies
├── data/                 # Data persistence layer
│   └── restaurants.json  # Database file
├── scrum/                # Scrum artifacts
│   └── team-agreement.md # Team workflows and versions
├── tests/                # Test suite modules
│   └── test_main.py      # Automated test specifications
└── README.md             # Setup and developer documentation
```
