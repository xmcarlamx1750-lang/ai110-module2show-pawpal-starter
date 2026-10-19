from dataclasses import dataclass, field, replace
from datetime import date, timedelta

PRIORITY_RANKS = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    time: str | None = None  # preferred start time, "HH:MM"
    frequency: str = "daily"  # "once", "daily", or "weekly"
    completed: bool = False
    due_date: date | None = None  # None means due whenever it is planned

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Build the next instance of a recurring task.

        Daily tasks recur after 1 day and weekly tasks after 7, counted from
        this task's due_date (or today if it has none).

        Returns:
            A new, uncompleted Task copy with the later due_date, or None if
            the frequency is "once" (or otherwise non-recurring).
        """
        days = {"daily": 1, "weekly": 7}.get(self.frequency)
        if days is None:
            return None
        base = self.due_date or date.today()
        return replace(self, completed=False, due_date=base + timedelta(days=days))

    def priority_rank(self) -> int:
        """Lower number means more urgent (high=0, medium=1, low=2)."""
        return PRIORITY_RANKS[self.priority]


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and schedule its follow-up if it recurs.

        Args:
            task: A task belonging to this pet.

        Returns:
            The newly added next occurrence, or None for one-off tasks.
        """
        task.mark_complete()
        following = task.next_occurrence()
        if following:
            self.add_task(following)
        return following

    def pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    name: str
    available_minutes: int = 120
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every pet's tasks combined into one list."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds and explains a daily plan from all of an owner's pets' tasks."""

    def __init__(self, owner: Owner, plan_date: date | None = None):
        self.owner = owner
        self.date = plan_date or date.today()
        self.plan: list[Task] = []
        self.skipped: list[Task] = []

    def get_pending_tasks(self) -> list[Task]:
        """Collect tasks that are eligible for this scheduler's plan date.

        A task is included if it is not completed and is either undated or
        due on or before the plan date (so future recurrences are held back).
        """
        return [
            t
            for t in self.owner.get_all_tasks()
            if not t.completed and (t.due_date is None or t.due_date <= self.date)
        ]

    def filter_tasks(
        self, completed: bool | None = None, pet_name: str | None = None
    ) -> list[Task]:
        """Filter tasks across the owner's pets.

        Args:
            completed: True for done tasks, False for pending, None for both.
            pet_name: Case-insensitive pet name to restrict to, or None for all pets.

        Returns:
            Matching tasks in pet order, then task order. Unlike
            get_pending_tasks, due dates are ignored.
        """
        pets = self.owner.pets
        if pet_name is not None:
            pets = [p for p in pets if p.name.lower() == pet_name.lower()]
        return [
            t
            for pet in pets
            for t in pet.tasks
            if completed is None or t.completed == completed
        ]

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order by priority, then preferred time (untimed last), then shortest first."""
        return sorted(
            tasks,
            key=lambda t: (t.priority_rank(), t.time or "99:99", t.duration_minutes),
        )

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically by preferred start time.

        Times are converted to minutes since midnight so ordering is numeric
        rather than string-based. Tasks without a time sort last. The sort is
        stable, so ties keep their input order. Returns a new list.
        """

        def minutes(t: Task) -> int:
            if not t.time:
                return 24 * 60  # after every real time of day
            hours, mins = t.time.split(":")
            return int(hours) * 60 + int(mins)

        return sorted(tasks, key=minutes)

    def detect_conflicts(self) -> list[str]:
        """Return a warning per start time shared by two or more pending tasks.

        Lightweight: exact "HH:MM" matches only (same pet or different pets),
        no overlap math. Returns messages instead of raising.
        """
        by_time: dict[str, list[tuple[str, Task]]] = {}
        for pet in self.owner.pets:
            for t in pet.pending_tasks():
                if t.time and (t.due_date is None or t.due_date <= self.date):
                    by_time.setdefault(t.time, []).append((pet.name, t))
        return [
            f"Warning: {len(group)} tasks at {time}: "
            + ", ".join(f"'{t.title}' ({name})" for name, t in group)
            for time, group in sorted(by_time.items())
            if len(group) > 1
        ]

    def fits_in_time(self, task: Task, minutes_used: int) -> bool:
        """Return True if the task fits in the owner's remaining available time."""
        return minutes_used + task.duration_minutes <= self.owner.available_minutes

    def build_plan(self) -> list[Task]:
        """Greedily fit sorted tasks into the owner's available time."""
        self.plan, self.skipped = [], []
        used = 0
        for task in self.sort_tasks(self.get_pending_tasks()):
            if self.fits_in_time(task, used):
                self.plan.append(task)
                used += task.duration_minutes
            else:
                self.skipped.append(task)
        return self.plan

    def explain_plan(self) -> str:
        """Return a readable summary of the plan and any skipped tasks."""
        if not self.plan and not self.skipped:
            self.build_plan()
        used = sum(t.duration_minutes for t in self.plan)
        lines = [
            f"Plan for {self.date} ({used}/{self.owner.available_minutes} min used):"
        ]
        for t in self.plan:
            when = f" at {t.time}" if t.time else ""
            lines.append(
                f"- {t.title}{when} ({t.duration_minutes} min, {t.priority} priority)"
            )
        if self.skipped:
            lines.append("Skipped (not enough time):")
            lines.extend(f"- {t.title} ({t.duration_minutes} min)" for t in self.skipped)
        lines.extend(self.detect_conflicts())
        return "\n".join(lines)
