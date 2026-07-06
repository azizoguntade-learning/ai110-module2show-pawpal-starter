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
        """Marks the task as completed."""
        self.is_completed = True
        return self.is_completed

    def update_priority(self, new_priority: str) -> None:
        """Updates the priority level of the task."""
        self.priority = new_priority

    def reschedule(self, new_time: datetime) -> None:
        """Reschedules the task to a new due time."""
        self.due_time = new_time

@dataclass
class Pet:
    """Represents a pet profile."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a new task to the pet's list."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Removes a task by its ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_pending_tasks(self) -> List[Task]:
        """Returns a list of tasks that are not yet completed."""
        return [t for t in self.tasks if not t.is_completed]

@dataclass
class Owner:
    """Manages multiple pets and owner-level constraints."""
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Registers a new pet profile to the owner."""
        self.pets.append(pet)

    def get_all_pet_tasks(self) -> List[Tuple[str, Task]]:
        """Aggregates all tasks across all owned pets."""
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
        """Helper to return a list of all tasks across the owner's pets."""
        return self.owner.get_all_pet_tasks()

    def build_schedule(self) -> List[Tuple[str, Task]]:
        """Builds a daily schedule based on available time and priority."""
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
        """Retrieves a sorted list of upcoming, uncompleted tasks."""
        all_tasks = self.get_all_tasks()
        upcoming = [t for t in all_tasks if not t[1].is_completed]
        return sorted(upcoming, key=lambda x: x[1].due_time)

    def check_conflicts(self, new_task: Task) -> bool:
        """Evaluates if a new task overlaps exactly with an existing schedule time."""
        for _, task in self.get_all_tasks():
            if task.due_time == new_task.due_time:
                return True
        return False

    def generate_recurring_tasks(self) -> None:
        """Spawns the next instance for daily recurring tasks."""
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