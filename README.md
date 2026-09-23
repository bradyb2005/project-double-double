# Project Double Double
COSC 310 Final Project.

Required Python version.
3.12+

Setup instructions.
1. Clone the repo:
    Git clone https://github.com/bradyb2005/project-double-double.git
    cd project-double-double
2. Create and activate virtual enviroment
    python -m venv .venv
    #macOS / Linux 
    source .venv/bin/activate.ps1
    #windows
    .venv/Scripts/activate.ps1
3. Install dependencies
    pip install -r requirements.txt

How to start the application.
Run in the root directory:
    uvicorn app.main:app --reload

API endpoint paths.
API is available at http://127.0.0.1:8000
Health Check Endpoint at http://127.0.0.1:8000/health (Returns HTTP 200)
Restaurant List Endpoint at http://127.0.0.1:8000/restaurants

/docs path.
Docs path is available at http://127.0.0.1:8000/docs

Location of representative data.
Stored inside 'data/restaurants.json'

How to run tests.
python -m pytest

Brief repository structure.
project-double-double/
├── app/                  # Main application package
│   ├── api/              # API router handling
│   │   └── routes/       # Endpoint paths (/health, /restaurants)
│   ├── core/             # App configuration settings
│   ├── repositories/     # Data access layer (File reading logic)
│   ├── schemas/          # Data transfer objects and Pydantic models
│   ├── services/         # Business & application logic layer
│   ├── main.py           # Application entry point
|   └── pyproject.toml    # Application configurations and dependencies
├── data/                 # Data persistence layer
│   └── restaurants.json  # Database file
├── scrum/                # Scrum artifacts
│   └── team-agreement.md # Team workflows and versions
├── tests/                # Test suite modules
│   └── test_main.py      # Automated test specifications
└── README.md             # Setup and developer documentation