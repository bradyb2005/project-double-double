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
