from dataclasses import dataclass, field
from datetime import date

PRIORITY_RANKS = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    completed: bool = False

    def mark_complete(self) -> None:
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
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    available_minutes: int = 120
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds and explains a daily plan. Logic to be implemented."""

    def __init__(self, owner: Owner, plan_date: date | None = None):
        self.owner = owner
        self.date = plan_date or date.today()

    def build_plan(self) -> list:
        raise NotImplementedError

    def explain_plan(self) -> str:
        raise NotImplementedError

    def fits_in_time(self, task: Task, minutes_used: int) -> bool:
        raise NotImplementedError
