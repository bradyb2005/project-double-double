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
- **PR:** N/A

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

### Entry: Pycache .gitignore

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

**Date:** Tuesday, October 16th
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

**Date:** Friday, October 16th
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

### Entry: README and M1 submission doc update
- **Date:** Friday, October 16
- **Student(s):** @Lxamwastaken
- **Artifact:** `app/backend/tests/services/test_restaurant_service.py`
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