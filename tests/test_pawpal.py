from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task

TODAY = date(2026, 3, 10)


def make_scheduler(*pets, minutes=120, plan_date=TODAY):
    owner = Owner("Sam", available_minutes=minutes)
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner, plan_date)


def test_mark_complete_changes_status():
    task = Task("Morning walk", 20)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Rex", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Morning walk", 20))

    assert len(pet.tasks) == 1


# --- Sorting ---


def test_sort_by_time_orders_numerically_and_puts_untimed_last():
    sched = make_scheduler()
    tasks = [
        Task("untimed", 5),
        Task("late", 5, time="23:59"),
        Task("midnight", 5, time="00:00"),
        Task("morning", 5, time="09:00"),
        Task("mid", 5, time="10:30"),
    ]

    result = [t.title for t in sched.sort_by_time(tasks)]

    assert result == ["midnight", "morning", "mid", "late", "untimed"]


def test_sort_by_time_is_stable_for_ties_and_does_not_mutate_input():
    sched = make_scheduler()
    a = Task("a", 5, time="08:00")
    b = Task("b", 5, time="08:00")
    c = Task("c", 5, time="07:00")
    original = [a, b, c]

    result = sched.sort_by_time(original)

    assert result == [c, a, b]
    assert original == [a, b, c]


def test_sort_tasks_priority_beats_time_then_duration_breaks_ties():
    sched = make_scheduler()
    low_early = Task("low early", 5, priority="low", time="07:00")
    high_late = Task("high late", 30, priority="high", time="18:00")
    high_late_short = Task("high late short", 10, priority="high", time="18:00")

    result = sched.sort_tasks([low_early, high_late, high_late_short])

    assert result == [high_late_short, high_late, low_early]


def test_sorting_empty_list_returns_empty_list():
    sched = make_scheduler()

    assert sched.sort_tasks([]) == []
    assert sched.sort_by_time([]) == []


# --- Recurring tasks ---


def test_daily_task_completion_creates_next_day_task():
    pet = Pet("Rex", "dog")
    task = Task("Walk", 20, frequency="daily", due_date=TODAY)
    pet.add_task(task)

    following = pet.complete_task(task)

    assert task.completed is True
    assert following is not None
    assert following.completed is False
    assert following.due_date == TODAY + timedelta(days=1)
    assert following in pet.tasks and len(pet.tasks) == 2


def test_weekly_task_completion_creates_task_seven_days_later():
    pet = Pet("Rex", "dog")
    task = Task("Bath", 30, frequency="weekly", due_date=TODAY)
    pet.add_task(task)

    following = pet.complete_task(task)

    assert following.due_date == TODAY + timedelta(days=7)


def test_once_task_does_not_recur():
    pet = Pet("Rex", "dog")
    task = Task("Vet visit", 60, frequency="once", due_date=TODAY)
    pet.add_task(task)

    assert pet.complete_task(task) is None
    assert len(pet.tasks) == 1


def test_unknown_frequency_does_not_recur():
    assert Task("Trim nails", 10, frequency="monthly").next_occurrence() is None


def test_recurrence_without_due_date_counts_from_today():
    following = Task("Walk", 20, frequency="daily").next_occurrence()

    assert following.due_date == date.today() + timedelta(days=1)


def test_recurrence_crosses_month_and_year_boundaries():
    new_year = Task("Walk", 20, due_date=date(2026, 12, 31)).next_occurrence()
    leap_day = Task("Walk", 20, due_date=date(2028, 2, 28)).next_occurrence()

    assert new_year.due_date == date(2027, 1, 1)
    assert leap_day.due_date == date(2028, 2, 29)


# --- Scheduler: recurrence interactions ---


def test_next_occurrence_is_held_back_until_its_due_date():
    pet = Pet("Rex", "dog")
    task = Task("Walk", 20, frequency="daily", due_date=TODAY)
    pet.add_task(task)
    pet.complete_task(task)

    today_plan = make_scheduler(pet, plan_date=TODAY).build_plan()
    tomorrow_plan = make_scheduler(
        pet, plan_date=TODAY + timedelta(days=1)
    ).build_plan()

    assert today_plan == []
    assert [t.due_date for t in tomorrow_plan] == [TODAY + timedelta(days=1)]


