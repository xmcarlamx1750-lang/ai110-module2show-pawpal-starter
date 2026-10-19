from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Carla", available_minutes=120)
    rex = Pet("Rex", "dog", age=3)
    mia = Pet("Mia", "cat", age=5)
    owner.add_pet(rex)
    owner.add_pet(mia)

    rex.add_task(Task("Morning walk", 30, priority="high", time="08:00"))
    mia.add_task(Task("Feed breakfast", 10, priority="high", time="08:00"))  # same time
    mia.add_task(Task("Brush fur", 15, priority="low", time="09:30"))

    scheduler = Scheduler(owner)
    scheduler.build_plan()
    print(scheduler.explain_plan())

    print("\nConflict check:")
    warnings = scheduler.detect_conflicts()
    if warnings:
        print("\n".join(warnings))
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()
