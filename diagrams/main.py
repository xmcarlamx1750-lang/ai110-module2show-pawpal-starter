import sys
from pathlib import Path

# pawpal_system.py lives in the project root, one level above this file
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner("Carla", available_minutes=45)

rex = Pet("Rex", "dog", age=3)
mochi = Pet("Mochi", "cat", age=5)
owner.add_pet(rex)
owner.add_pet(mochi)

rex.add_task(Task("Morning walk", 20, "high", "exercise", time="08:00"))
mochi.add_task(Task("Feed breakfast", 5, "high", "feeding", time="07:30"))
mochi.add_task(Task("Play with wand toy", 15, "low", "enrichment"))
rex.add_task(Task("Brush coat", 15, "medium", "grooming"))

scheduler = Scheduler(owner)
scheduler.build_plan()
print(scheduler.explain_plan())
