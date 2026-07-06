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

This file acts as your interactive interface. It connects your backend classes 
and scheduling logic directly to the user's browser.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Profile Inputs")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

# Access the active pet from memory
current_pet = st.session_state.owner.pets[0]
pet_name = st.text_input("Pet name", value=current_pet.name)

# Handle the species selectbox safely
species_options = ["dog", "cat", "other"]
species_idx = species_options.index(current_pet.species) if current_pet.species in species_options else 0
species = st.selectbox("Species", species_options, index=species_idx)

# Update state based on inputs
st.session_state.owner.name = owner_name
current_pet.name = pet_name
current_pet.species = species

st.markdown(f"### Add Tasks for {current_pet.name}")

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
        # Stagger the due time by the task ID for testing purposes
        due_time=datetime.now() + timedelta(hours=task_id), 
        frequency="Once"
    )
    
    # Instantiate scheduler to check for conflicts BEFORE the user commits
    scheduler = Scheduler(owner=st.session_state.owner)
    conflict_warning = scheduler.check_conflicts(new_task)
    
    # Add task to pet profile immediately
    current_pet.add_task(new_task)
    
    # Surface the backend logic to the UI
    if conflict_warning:
        st.warning(f"⚠️ {conflict_warning}")
        st.info("Task added to your queue, but please review your schedule for overlaps.")
    else:
        st.success(f"Task '{task_title}' added successfully!")

# Display current tasks dynamically from the backend objects
if current_pet.tasks:
    st.write(f"Current pending tasks for {current_pet.name}:")
    
    task_display = [
        {
            "Description": t.description,
            "Duration (min)": t.duration_mins,
            "Priority": t.priority.capitalize(),
            "Due Time": t.due_time.strftime("%I:%M %p")
        } for t in current_pet.tasks if not t.is_completed
    ]
    st.table(task_display)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate Daily Plan")
if st.button("Build Schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    
    if not current_pet.tasks:
        st.warning("Please add at least one task before generating a schedule.")
    else:
        # Trigger the Knapsack-lite algorithm
        daily_plan = scheduler.build_schedule()
        
        st.success(f"Schedule optimized for {st.session_state.owner.name}'s available time ({st.session_state.owner.available_minutes} mins)!")
        
        if daily_plan:
            # Display the sorted, filtered, and conflict-free plan
            plan_data = []
            for p_name, task in daily_plan:
                plan_data.append({
                    "Time": task.due_time.strftime("%I:%M %p"),
                    "Pet": p_name,
                    "Task": task.description,
                    "Duration": f"{task.duration_mins} min",
                    "Priority": task.priority.capitalize()
                })
            st.table(plan_data)
        else:
            st.warning("No tasks could be scheduled. Check if task durations exceed your total available time.")