# AI Provenance - Project Double Double

> *(Note: Provenance Entries are not required for Milestone 0 - Foundational Gate)*

#### AI Label Glossary:

| Situation                                                                       | Label            |
| :------------------------------------------------------------------------------ | :--------------- |
| You ask AI to write a function and then modify the generated code.              | `AI-GENERATED` |
| You ask AI for implementation suggestions and then write the function yourself. | `AI-ASSISTED`  |
| You write a function and later ask AI to refactor it.                           | `AI-REVISED`   |
| You write the function without using generative AI.                             | `NO-AI`        |

---

## Milestone 0 - Foundation

### Template: Entry 0

- **Date:** Thursday, September 24
- **Student(s):** @bradyb2005
- **Artifact:** `docs/PROVENANCE.md`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [X] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Verify the template for future Provenance entries.
- **Influence:** Used Gemini to verify the formatting, semantics, and spelling were correct.
- **Validation:** Manually previewed rendered Markdown in GitHub to confirm suggestions formatted properly.
- **PR:** 71

### Entry: GitHub Actions PR label modification
- **Date:** Thursday, September 24
- **Student(s):** @bradyb2005
- **Artifact:** `.github/workflows/auto-label-pr.yml`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** I don't know YML so I had Gemini refactor the existing GitHub automation to auto assign a PR's author to assignee and the remaining 3 group members as reviewers.
- **Influence:** AI fully generated the revised YML code.
- **Validation:** Unable to validate until PR is merged.
- **PR:** #28

---

## Milestone 1 - First Vertical Slice

### Entry: Restaurant route testing

- **Date:** Wednesday, September 30th
- **Student(s):** @bradyb2005
- **Artifact:** `tests/services/test_restaurant_service.py`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Help prevent testing from creating new restaurants to `restaurants.json`.
- **Influence:** Used Gemini to ask how to prevent that, and it generated a bypass using the `unittest.mock patch` function.
- **Validation:** Ran `python -m pytest`, and verified that testing does not create a restaurant.
- **PR:** #27

### Entry: Restaurant service validation

- **Date:** Wednesday, September 30th
- **Student(s):** @bradyb2005
- **Artifact:** `/.gitignore`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Prevent GitHub from staging `pycache` files from testing.
- **Influence:** Used Gemini to ask how to do that, and figured out to add the lines below:
```bash
.pytest_cache/
*/.pytest_cache/
```
- **Validation:** Ran `python -m pytest`, and verified that new pycache files/folders won't appear in VS Code's source control panel.
- **PR:** #27

### Entry: Pycache .gitignore

- **Date:** Wednesday, September 30th
- **Student(s):** @bradyb2005
- **Artifact:** `app/services/restaurant_service.py`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [x] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Figure out how to type check for phones and postal codes using regex.
- **Influence:** Used Gemini to find the correct regex pattern when original attempts came up null.
- **Validation:** Ran tests in `test_restaurant_service.py` to validate the generated regex's correctness.
- **PR:** #27

### Entry: Restaurant route testing
- **Date:** Tuesday, October 6th
- **Student(s):** @Lxamwastaken
- **Artifact:** `tests/conftest.py` `tests/services/test_menu_item_service.py`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [x] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:**
  - Assisted with understanding pytest fixtures and creating service-layer tests for the menu item feature.
  - Helped identify missing test fixture data (`"menu": []`) required by the new menu functionality.
- **Influence:**
  - Helped diagnose and resolve test failures caused by missing menu data in test fixtures.
- **Validation:**
  - Ran `python -m pytest`, and verified that testing passes 13/13
- **PR:** #31

### Entry: Dummy data for menu items
- **Date:** Saturday, October 10
- **Student(s):** @advvaith~
- **Artifact:** `data/menus.json`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** dummy data for the view menu endpoint
- **Influence:** got dummy data to proceed
- **Validation:** read the output to see if it checks out
- **PR:** #25

### Entry: GitHub Actions PR label modification
- **Date:** Saturday, October 10
- **Student(s):** @mooz-55
- **Artifact:** `tests/rservices/test_restaurant_service`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [x] AI-REVISED ✍️

