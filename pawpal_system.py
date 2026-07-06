from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Tuple

@dataclass
class Task:
    """Represents a single care activity."""
    id: int
    description: str
    duration_mins: int
    priority: str
    due_time: datetime
    frequency: str
    is_completed: bool = False

    def mark_complete(self) -> bool:
        """Flags the task status to true to indicate completion."""
        self.is_completed = True
        return self.is_completed

    def update_priority(self, new_priority: str) -> None:
        """Modifies the priority attribute to adjust task urgency."""
        self.priority = new_priority

    def reschedule(self, new_time: datetime) -> None:
        """Alters the due time to shift the task schedule."""
        self.due_time = new_time

@dataclass
class Pet:
    """Represents a pet profile."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Appends a new task to expand the pet's schedule."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Deletes a task by ID to clear it from the schedule."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_pending_tasks(self) -> List[Task]:
        """Filters the task list to return uncompleted items."""
        return [t for t in self.tasks if not t.is_completed]

@dataclass
class Owner:
    """Manages multiple pets and owner-level constraints."""
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Registers a new pet to link it with the owner."""
        self.pets.append(pet)

    def get_all_pet_tasks(self) -> List[Tuple[str, Task]]:
        """Iterates through pets to aggregate all assigned tasks."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks

class Scheduler:
    """Manages scheduling logic, conflict detection, and task retrieval."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Tuple[str, Task]]:
        """Calls the owner method to retrieve the complete task pool."""
        return self.owner.get_all_pet_tasks()

    def build_schedule(self) -> List[Tuple[str, Task]]:
        """Sorts and filters tasks to generate a time-constrained daily plan."""
        priority_weights = {"high": 1, "medium": 2, "low": 3}
        pending_tasks = []
        
        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                pending_tasks.append((pet.name, task))
                
        # Sort tasks by priority weight, then by due time
        sorted_tasks = sorted(
            pending_tasks, 
            key=lambda x: (priority_weights.get(x[1].priority.lower(), 4), x[1].due_time)
        )
        
        schedule = []
        time_used = 0
        
        for pet_name, task in sorted_tasks:
            if time_used + task.duration_mins <= self.owner.available_minutes:
                schedule.append((pet_name, task))
                time_used += task.duration_mins
                
        return schedule

    def get_upcoming_tasks(self) -> List[Tuple[str, Task]]:
        """Sorts pending tasks chronologically to display upcoming requirements."""
        all_tasks = self.get_all_tasks()
        upcoming = [t for t in all_tasks if not t[1].is_completed]
        return sorted(upcoming, key=lambda x: x[1].due_time)

    def check_conflicts(self, new_task: Task) -> bool:
        """Compares execution times to detect schedule overlaps."""
        for _, task in self.get_all_tasks():
            if task.due_time == new_task.due_time:
                return True
        return False

    def generate_recurring_tasks(self) -> None:
        """Duplicates completed daily tasks to sustain recurring schedules."""
        for pet in self.owner.pets:
            new_tasks = []
            for task in pet.tasks:
                if task.frequency.lower() == "daily" and task.is_completed:
                    new_task = Task(
                        id=task.id + 1000, 
                        description=task.description,
                        duration_mins=task.duration_mins,
                        priority=task.priority,
                        due_time=task.due_time + timedelta(days=1),
                        frequency=task.frequency,
                        is_completed=False
                    )
                    new_tasks.append(new_task)
            pet.tasks.extend(new_tasks)