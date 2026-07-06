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

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
Task sorting |	Scheduler.sort_by_time() | Sort pending tasks chronologically using a lambda function to order the daily schedule.
Filtering | Scheduler.filter_tasks() | Filter the master list by pet name and status to isolate relevant active  tasks.
Conflict handling | Scheduler.check_conflicts() | Compare task intervals using overlap detection to return a lightweight warning message.
Recurring tasks | Scheduler.complete_task() | Calculate timedelta using frequency maps to generate the next task occurrence automatically.
## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Input owner and pet information into the UI to establish the system profiles.
2. Add multiple tasks with varying durations and priorities to populate the pending list.
3. Click the "Generate schedule" button to trigger the knapsack-lite and sorting algorithms.
4. Review the displayed chronological schedule to confirm accurate time allocation without conflicts.
5. Mark a daily task as complete to automatically generate its next occurrence for the following day.
