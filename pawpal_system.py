from dataclasses import dataclass, field
from datetime import date

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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

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
        """Incomplete tasks across every pet, via Owner.get_all_tasks."""
        return [t for t in self.owner.get_all_tasks() if not t.completed]

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order by priority, then preferred time (untimed last), then shortest first."""
        return sorted(
            tasks,
            key=lambda t: (t.priority_rank(), t.time or "99:99", t.duration_minutes),
        )

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
        return "\n".join(lines)
