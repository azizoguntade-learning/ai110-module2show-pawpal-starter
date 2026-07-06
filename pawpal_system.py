from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

    def get_all_pet_tasks(self, pet_name: Optional[str] = None) -> List[Tuple[str, Task]]:
        """Iterates through pets to aggregate assigned tasks, optionally filtering by pet name."""
        all_tasks = []
        for pet in self.pets:
            if pet_name and pet.name != pet_name:
                continue
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks


class Scheduler:
    """Manages scheduling logic, conflict detection, and task retrieval."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self, pet_name: Optional[str] = None) -> List[Tuple[str, Task]]:
        """Calls the owner method to retrieve the complete or filtered task pool."""
        return self.owner.get_all_pet_tasks(pet_name)

    def build_schedule(self, target_date: Optional[datetime.date] = None) -> List[Tuple[str, Task]]:
        """Sorts and filters tasks to generate a time-constrained daily plan free of overlaps."""
        if target_date is None:
            target_date = datetime.today().date()
            
        priority_weights = {"high": 1, "medium": 2, "low": 3}
        pending_tasks = []
        
        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                if task.due_time.date() == target_date:
                    pending_tasks.append((pet.name, task))
                
        # Sort tasks by priority weight, then by due time
        sorted_tasks = sorted(
            pending_tasks, 
            key=lambda x: (priority_weights.get(x[1].priority.lower(), 4), x[1].due_time)
        )
        
        schedule = []
        time_used = 0
        
        # Knapsack-lite approach: continues evaluating remaining tasks even if a prior task exceeded time constraints
        for pet_name, task in sorted_tasks:
            if time_used + task.duration_mins <= self.owner.available_minutes:
                # Interval overlap detection against already scheduled tasks
                if not self._has_schedule_conflict(task, schedule):
                    schedule.append((pet_name, task))
                    time_used += task.duration_mins
                
        return schedule

    def _has_schedule_conflict(self, new_task: Task, current_schedule: List[Tuple[str, Task]]) -> bool:
        """Compares interval times to detect schedule overlaps."""
        new_start = new_task.due_time
        new_end = new_start + timedelta(minutes=new_task.duration_mins)
        
        for _, scheduled_task in current_schedule:
            sched_start = scheduled_task.due_time
            sched_end = sched_start + timedelta(minutes=scheduled_task.duration_mins)
            
            if new_start < sched_end and sched_start < new_end:
                return True
        return False

    def check_conflicts(self, new_task: Task) -> bool:
        """Evaluates a single new task against all pending tasks for interval overlaps."""
        return self._has_schedule_conflict(new_task, self.get_upcoming_tasks())

    def get_upcoming_tasks(self) -> List[Tuple[str, Task]]:
        """Sorts pending tasks chronologically to display upcoming requirements."""
        all_tasks = self.get_all_tasks()
        upcoming = [t for t in all_tasks if not t[1].is_completed]
        return sorted(upcoming, key=lambda x: x[1].due_time)

    def sort_by_time(self, task_list: List[Tuple[str, Task]]) -> List[Tuple[str, Task]]:
        """Sorts tasks chronologically by their due time."""
        return sorted(task_list, key=lambda x: x[1].due_time)

    def filter_tasks(self, is_completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Tuple[str, Task]]:
        """Filters tasks by completion status and/or pet name."""
        filtered = self.get_all_tasks(pet_name=pet_name)
        
        if is_completed is not None:
            filtered = [item for item in filtered if item[1].is_completed == is_completed]
            
        return filtered

    def _get_next_id(self) -> int:
        """Scans existing tasks to generate the next unique task ID."""
        all_tasks = self.get_all_tasks()
        if not all_tasks:
            return 1
        return max(task.id for _, task in all_tasks) + 1

    def generate_recurring_tasks(self) -> None:
        """Duplicates completed recurring tasks to sustain schedules."""
        frequency_map = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1)
        }
        
        for pet in self.owner.pets:
            new_tasks = []
            for task in pet.tasks:
                freq_key = task.frequency.lower()
                if freq_key in frequency_map and task.is_completed:
                    new_task = Task(
                        id=self._get_next_id() + len(new_tasks), 
                        description=task.description,
                        duration_mins=task.duration_mins,
                        priority=task.priority,
                        due_time=task.due_time + frequency_map[freq_key],
                        frequency=task.frequency,
                        is_completed=False
                    )
                    new_tasks.append(new_task)
            pet.tasks.extend(new_tasks)