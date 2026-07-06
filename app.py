import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Please add at least one task before generating a schedule.")
    else:
        # Initialize backend objects using UI inputs
        # Assuming a default of 120 available minutes for the demo
        owner = Owner(name=owner_name, available_minutes=120) 
        pet = Pet(name=pet_name, species=species, age=2) 
        owner.add_pet(pet)

        # Convert session state dictionaries into Task objects
        now = datetime.now()
        for idx, task_data in enumerate(st.session_state.tasks):
            new_task = Task(
                id=idx + 1,
                description=task_data["title"],
                duration_mins=task_data["duration_minutes"],
                priority=task_data["priority"],
                # Staggering the due times artificially for the UI demo
                due_time=now + timedelta(hours=idx + 1), 
                frequency="Once"
            )
            pet.add_task(new_task)

        # Execute scheduling logic
        scheduler = Scheduler(owner=owner)
        daily_plan = scheduler.build_schedule()

        # Display formatted results
        st.success(f"Schedule successfully generated for {owner.name}'s pet(s)!")
        
        for p_name, task in daily_plan:
            time_str = task.due_time.strftime("%I:%M %p")
            st.info(f"**[{time_str}] {p_name}**: {task.description} ({task.duration_mins} min) | Priority: {task.priority.capitalize()}")