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

```text
Today's Schedule:
[09:18 PM] Luna: Morning Walk (30 min) - Priority: High
[10:18 PM] Luna: Feed Breakfast (10 min) - Priority: High
[11:18 PM] Milo: Brush Fur (15 min) - Priority: Low

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

============================= test session starts =============================
collected 4 items

tests/test_pawpal.py::test_sorting_correctness PASSED                   [ 25%]
tests/test_pawpal.py::test_recurrence_logic PASSED                      [ 50%]
tests/test_pawpal.py::test_conflict_detection_overlap PASSED            [ 75%]
tests/test_pawpal.py::test_conflict_detection_abutting PASSED           [100%]

============================== 4 passed in 0.05s ==============================

## 📐 Smarter Scheduling Features

Implement scheduling logic + integrate Python algorithms + optimize daily plans.

| Feature | Description |
|---------|-------------|
| **Chronological Sorting** | `Scheduler.sort_by_time()` utilizes a lambda function to order tasks strictly by their `due_time` attribute. |
| **Dynamic Filtering** | `Scheduler.filter_tasks()` isolates tasks by pet name or completion status to maintain focus on pending requirements. |
| **Interval Conflict Detection** | `Scheduler.check_conflicts()` evaluates start and end times (`start < end` & `end > start`) to detect overlaps and surface warnings without crashing the application. |
| **Automated Recurrence** | `Scheduler.complete_task()` processes frequency maps (e.g., Daily, Weekly) to instantiate the next occurrence of a task automatically upon completion. |

## 📸 Demo Walkthrough

1. **Establish Profiles:** The user enters owner constraints (available time) and pet demographic data into the Streamlit UI.
2. **Populate Queue:** The user adds care activities. The system evaluates the start and end times in real-time, surfacing a UI warning if a newly added task overlaps with an existing one.
3. **Generate Plan:** The user clicks "Build Schedule." The backend executes a knapsack-lite algorithm, bypassing low-priority or excessively long tasks to maximize the owner's available minutes.
4. **Review Output:** The final chronological itinerary renders cleanly in a UI data table. 

### Sample CLI Output (`main.py`)
```text
=== TEST 1: FILTERING AND SORTING ===
Pending tasks for Luna (Sorted by Time):
[02:15 PM] Luna: Morning Walk (30 min)
[03:15 PM] Luna: Afternoon Play (15 min)

=== TEST 2: RECURRING TASK GENERATION ===
[ACTION] Completing Task ID 1 (Morning Walk)...
New Pending Tasks (Verifying recurrence generation):
ID: 4 | Luna: Morning Walk | Due: 2026-07-06 02:15 PM

=== TEST 3: CONFLICT DETECTION ===
WARNING: 'Vet Visit' conflicts with Luna's scheduled 'Morning Walk' at 02:15 PM.

