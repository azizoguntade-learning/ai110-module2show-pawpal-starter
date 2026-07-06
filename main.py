from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

def main():
    # Setup Owner and Pets
    owner = Owner(name="Alex", available_minutes=120)
    dog = Pet(name="Luna", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)

    now = datetime.now()
    
    # Create existing scheduled tasks
    task1 = Task(id=1, description="Morning Walk", duration_mins=30, priority="high", due_time=now + timedelta(hours=1), frequency="Daily")
    task2 = Task(id=2, description="Morning Feed", duration_mins=10, priority="high", due_time=now + timedelta(hours=2), frequency="Daily")
    task3 = Task(id=3, description="Afternoon Play", duration_mins=15, priority="low", due_time=now + timedelta(hours=3), frequency="Once")
    
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)

    # Initialize the Scheduler
    scheduler = Scheduler(owner=owner)

    print("=== TEST 1: FILTERING AND SORTING ===")
    print("Pending tasks for Luna (Sorted by Time):")
    luna_pending = scheduler.filter_tasks(is_completed=False, pet_name="Luna")
    sorted_luna = scheduler.sort_by_time(luna_pending)
    for pet_name, task in sorted_luna:
        time_str = task.due_time.strftime("%I:%M %p")
        print(f"[{time_str}] {pet_name}: {task.description} ({task.duration_mins} min)")

    print("\n=== TEST 2: RECURRING TASK GENERATION ===")
    print("[ACTION] Completing Task ID 1 (Morning Walk)...")
    scheduler.complete_task(pet_name="Luna", task_id=1)
    
    print("Completed Tasks:")
    for pet_name, task in scheduler.filter_tasks(is_completed=True):
        print(f"ID: {task.id} | {pet_name}: {task.description}")

    print("\nNew Pending Tasks (Verifying recurrence generation):")
    for pet_name, task in scheduler.filter_tasks(is_completed=False, pet_name="Luna"):
        print(f"ID: {task.id} | {pet_name}: {task.description} | Due: {task.due_time.strftime('%Y-%m-%d %I:%M %p')}")

    print("\n=== TEST 3: CONFLICT DETECTION ===")
    # Create a conflicting task set to overlap with task2
    conflicting_task = Task(id=99, description="Vet Visit", duration_mins=45, priority="high", due_time=now + timedelta(hours=2), frequency="Once")
    
    warning = scheduler.check_conflicts(conflicting_task)
    if warning:
        print(warning)
    else:
        print("No conflicts detected. Task can be scheduled.")

if __name__ == "__main__":
    main()