### Entry: Search/Filter tests creation
- **Date:** Thursday, Oct 15th
- **Student(s):** @bradyb2005
- **Artifact:** `tests/conftest.py`, `tests/services/test_restaurant_service.py`, `tests/api/routes/test_restaurant_routes.py`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Neeeded some help formatting and organizing the tests. I had the base and conditions needed to be tested, but was not completely fammiliar with the python formatting so I wrote my own and used Gemini to review. I then took the format and wrote my own tests under for the otheer conditions.
- **Influence:** AI checked over my test code and fixed formatting and syntax errors
- **Validation:** Unable to validate until PR is merged.
- **PR:** #33

**Date:** Friday, October 16th
- **Purpose:** 
  - Provide automated unit and integration test coverage for the search and filter restaurant feature
- **Influence:**
  - Generated tests across the service and routing layer.
- **Validation:** 
  - Manually approved these tests and ran them using `python -m pytest`.
- **PR:** #37

### Entry: Menu item update bug fix

- **Date:** Tuesday, October 16th
- **Student(s):** @Lxamwastaken
- **Artifact:** `services/restaurant_service.py` 
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [x] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** 
  - Assisted solving bug where errors occured updating a single part of an item
- **Influence:**
  - Helped diagnose and resolve error that arose when manually testing
- **Validation:** 
  - Tested updating only item price of restaurant ID 1 and item ID 1 to $150.00
- **PR:** #36

### Entry: Menu item service tests

- **Date:** Friday, October 16th
- **Student(s):** @Lxamwastaken
- **Artifact:** `tests/services/test_menu_item_service.py` 
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** 
  - Generated test cases to fix known errors
- **Influence:**
  - Helped create test case when manually found error arose
- **PR:** #39

### Entry: Frontend scaffold
- **Date:** Friday, October 16
- **Student(s):** @advvaith~
- **Artifact:** `frontend/`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** React + Vite frontend for browsing restaurants and menus, built on the merged backend endpoints
- **Influence:** generated the whole frontend (pages, API client, Vite proxy to the backend)
- **Validation:** ran it against the backend and checked the pages load restaurant and menu data
- **PR:** #42

### Entry: start.sh setup and launch script
- **Date:** Friday, October 16
- **Student(s):** @advvaith~
- **Artifact:** `start.sh`, `README.md`, `.gitignore`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** one command to install Python, Node and all dependencies, then start the backend and frontend on any OS. Also fixed the README setup steps and added manual steps for every platform
- **Influence:** generated the script and the README changes
- **Validation:** ran `./start.sh` with a fresh venv, checked the backend, frontend and `/api` proxy returned 200 and that Ctrl+C left no processes running. Windows and Linux steps untested
- **PR:** #43

### Entry: GitHub Actions CI workflow
- **Date:** Friday, October 16
- **Student(s):** @advvaith~
- **Artifact:** `.github/workflows/ci.yml`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** M1 requires CI that runs pytest automatically in a clean environment on push and pull request
- **Influence:** generated the workflow (backend pytest job, plus a frontend lint and build job)
- **Validation:** copied the repo into a clean directory, installed the dependencies in a fresh venv and ran the same steps. 56 tests passed and the frontend lint and build succeeded. The workflow has not run on GitHub yet
- **PR:** #44

### Entry: OpenAPI documentation for all endpoints
- **Date:** Friday, October 16
- **Student(s):** @advvaith~
- **Artifact:** `backend/app/api/routes/restaurants.py`, `backend/app/main.py`, `backend/app/schemas/error.py`, `backend/app/schemas/restaurant.py`, `backend/app/schemas/menu_item.py`, `backend/tests/test_openapi_docs.py`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** M1 requires every endpoint to have a description, a response model and documented status codes and errors
- **Influence:** generated the summaries, descriptions, response models, error response documentation and the tests that check them. No endpoint behaviour was changed
- **Validation:** ran the full test suite (61 passed) and sent the same 17 requests to the old and new code on temporary data. Responses were identical except that create and update now also return `rating: 0.0`
- **PR:** #45

### Entry: README and M1 submission doc update
- **Date:** Friday, October 16
- **Student(s):** @advvaith~
- **Artifact:** `README.md`, `docs/submissions/m1-first-vertical-slice.md`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** M1 requires the README to reflect the implementation, and the submission doc linked to the wrong tag
- **Influence:** generated the endpoint table, architecture, frontend, testing and CI sections and the updated structure tree, and corrected the tag link and commit line in the submission doc
- **Validation:** compared the endpoint table (methods, paths, success and error codes) against the generated OpenAPI schema with a script, all 9 endpoints match. Have not viewed the rendered README on GitHub yet
- **PR:** #43

