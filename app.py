import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

# Initialize the Owner object in session state only if it does not already exist
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

# Initialize a default Pet for testing purposes
if "pet_initialized" not in st.session_state:
    default_pet = Pet(name="Mochi", species="dog", age=2)
    st.session_state.owner.add_pet(default_pet)
    st.session_state.pet_initialized = True

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

# Access the active pet from memory
current_pet = st.session_state.owner.pets[0]

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task_id = len(current_pet.tasks) + 1
    
    # Instantiate the custom Task object
    new_task = Task(
        id=task_id,
        description=task_title,
        duration_mins=int(duration),
        priority=priority,
        due_time=datetime.now() + timedelta(hours=task_id), 
        frequency="Once"
    )
    
    # Add task + Update pet + Store in memory
    current_pet.add_task(new_task)
    st.success(f"Task '{task_title}' added to {current_pet.name}'s profile!")

# Read dynamically from the backend objects
if current_pet.tasks:
    st.write(f"Current tasks for {current_pet.name}:")
    
    task_display = [
        {
            "Description": t.description,
            "Duration (min)": t.duration_mins,
            "Priority": t.priority.capitalize(),
            "Due Time": t.due_time.strftime("%I:%M %p")
        } for t in current_pet.tasks
    ]
    st.table(task_display)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    current_pet = st.session_state.owner.pets[0]
    
    if not current_pet.tasks:
        st.warning("Please add at least one task before generating a schedule.")
    else:
        # Update owner and pet attributes based on the latest UI inputs
        st.session_state.owner.name = owner_name
        current_pet.name = pet_name
        current_pet.species = species
        
        # Execute scheduling logic using the persistent memory object
        scheduler = Scheduler(owner=st.session_state.owner)
        daily_plan = scheduler.build_schedule()

        # Display formatted results
        st.success(f"Schedule successfully generated for {st.session_state.owner.name}'s pet(s)!")
        
        for p_name, task in daily_plan:
            time_str = task.due_time.strftime("%I:%M %p")
            st.info(f"**[{time_str}] {p_name}**: {task.description} ({task.duration_mins} min) | Priority: {task.priority.capitalize()}")