def test_overdue_tasks_are_included_and_completed_tasks_are_not():
    pet = Pet("Rex", "dog")
    overdue = Task("Overdue", 10, due_date=TODAY - timedelta(days=3))
    done = Task("Done", 10, completed=True)
    pet.tasks.extend([overdue, done])

    assert make_scheduler(pet).get_pending_tasks() == [overdue]


# --- Scheduler: conflicts ---


def test_detect_conflicts_flags_same_time_across_pets():
    rex, mia = Pet("Rex", "dog"), Pet("Mia", "cat")
    rex.add_task(Task("Walk", 20, time="08:00"))
    mia.add_task(Task("Feed", 5, time="08:00"))

    warnings = make_scheduler(rex, mia).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0] and "Rex" in warnings[0] and "Mia" in warnings[0]


def test_detect_conflicts_ignores_untimed_completed_and_future_tasks():
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Untimed A", 5))
    pet.add_task(Task("Untimed B", 5))
    pet.add_task(Task("Done", 5, time="09:00", completed=True))
    pet.add_task(Task("Active", 5, time="09:00"))
    pet.add_task(Task("Future", 5, time="09:00", due_date=TODAY + timedelta(days=1)))

    assert make_scheduler(pet).detect_conflicts() == []


def test_detect_conflicts_misses_overlap_without_identical_start_times():
    # Known limitation: only exact "HH:MM" matches are detected.
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Long walk", 60, time="09:00"))
    pet.add_task(Task("Feed", 5, time="09:30"))

    assert make_scheduler(pet).detect_conflicts() == []


def test_detect_conflicts_with_no_tasks_returns_empty_list():
    assert make_scheduler(Pet("Rex", "dog")).detect_conflicts() == []


# --- Scheduler: time budget ---


def test_task_that_exactly_fills_budget_fits_but_one_minute_over_is_skipped():
    pet = Pet("Rex", "dog")
    exact = Task("Exact", 60, priority="high")
    over = Task("Over", 1, priority="low")
    pet.tasks.extend([exact, over])

    sched = make_scheduler(pet, minutes=60)
    sched.build_plan()

    assert sched.plan == [exact]
    assert sched.skipped == [over]


def test_greedy_plan_skips_big_task_but_still_schedules_later_small_ones():
    pet = Pet("Rex", "dog")
    first = Task("First", 40, priority="high")
    big = Task("Big", 50, priority="medium")
    small = Task("Small", 10, priority="low")
    pet.tasks.extend([first, big, small])

    sched = make_scheduler(pet, minutes=60)
    sched.build_plan()

    assert sched.plan == [first, small]
    assert sched.skipped == [big]


def test_zero_available_minutes_skips_everything():
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", 20))

    sched = make_scheduler(pet, minutes=0)
    sched.build_plan()

    assert sched.plan == [] and len(sched.skipped) == 1


def test_scheduler_with_no_pets_or_tasks_builds_empty_plan_and_explains():
    sched = make_scheduler()

    assert sched.build_plan() == []
    assert "0/120 min used" in sched.explain_plan()


# --- Scheduler: filtering ---


def test_filter_tasks_by_pet_name_is_case_insensitive_and_by_completion():
    rex, mia = Pet("Rex", "dog"), Pet("Mia", "cat")
    walk = Task("Walk", 20, completed=True)
    feed = Task("Feed", 5)
    nap = Task("Nap", 5)
    rex.tasks.extend([walk, feed])
    mia.tasks.append(nap)
    sched = make_scheduler(rex, mia)

    assert sched.filter_tasks(pet_name="REX") == [walk, feed]
    assert sched.filter_tasks(completed=False) == [feed, nap]
    assert sched.filter_tasks(pet_name="Ghost") == []
    assert sched.filter_tasks() == [walk, feed, nap]