## Milestone 2 - Integrated System

### Entry: M1 bug checks/fixes for M2
- **Date:** Friday, October 16
- **Student(s):** @Lxamwastaken
- **Artifact:** `backend/tests/services/test_restaurant_service.py`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [x] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** To make sure our existing M1 code is rock-solid
- **Influence:** generated a list of potential tests to add to enforce our code's behaviour.
- **Validation:** Implemented tests and ran them
- **PR:** #65

### Entry: Security setup for password hashing
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/core/security.py`, `backend/app/requirements.txt`
- **Label:**
- [x] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [ ] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Needed to securely hash and verify user passwords for the JSON data storage using bcrypt.
- **Influence:** Generated the `CryptContext` configuration and the `get_password_hash` and `verify_password` utility functions using the `passlib` library.
- **Validation:** Reviewed the implementation to ensure it matches standard passlib security practices and confirmed `passlib[bcrypt]` was successfully added to `requirements.txt`.
- **PR:** #66

### Entry: Fix role type annotation in UserCreate schema
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/schemas/user.py`
- **Label:**
- [ ] AI-GENERATED 🤖
- [x] AI-ASSISTED 🤝
- [ ] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Didn't know how to set a default enum value in the `UserCreate` schema.
- **Influence:** Updated the `role` field in `UserCreate` to use the `UserRole` Enum type, and provided the syntax for setting an Enum default value.
- **Validation:** Verified no errors in implementation.
- **PR:** #66

