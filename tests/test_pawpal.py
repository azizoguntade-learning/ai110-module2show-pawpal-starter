import pytest
from datetime import datetime, timedelta
import sys
import os

# Ensure pytest can find the pawpal_system module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pawpal_system import Task, Pet, Owner, Scheduler

def test_sorting_correctness():
    """Verify tasks are returned in chronological order."""
    owner = Owner(name="Test Owner", available_minutes=120)
    dog = Pet(name="Luna", species="Dog", age=3)
    owner.add_pet(dog)
    
    now = datetime.now()
    # Add tasks out of order
    task_late = Task(id=1, description="Late Task", duration_mins=10, priority="low", due_time=now + timedelta(hours=3), frequency="Once")
    task_early = Task(id=2, description="Early Task", duration_mins=10, priority="low", due_time=now + timedelta(hours=1), frequency="Once")
    
    dog.add_task(task_late)
    dog.add_task(task_early)
    
    scheduler = Scheduler(owner=owner)
    all_tasks = scheduler.get_all_tasks()
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    
    # Assert the first task in the sorted list is the 'Early Task'
    assert sorted_tasks[0][1].description == "Early Task"
    assert sorted_tasks[1][1].description == "Late Task"

def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner(name="Test Owner", available_minutes=120)
    cat = Pet(name="Milo", species="Cat", age=5)
    owner.add_pet(cat)
    
    now = datetime.now()
    daily_task = Task(id=1, description="Morning Feed", duration_mins=10, priority="high", due_time=now, frequency="Daily")
    cat.add_task(daily_task)
    
    scheduler = Scheduler(owner=owner)
    
    # Complete the task
    scheduler.complete_task(pet_name="Milo", task_id=1)
    
    # Milo should now have 2 tasks (1 completed, 1 new pending)
    assert len(cat.tasks) == 2
    
    completed_task = [t for t in cat.tasks if t.id == 1][0]
    new_task = [t for t in cat.tasks if t.id != 1][0]
    
    assert completed_task.is_completed is True
    assert new_task.is_completed is False
    assert new_task.frequency == "Daily"
    # Ensure the new task is scheduled exactly 1 day later
    assert new_task.due_time == now + timedelta(days=1)

def test_conflict_detection_overlap():
    """Verify that the Scheduler flags overlapping times."""
    owner = Owner(name="Test Owner", available_minutes=120)
    dog = Pet(name="Luna", species="Dog", age=3)
    owner.add_pet(dog)
    
    now = datetime.now()
    # Task 1: 9:00 to 9:30
    task1 = Task(id=1, description="Morning Walk", duration_mins=30, priority="high", due_time=now, frequency="Once")
    dog.add_task(task1)
    
    scheduler = Scheduler(owner=owner)
    
    # Task 2: 9:15 to 9:45 (Overlaps with Task 1)
    task2 = Task(id=2, description="Grooming", duration_mins=30, priority="medium", due_time=now + timedelta(minutes=15), frequency="Once")
    
    warning = scheduler.check_conflicts(task2)
    assert warning is not None
    assert "WARNING" in warning

def test_conflict_detection_abutting():
    """Verify that tasks placed exactly back-to-back do not conflict."""
    owner = Owner(name="Test Owner", available_minutes=120)
    dog = Pet(name="Luna", species="Dog", age=3)
    owner.add_pet(dog)
    
    now = datetime.now()
    # Task 1: 9:00 to 9:30
    task1 = Task(id=1, description="Morning Walk", duration_mins=30, priority="high", due_time=now, frequency="Once")
    dog.add_task(task1)
    
    scheduler = Scheduler(owner=owner)
    
    # Task 2: Starts exactly at 9:30
    task2 = Task(id=2, description="Feeding", duration_mins=10, priority="medium", due_time=now + timedelta(minutes=30), frequency="Once")
    
    warning = scheduler.check_conflicts(task2)
    # Since they do not strictly overlap, warning should be None
    assert warning is None