# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->


Sample Output: carlarodriguez@Mac ai110-module2show-pawpal-starter % python3 -m venv .venv
carlarodriguez@Mac ai110-module2show-pawpal-starter % source .venv/bin/activate
(.venv) carlarodriguez@Mac ai110-module2show-pawpal-starter % .\.venv\Scripts\Activate.ps1
zsh: command not found: ..venvScriptsActivate.ps1
(.venv) carlarodriguez@Mac ai110-module2show-pawpal-starter % python -m pip install --upgrade pip
pip install -r requirements.txt
Requirement already satisfied: pip in ./.venv/lib/python3.13/site-packages (25.1.1)
Collecting pip
  Using cached pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
Using cached pip-26.2.1-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 25.1.1
    Uninstalling pip-25.1.1:
      Successfully uninstalled pip-25.1.1
Successfully installed pip-26.2.1
Collecting streamlit>=1.30 (from -r requirements.txt (line 1))
  Downloading streamlit-1.66.0-py3-none-any.whl.metadata (10 kB)
Collecting pytest>=7.0 (from -r requirements.txt (line 2))
  Using cached pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting altair!=5.4.0,!=5.4.1,<7,>=5.0.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Downloading altair-6.3.0-py3-none-any.whl.metadata (11 kB)
Collecting click<9,>=7.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting numpy<3,>=1.25.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Downloading numpy-2.5.4-cp313-cp313-macosx_14_0_arm64.whl.metadata (6.6 kB)
Collecting packaging>=20 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pandas<4,>=1.5.3 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached pandas-3.0.6-cp313-cp313-macosx_11_0_arm64.whl.metadata (79 kB)
Collecting pillow<13,>=9.2.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached pillow-12.3.0-cp313-cp313-macosx_11_0_arm64.whl.metadata (9.1 kB)
Collecting pydeck<1,>=0.8.0b4 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached pydeck-0.9.3-py2.py3-none-any.whl.metadata (4.2 kB)
Collecting protobuf<8,>=5.26.1 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached protobuf-7.36.2-cp310-abi3-macosx_10_9_universal2.whl.metadata (595 bytes)
Collecting pyarrow!=25.0.0,<27,>=10.0.1 (from streamlit>=1.30->-r requirements.txt (line 1))
  Downloading pyarrow-26.0.0-cp313-cp313-macosx_12_0_arm64.whl.metadata (3.0 kB)
Collecting requests<3,>=2.27 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
Collecting typing-extensions<5,>=4.10.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting starlette<2,>=0.46.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Downloading starlette-1.9.0-py3-none-any.whl.metadata (6.6 kB)
Collecting uvicorn<1,>=0.30.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached uvicorn-0.54.0-py3-none-any.whl.metadata (6.6 kB)
Collecting anyio<5,>=4.0.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting python-multipart<1,>=0.0.10 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached python_multipart-0.0.32-py3-none-any.whl.metadata (2.1 kB)
Collecting websockets<18,>=12.0.0 (from streamlit>=1.30->-r requirements.txt (line 1))
  Downloading websockets-17.2-cp313-cp313-macosx_11_0_arm64.whl.metadata (6.3 kB)
