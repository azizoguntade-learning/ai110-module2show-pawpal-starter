from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple, Optional

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
        pass

    def update_priority(self, new_priority: str) -> None:
        """Updates the priority level of the task."""
        pass

    def reschedule(self, new_time: datetime) -> None:
        """Reschedules the task to a new due time."""
        pass

@dataclass
class Pet:
    """Represents a pet profile."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a new task to the pet's list."""
        pass

    def remove_task(self, task_id: int) -> None:
        """Removes a task by its ID."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Returns a list of tasks that are not yet completed."""
        pass

class Scheduler:
    """Manages scheduling logic, conflict detection, and task retrieval."""
    def __init__(self):
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Registers a new pet profile to the scheduler."""
        pass

    def get_all_tasks(self) -> List[Tuple[str, Task]]:
        """Helper to return a list of all tasks across all pets."""
        pass

    def build_schedule(self, available_minutes: int) -> List[Task]:
        """Builds a daily schedule based on constraints like available time."""
        pass

    def get_upcoming_tasks(self) -> List[Task]:
        """Retrieves a sorted list of upcoming tasks."""
        pass

    def check_conflicts(self, new_task: Task) -> bool:
        """Evaluates if a new task overlaps with the existing schedule."""
        pass

    def generate_recurring_tasks(self) -> None:
        """Spawns the next instance for recurring tasks."""
        pass