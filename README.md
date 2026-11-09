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

Running `python3 main.py` generates a daily plan and flags scheduling conflicts:

```
Plan for 2026-11-08 (55/120 min used):
- Feed breakfast at 08:00 (10 min, high priority)
- Morning walk at 08:00 (30 min, high priority)
- Brush fur at 09:30 (15 min, low priority)
Warning: 2 tasks at 08:00: 'Morning walk' (Rex), 'Feed breakfast' (Mia)

Conflict check:
Warning: 2 tasks at 08:00: 'Morning walk' (Rex), 'Feed breakfast' (Mia)
```

The Streamlit app (`streamlit run app.py`) shows the same plan and conflict warnings in the browser.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
collected 23 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  4%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [  8%]
tests/test_pawpal.py::test_sort_by_time_orders_numerically_and_puts_untimed_last PASSED [ 13%]
tests/test_pawpal.py::test_sort_by_time_is_stable_for_ties_and_does_not_mutate_input PASSED [ 17%]
tests/test_pawpal.py::test_sort_tasks_priority_beats_time_then_duration_breaks_ties PASSED [ 21%]
tests/test_pawpal.py::test_sorting_empty_list_returns_empty_list PASSED  [ 26%]
tests/test_pawpal.py::test_daily_task_completion_creates_next_day_task PASSED [ 30%]
tests/test_pawpal.py::test_weekly_task_completion_creates_task_seven_days_later PASSED [ 34%]
tests/test_pawpal.py::test_once_task_does_not_recur PASSED               [ 39%]
tests/test_pawpal.py::test_unknown_frequency_does_not_recur PASSED       [ 43%]
tests/test_pawpal.py::test_recurrence_without_due_date_counts_from_today PASSED [ 47%]
tests/test_pawpal.py::test_recurrence_crosses_month_and_year_boundaries PASSED [ 52%]
tests/test_pawpal.py::test_next_occurrence_is_held_back_until_its_due_date PASSED [ 56%]
tests/test_pawpal.py::test_overdue_tasks_are_included_and_completed_tasks_are_not PASSED [ 60%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time_across_pets PASSED [ 65%]
tests/test_pawpal.py::test_detect_conflicts_ignores_untimed_completed_and_future_tasks PASSED [ 69%]
tests/test_pawpal.py::test_detect_conflicts_misses_overlap_without_identical_start_times PASSED [ 73%]
tests/test_pawpal.py::test_detect_conflicts_with_no_tasks_returns_empty_list PASSED [ 78%]
tests/test_pawpal.py::test_task_that_exactly_fills_budget_fits_but_one_minute_over_is_skipped PASSED [ 82%]
tests/test_pawpal.py::test_greedy_plan_skips_big_task_but_still_schedules_later_small_ones PASSED [ 86%]
tests/test_pawpal.py::test_zero_available_minutes_skips_everything PASSED [ 91%]
tests/test_pawpal.py::test_scheduler_with_no_pets_or_tasks_builds_empty_plan_and_explains PASSED [ 95%]
tests/test_pawpal.py::test_filter_tasks_by_pet_name_is_case_insensitive_and_by_completion PASSED [100%]

============================== 23 passed in 0.03s ==============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting |Complete taks that are priority | Start time and mins left |

| Filtering | Completion status|  skip tasks if time runs out |

| Conflict handling | Skip if theres still time to leave at the end| overlapping time slots |
| Recurring tasks |Skip until the end  |  daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Start the app 
2. Enter the owner name and the minutes available for pet care today.
3. Enter a name for the pet, choose a species (dog, cat, other) and click add pet
4.   Pick the pet, then enter a title, duration, and priority (low, medium, high).a
5. Check if theres confllict. If two tasks share a start time, a ⚠️ warning appears. Otherwise you see "No scheduling conflicts."
6. Check the task list. Observe if its  pending and completed.
7. Select a task and click if completed. Recurring tasks are rescheduled automatically.
8. Click generate schedule to get an ordered plan that fits your available time. Any tasks that don't fit or that conflict are flagged with warnings.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->



#Summary 
The completion of tasks being marked completed or still pending. Owner also connects to adding pets into the list.
Also allowing for a time limit for a task to be completed and if its daily or weekly.