Collecting itsdangerous<3,>=2.1.2 (from streamlit>=1.30->-r requirements.txt (line 1))
  Using cached itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting jinja2 (from altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting jsonschema>=3.0 (from altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
Collecting narwhals>=2.4.0 (from altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Downloading narwhals-2.27.1-py3-none-any.whl.metadata (15 kB)
Collecting idna>=2.8 (from anyio<5,>=4.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Collecting python-dateutil>=2.8.2 (from pandas<4,>=1.5.3->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting charset_normalizer<4,>=2 (from requests<3,>=2.27->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached charset_normalizer-3.5.2-cp313-cp313-macosx_10_13_universal2.whl.metadata (46 kB)
Collecting urllib3<3,>=1.26 (from requests<3,>=2.27->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached urllib3-2.8.0-py3-none-any.whl.metadata (7.4 kB)
Collecting certifi>=2023.5.7 (from requests<3,>=2.27->streamlit>=1.30->-r requirements.txt (line 1))
  Downloading certifi-2026.10.18-py3-none-any.whl.metadata (2.5 kB)
Collecting h11>=0.8 (from uvicorn<1,>=0.30.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting iniconfig>=1.0.1 (from pytest>=7.0->-r requirements.txt (line 2))
  Using cached iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting pluggy<2,>=1.5 (from pytest>=7.0->-r requirements.txt (line 2))
  Downloading pluggy-1.7.0-py3-none-any.whl.metadata (5.0 kB)
Collecting pygments>=2.7.2 (from pytest>=7.0->-r requirements.txt (line 2))
  Using cached pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Collecting MarkupSafe>=2.0 (from jinja2->altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached markupsafe-3.0.4-cp313-cp313-macosx_11_0_arm64.whl.metadata (2.7 kB)
Collecting attrs>=22.2.0 (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting jsonschema-specifications>=2023.03.6 (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached jsonschema_specifications-2025.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting referencing>=0.28.4 (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached referencing-0.37.0-py3-none-any.whl.metadata (2.8 kB)
Collecting rpds-py>=0.25.0 (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached rpds_py-2026.9.1-cp313-cp313-macosx_11_0_arm64.whl.metadata (4.1 kB)
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas<4,>=1.5.3->streamlit>=1.30->-r requirements.txt (line 1))
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Downloading streamlit-1.66.0-py3-none-any.whl (10.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 10.4/10.4 MB 3.7 MB/s  0:00:02
Downloading altair-6.3.0-py3-none-any.whl (797 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━ 797.2/797.2 kB 6.9 MB/s  0:00:00
Using cached anyio-4.15.1-py3-none-any.whl (132 kB)
Using cached click-8.5.0-py3-none-any.whl (125 kB)
Using cached itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Downloading numpy-2.5.4-cp313-cp313-macosx_14_0_arm64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 7.3 MB/s  0:00:00
Using cached pandas-3.0.6-cp313-cp313-macosx_11_0_arm64.whl (10.1 MB)
Using cached pillow-12.3.0-cp313-cp313-macosx_11_0_arm64.whl (4.8 MB)
Using cached protobuf-7.36.2-cp310-abi3-macosx_10_9_universal2.whl (456 kB)
Downloading pyarrow-26.0.0-cp313-cp313-macosx_12_0_arm64.whl (36.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 36.3/36.3 MB 9.9 MB/s  0:00:03
Using cached pydeck-0.9.3-py2.py3-none-any.whl (11.4 MB)
Using cached python_multipart-0.0.32-py3-none-any.whl (30 kB)
Using cached requests-2.34.2-py3-none-any.whl (73 kB)
Using cached charset_normalizer-3.5.2-cp313-cp313-macosx_10_13_universal2.whl (366 kB)
Using cached idna-3.20-py3-none-any.whl (69 kB)
Downloading starlette-1.9.0-py3-none-any.whl (80 kB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached urllib3-2.8.0-py3-none-any.whl (135 kB)
Using cached uvicorn-0.54.0-py3-none-any.whl (87 kB)
Downloading websockets-17.2-cp313-cp313-macosx_11_0_arm64.whl (215 kB)
Using cached pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.7.0-py3-none-any.whl (27 kB)
Downloading certifi-2026.10.18-py3-none-any.whl (134 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Using cached jinja2-3.1.6-py3-none-any.whl (134 kB)
Using cached jsonschema-4.26.0-py3-none-any.whl (90 kB)
Using cached attrs-26.1.0-py3-none-any.whl (67 kB)
Using cached jsonschema_specifications-2025.9.1-py3-none-any.whl (18 kB)
Using cached markupsafe-3.0.4-cp313-cp313-macosx_11_0_arm64.whl (12 kB)
Downloading narwhals-2.27.1-py3-none-any.whl (483 kB)
Using cached packaging-26.3-py3-none-any.whl (129 kB)
Using cached pygments-2.21.0-py3-none-any.whl (1.3 MB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached referencing-0.37.0-py3-none-any.whl (26 kB)
Using cached rpds_py-2026.9.1-cp313-cp313-macosx_11_0_arm64.whl (340 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: websockets, urllib3, typing-extensions, six, rpds-py, python-multipart, pygments, pyarrow, protobuf, pluggy, pillow, packaging, numpy, narwhals, MarkupSafe, itsdangerous, iniconfig, idna, h11, click, charset_normalizer, certifi, attrs, uvicorn, requests, referencing, python-dateutil, pytest, jinja2, anyio, starlette, pydeck, pandas, jsonschema-specifications, jsonschema, altair, streamlit
Successfully installed MarkupSafe-3.0.4 altair-6.3.0 anyio-4.15.1 attrs-26.1.0 certifi-2026.10.18 charset_normalizer-3.5.2 click-8.5.0 h11-0.16.0 idna-3.20 iniconfig-2.3.1 itsdangerous-2.2.0 jinja2-3.1.6 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 narwhals-2.27.1 numpy-2.5.4 packaging-26.3 pandas-3.0.6 pillow-12.3.0 pluggy-1.7.0 protobuf-7.36.2 pyarrow-26.0.0 pydeck-0.9.3 pygments-2.21.0 pytest-9.1.1 python-dateutil-2.9.0.post0 python-multipart-0.0.32 referencing-0.37.0 requests-2.34.2 rpds-py-2026.9.1 six-1.17.0 starlette-1.9.0 streamlit-1.66.0 typing-extensions-4.16.0 urllib3-2.8.0 uvicorn-0.54.0 websockets-17.2
(.venv) carlarodriguez@Mac ai110-module2show-pawpal-starter % 


#Summary 
The completion of tasks being markedt completed. Pets working with the tasks to see if they are completed or still pending.Owner also connects to adding pet into the list.


Smarter Scheduling 
Testing PawPal+
A follow up and overdue tasks and completed. Also allows to view for an overlap of tasks a warning and a time and sets the time.