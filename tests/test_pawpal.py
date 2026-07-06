import pytest
from datetime import datetime
from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    # 1. Setup
    task = Task(
        id=1,
        description="Morning Walk",
        duration_mins=30,
        priority="high",
        due_time=datetime.now(),
        frequency="Daily"
    )
    
    # 2. Pre-check
    assert task.is_completed is False
    
    # 3. Action
    task.mark_complete()
    
    # 4. Verification
    assert task.is_completed is True

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # 1. Setup
    dog = Pet(name="Luna", species="Dog", age=3)
    task = Task(
        id=2,
        description="Feed Breakfast",
        duration_mins=10,
        priority="high",
        due_time=datetime.now(),
        frequency="Daily"
    )
    
    # 2. Pre-check
    initial_count = len(dog.tasks)
    
    # 3. Action
    dog.add_task(task)
    
    # 4. Verification
    assert len(dog.tasks) == initial_count + 1
    assert task in dog.tasks