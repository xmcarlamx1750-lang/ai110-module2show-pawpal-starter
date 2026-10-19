from pawpal_system import Pet, Task


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