### Entry: Refactor schemas using Base class inheritance
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/schemas/user.py`
- **Label:**
- [ ] AI-GENERATED 🤖
- [x] AI-ASSISTED 🤝
- [ ] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Eliminate code duplication between User and UserCreate schemas.
- **Influence:** Provided the UserBase inheritance pattern to share fields and validators across Pydantic models.
- **Validation:** Ensured compliance with standard FastAPI/Pydantic DRY (Don't Repeat Yourself) architectural patterns.
- **PR:** #66

### Entry: Revision suggestion to add UserUpdate schema
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/schemas/user.py`
- **Label:**
- [ ] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [x] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Align Pydantic models with the M2 T1.1 GitHub issue acceptance criteria.
- **Influence:** Generated a `UserUpdate` schema to support partial profile updates.
- **Validation:** Cross-referenced existing code with the GitHub issue tracker (#51).
- **PR:** #66

### Entry: Add update_user method to JSON repository
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/repositories/user_repository.py`
- **Label:**
- [x] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [ ] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Implement a method to update an existing user by ID within the JSON-based repository.
- **Influence:** Generated the `update_user` repository method leveraging dictionary in-place modification and automatic `last_modified` timestamping, plus demonstrated integration with Pydantic's `model_dump(exclude_unset=True)`.
- **Validation:** Ensured correct Python dictionary `.update()` behavior.
- **PR:** #66

### Entry: Review and correct UserService imports
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/services/user_service.py`
- **Label:**
- [ ] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [x] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Review `user_service.py` logic and fix a bug with the `timezone` import.
- **Influence:** Identified that `timezone` was incorrectly imported from the `time` module instead of `datetime` and provided the corrected import statement.
- **Validation:** Visual code review of the provided screenshot against standard Python library documentation.
- **PR:** #66

### Entry: Fix logic bugs in deactivate_user method
- **Date:** Thursday, November 5
- **Student(s):** @bradyb2005
- **Artifact:** `backend/app/services/user_service.py`
- **Label:**
- [ ] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [x] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [x] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [ ] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Resolve a boolean logic inversion and a data-persistence crash in the deactivation flow.
- **Influence:** Corrected the `is_active` check and refactored the method to correctly utilize the repository's `update_user` function without redundantly calling `save_users`.
- **Validation:** Ensured correct Python boolean evaluation and prevented a type-mismatch crash during file I/O operations. No tests have been made yet, that will truly validate this fix.
- **PR:** #66

### Entry: Fix user route test environment compatibility
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifact:** `backend/tests/api/routes/test_user_routes.py`, `backend/tests/conftest.py`, `pyproject.toml`, `backend/app/requirements.txt`
- **Label:**
- [ ] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [x] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Fix the user route test failure caused by the test dependency override and incompatible bcrypt version.
- **Influence:** Corrected the test fixture imports and user data field, updated the invalid-input expectation, and constrained bcrypt to a Passlib-compatible version.
- **Validation:** Reinstalled dependencies and ran `pytest`; all 68 tests passed.
- **PR:** #66

### Entry: Add user repository tests
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifact:** `backend/tests/repositories/test_user_repository.py`
- **Label:**
- [x] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [ ] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Add automated coverage for the user repository's file operations, lookups, updates, and error handling.
- **Influence:** Generated tests using the existing `users_json` and `user_repository` fixtures, including persistence checks and invalid input scenarios.
- **Validation:** Ran the focused repository tests and the full test suite; all 77 tests passed.
- **PR:** #66

### Entry: Add user service tests
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifact:** `backend/tests/services/test_user_service.py`
- **Label:**
- [x] AI-GENERATED 🤖
- [ ] AI-ASSISTED 🤝
- [ ] AI-REVISED ✍️
- [ ] NO-AI ❌
- **AI Tool Used:**
- [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
- [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
- [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
- [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
- [ ] Other: ____
- **Purpose:** Add service-level coverage for user registration, profile access, updates, deactivation, and validation acceptance criteria.
- **Influence:** Generated tests using the existing user fixtures and schema types to verify customer defaults, restaurant roles, generated fields, partial updates, and error handling.
- **Validation:** Ran the focused user service tests and the full test suite; all 89 tests passed.
- **PR:** #66

### Entry: Add project start date workflow
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifact:** `.github/workflows/set-project-start-date.yml`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Automatically set an issue's GitHub Project start date when a branch named with the issue number is created.
- **Influence:** Generated a GitHub Actions workflow that parses the issue number from the branch name, locates the issue in the project, and updates its `Start date` field through the Projects GraphQL API.
- **Validation:** Reviewed the workflow configuration and verified the YAML diff formatting. The workflow requires a `PROJECT_TOKEN` secret and a configured project number before live validation.
- **PR:** #67

### Entry: Add JWT security and automatic local secret setup
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifacts:** `backend/app/core/security.py`, `backend/app/requirements.txt`, `pyproject.toml`, `start.sh`, `.env` configuration, `.gitignore`, `README.md`, `.vscode/settings.json`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Add JWT-based access-token security for M2 login and make the project downloadable and runnable without committing a secret key.
- **Influence:** Added token creation and validation to `security.py`, added the `PyJWT` dependency, generated a local `.env` secret from `start.sh`, loaded the secret at runtime, ignored `.env`, and documented the setup behavior.
- **Validation:** Ran the full test suite with 102 tests passing, verified JWT creation and tamper rejection, checked `start.sh` syntax, and ran `./start.sh --setup-only` to confirm local secret generation.
- **PR:** 71

### Entry: Add login service tests
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifact:** `backend/tests/services/test_login_service.py`, `backend/tests/conftest.py`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [x] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Add service-level coverage for successful login, missing accounts, incorrect passwords, and inactive accounts.
- **Influence:** Assisted with organizing shared login fixtures and identifying the service behaviors that require tests.
- **Validation:** Ran the focused login tests and the full test suite; all 110 tests passed.
- **PR:** 71

### Entry: Add login route tests
- **Date:** Friday, November 6
- **Student(s):** @bradyb2005
- **Artifact:** `backend/tests/api/routes/test_login_routes.py`, `backend/tests/conftest.py`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [x] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Add route-level coverage for successful login, invalid credentials, authentication headers, and request validation.
- **Influence:** Assisted with configuring the FastAPI dependency override and checking the expected HTTP status codes.
- **Validation:** Ran the focused login and user route tests; all 14 tests passed.
- **PR:** 71

### Entry: Configure CI test secret
- **Date:** Saturday, November 7
- **Student(s):** @bradyb2005
- **Artifact:** `.github/workflows/ci.yml`
- **Label:**
  - [ ] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [x] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Fix CI authentication test failures caused by the missing `SECRET_KEY` environment variable.
- **Influence:** Revised the backend test job to provide a non-production secret key during GitHub Actions runs.
- **Validation:** Ran the backend test suite with the CI secret; all 117 tests passed with no warnings. Also verified the Git diff formatting.
- **PR:** 71

### Entry: Build customer account frontend
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifacts:** `frontend/src/api.js`, `frontend/src/App.jsx`, `frontend/src/components/Layout.jsx`, `frontend/src/pages/Login.jsx`, `frontend/src/pages/Register.jsx`, `frontend/src/pages/customer/Account.jsx`, `frontend/src/roles.js`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Implement the frontend required by issue #56 for customer registration, sign-in, and profile management.
- **Influence:** Generated the React routes, forms, API integration, token storage, authenticated profile loading, profile editing, validation, and account navigation using the existing Rubric design system and backend user endpoints.
- **Validation:** Ran the frontend lint and production build; both completed successfully.
- **Issue:** #56

### Entry: Add login test-account shortcuts
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifacts:** `frontend/src/pages/Login.jsx`, `backend/data/users.json`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Add login-screen shortcuts for testing customer, restaurant, and admin authentication flows.
- **Influence:** Generated labeled autofill buttons and seeded non-production accounts using the existing user schema and bcrypt password conventions.
- **Validation:** Ran the frontend lint and production build; both completed successfully.
- **Issue:** #56

### Entry: Fix backend startup import paths
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifacts:** `backend/app/api/routes/login.py`, `backend/app/api/routes/users.py`, `backend/app/core/dependencies.py`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Make the backend start consistently from the documented `backend/` directory.
- **Influence:** Replaced mixed `backend.app` imports with the local `app` package imports used by `uvicorn app.main:app`.
- **Validation:** Verified `from app.main import app` succeeds from `backend/`.

### Entry: Remove landing role chooser
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifact:** `frontend/src/App.jsx`, `frontend/README.md`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Remove the landing role chooser so the application opens directly to sign-in.
- **Influence:** Changed the root route to render the existing login screen and updated the frontend route description.
- **Validation:** Confirmed the route configuration and documentation diff are formatted correctly.

### Entry: Remove remaining role-selection labels
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifacts:** `frontend/src/components/Layout.jsx`, `frontend/src/pages/Login.jsx`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Remove residual role-selection language from the direct sign-in experience.
- **Influence:** Hid switch-role links when no role is active and renamed the login page eyebrow to “Sign in.”
- **Validation:** Ran the frontend lint and production build successfully.

### Entry: Confirm sign-out
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifact:** `frontend/src/components/Layout.jsx`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Prevent accidental sign-outs.
- **Influence:** Added a confirmation prompt before clearing the access token from either sign-out control.
- **Validation:** Ran the frontend lint and production build successfully.

### Entry: Prefill checkout from customer profile
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifact:** `frontend/src/pages/customer/Cart.jsx`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Populate checkout delivery fields from the authenticated customer's account.
- **Influence:** Loaded the signed-in user profile and used its name, phone, and street address as initial checkout values while preserving manually entered values.
- **Validation:** Ran the frontend lint and production build successfully.

### Entry: Replace switch-role navigation with sign-out
- **Date:** Wednesday, November 11
- **Student(s):** @bradyb2005
- **Artifact:** `frontend/src/components/Layout.jsx`
- **Label:**
  - [x] AI-GENERATED 🤖
  - [ ] AI-ASSISTED 🤝
  - [ ] AI-REVISED ✍️
  - [ ] NO-AI ❌
- **AI Tool Used:**
  - [ ] Gemini <img src="https://shorturl.at/aT3Bx" width="16" align="top 60%"/>
  - [ ] ChatGPT <img src="https://shorturl.at/BmeCK" width="16" align="top 60%"/>
  - [ ] Claude <img src="https://shorturl.at/pAFE7" width="16" align="top 60%"/>
  - [x] Copilot <img src="https://shorturl.at/P9VwD" width="16" align="top 60%"/>
  - [ ] Other: ____
- **Purpose:** Remove the obsolete role-switching control and provide a clear sign-out action for signed-in users.
- **Influence:** Replaced switch-role links with a sign-out button that clears the access token and navigates to `/login`.
- **Validation:** Ran the frontend lint and production build successfully.