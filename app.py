from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

PRIORITY_BADGES = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption(
    "Plan your pets' care around the time you have: tasks are sorted by priority "
    "and start time, recurring chores renew themselves, and clashing times are flagged."
)

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=720, value=120
)

# Create the Owner once; session_state keeps it across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner
owner.name = owner_name
owner.available_minutes = int(available_minutes)


def pet_of(task: Task) -> str:
    """Name of the pet a task belongs to."""
    return next(p.name for p in owner.pets if task in p.tasks)


def task_rows(tasks: list[Task], with_order: bool = False) -> list[dict]:
    """Display-ready table rows for a list of tasks."""
    rows = []
    for i, t in enumerate(tasks, 1):
        row = {"#": i} if with_order else {}
        row.update(
            {
                "Pet": pet_of(t),
                "Task": t.title,
                "Time": t.time or "—",
                "Duration": f"{t.duration_minutes} min",
                "Priority": PRIORITY_BADGES[t.priority],
                "Repeats": t.frequency.capitalize(),
                "Due": str(t.due_date) if t.due_date else "—",
                "Status": "✅ Done" if t.completed else "⏳ Pending",
            }
        )
        rows.append(row)
    return rows


st.subheader("Pets")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species))
    st.toast(f"Added {pet_name} the {species}", icon="🐾")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.subheader("Tasks")
if owner.pets:
    with st.form("add_task", clear_on_submit=False):
        target_name = st.selectbox("Add task for", [p.name for p in owner.pets])
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        col4, col5, col6 = st.columns(3)
        with col4:
            use_time = st.checkbox("Set a start time")
        with col5:
            start_time = st.time_input("Start time", value=time(8, 0))
        with col6:
            frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])
        submitted = st.form_submit_button("Add task")

    if submitted:
        target = next(p for p in owner.pets if p.name == target_name)
        target.add_task(
            Task(
                task_title,
                int(duration),
                priority,
                time=start_time.strftime("%H:%M") if use_time else None,
                frequency=frequency,
            )
        )
        st.toast(f"Added '{task_title}' for {target_name}", icon="✅")

    scheduler = Scheduler(owner)

    pending = scheduler.filter_tasks(completed=False)
    if pending:
        labels = [f"{pet_of(t)}: {t.title}" for t in pending]
        pick_col, btn_col = st.columns([3, 1], vertical_alignment="bottom")
        with pick_col:
            choice = st.selectbox(
                "Mark a task complete", range(len(pending)), format_func=labels.__getitem__
            )
        with btn_col:
            mark_clicked = st.button("Mark complete", width="stretch")
        if mark_clicked:
            task = pending[choice]
            owner_pet = next(p for p in owner.pets if task in p.tasks)
            following = owner_pet.complete_task(task)
            if following:
                st.success(
                    f"'{task.title}' done! Next one scheduled for {following.due_date}."
                )
            else:
                st.success(f"'{task.title}' done!")

    # Metrics and conflicts are computed after any change above so they stay current.
    all_tasks = scheduler.filter_tasks()
    pending_count = len(scheduler.filter_tasks(completed=False))
    conflicts = scheduler.detect_conflicts()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pets", len(owner.pets))
    m2.metric("Pending", pending_count)
    m3.metric("Completed", len(all_tasks) - pending_count)
    m4.metric("Conflicts", len(conflicts))

    if conflicts:
        for warning in conflicts:
            st.warning(warning, icon="⚠️")
    elif all_tasks:
        st.success("No scheduling conflicts.")

    fcol1, fcol2 = st.columns(2)
    with fcol1:
        pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
    with fcol2:
        status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    shown = scheduler.filter_tasks(
        completed={"All": None, "Pending": False, "Completed": True}[status_filter],
        pet_name=None if pet_filter == "All" else pet_filter,
    )
    if shown:
        st.caption(f"Showing {len(shown)} of {len(all_tasks)} task(s), sorted by start time.")
        st.dataframe(
            task_rows(scheduler.sort_by_time(shown)),
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("No tasks match. Add one above or change the filters.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule", type="primary"):
    scheduler = Scheduler(owner)
    plan = scheduler.build_plan()
    if not plan and not scheduler.skipped:
        st.warning("No pending tasks to schedule.")
    else:
        used = sum(t.duration_minutes for t in plan)
        total = owner.available_minutes
        s1, s2, s3 = st.columns(3)
        s1.metric("Planned", len(plan))
        s2.metric("Skipped", len(scheduler.skipped))
        s3.metric("Time used", f"{used}/{total} min")
        st.progress(min(used / total, 1.0))

        if plan:
            st.success(f"Your plan for {scheduler.date} is ready.")
            st.table(task_rows(plan, with_order=True))
        if scheduler.skipped:
            st.warning(
                "Skipped (not enough time): "
                + ", ".join(f"{t.title} ({t.duration_minutes} min)" for t in scheduler.skipped)
            )
        for warning in scheduler.detect_conflicts():
            st.warning(warning, icon="⚠️")
