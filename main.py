from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

def main():
    # 1. Create an Owner
    owner = Owner(name="Alex", available_minutes=120)

    # 2. Create at least two Pets
    dog = Pet(name="Luna", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # 3. Create at least three Tasks with different times
    now = datetime.now()
    task1 = Task(
        id=1, description="Morning Walk", duration_mins=30, 
        priority="high", due_time=now + timedelta(hours=1), frequency="Daily"
    )
    task2 = Task(
        id=2, description="Feed Breakfast", duration_mins=10, 
        priority="high", due_time=now + timedelta(hours=2), frequency="Daily"
    )
    task3 = Task(
        id=3, description="Brush Fur", duration_mins=15, 
        priority="low", due_time=now + timedelta(hours=3), frequency="Weekly"
    )

    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)

    # 4. Initialize Scheduler and build schedule
    scheduler = Scheduler(owner=owner)
    raw_schedule = scheduler.build_schedule()

    # 5. Print the messy output
    print("--- RAW OUTPUT ---")
    print(raw_schedule)
    print("\n")

    # 6. Print the formatted output
    print("--- FORMATTED OUTPUT ---")
    print("Today's Schedule:")
    for pet_name, task in raw_schedule:
        # Format the datetime object into a readable string (e.g., "09:15 AM")
        time_str = task.due_time.strftime("%I:%M %p")
        print(f"[{time_str}] {pet_name}: {task.description} ({task.duration_mins} min) - Priority: {task.priority.capitalize()}")

if __name__ == "__main__":
    main()