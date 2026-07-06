from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

def main():
    # Setup owner and pets
    owner = Owner(name="Alex", available_minutes=120)

    dog = Pet(name="Luna", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)

    now = datetime.now()
    
    # Adding tasks out of chronological order
    task1 = Task(id=1, description="Evening Walk", duration_mins=30, priority="high", due_time=now + timedelta(hours=5), frequency="Daily")
    task2 = Task(id=2, description="Morning Feed", duration_mins=10, priority="high", due_time=now + timedelta(hours=1), frequency="Daily")
    task3 = Task(id=3, description="Afternoon Play", duration_mins=15, priority="low", due_time=now + timedelta(hours=3), frequency="Once")
    task4 = Task(id=4, description="Brush Fur", duration_mins=15, priority="low", due_time=now + timedelta(hours=2), frequency="Weekly")

    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)
    cat.add_task(task4)
    
    # Mark one task as completed to test the status filter
    task2.mark_complete()

    # Initialize Scheduler
    scheduler = Scheduler(owner=owner)

    print("--- 1. FILTERING: PENDING TASKS FOR LUNA ---")
    luna_pending = scheduler.filter_tasks(is_completed=False, pet_name="Luna")
    for pet_name, task in luna_pending:
        print(f"{pet_name}: {task.description} (Completed: {task.is_completed})")

    print("\n--- 2. FILTERING: ALL COMPLETED TASKS ---")
    completed_tasks = scheduler.filter_tasks(is_completed=True)
    for pet_name, task in completed_tasks:
        print(f"{pet_name}: {task.description} (Completed: {task.is_completed})")

    print("\n--- 3. SORTING: LUNA'S PENDING TASKS BY TIME ---")
    sorted_luna_tasks = scheduler.sort_by_time(luna_pending)
    for pet_name, task in sorted_luna_tasks:
        time_str = task.due_time.strftime("%I:%M %p")
        print(f"[{time_str}] {pet_name}: {task.description}")

if __name__ == "__main__":
    main()