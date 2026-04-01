from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

@dataclass
class Owner:
    """Represents a pet owner."""
    name: str
    email: str
    phone: str
    time_available_daily: int  # in minutes
    preferences: dict = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)
    
    def add_pet(self, pet: 'Pet'):
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)
    
    def remove_pet(self, pet_id: str):
        """Remove a pet by its ID."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]
    
    def update_availability(self, minutes: int):
        """Update daily available time for pet care."""
        self.time_available_daily = minutes
    
    def set_preferences(self, preferences: dict):
        """Set owner preferences for task scheduling."""
        self.preferences = preferences


@dataclass
class Pet:
    """Represents a pet."""
    pet_id: str
    name: str
    species: str
    age: int
    owner_id: str
    health_conditions: List[str] = field(default_factory=list)
    tasks: List['Task'] = field(default_factory=list)

    def add_task(self, task: 'Task'):
        """Add a task specific to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by its ID."""
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def get_tasks_by_priority(self) -> List['Task']:
        """Return tasks sorted by priority (1=critical first)."""
        return sorted(self.tasks, key=lambda t: t.priority)

    def update_health_condition(self, condition: str):
        """Add or update a health condition."""
        if condition not in self.health_conditions:
            self.health_conditions.append(condition)


@dataclass
class Task:
    """Represents a pet care task."""
    task_id: str
    task_name: str
    pet_id: str
    duration: int  # in minutes
    priority: int  # 1-5 scale (1=critical, 5=optional)
    time_window: tuple = None  # e.g., (8, 12) for 8am-12pm
    frequency: str = "daily"  # e.g., "daily", "weekly"
    is_completed: bool = False
    description: str = ""

    def mark_completed(self):
        """Mark the task as completed."""
        self.is_completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.is_completed = False

    def update_priority(self, new_priority: int):
        """Update task priority."""
        if 1 <= new_priority <= 5:
            self.priority = new_priority

    def update_duration(self, new_duration: int):
        """Update task duration in minutes."""
        self.duration = new_duration


class Scheduler:
    """Handles daily scheduling logic for pet care tasks."""
    
    def __init__(self, owner: Owner, schedule_date: date):
        self.owner = owner
        self.owner_id = owner.name
        self.date = schedule_date
        self.scheduled_tasks: List[Task] = []
        self.unscheduled_tasks: List[Task] = []
        self.schedule_reasoning: str = ""
        self.total_available_minutes: int = 0

    def generate_daily_schedule(self, owner: Owner, pet_list: List[Pet]) -> List[Task]:
        """Generate a daily schedule based on constraints and priorities."""
        self.total_available_minutes = owner.time_available_daily
        all_tasks = self._collect_all_tasks(pet_list)
        
        # Sort by priority
        sorted_tasks = self.sort_tasks_by_priority(all_tasks)
        
        # Fit tasks into available time
        self.scheduled_tasks, self.unscheduled_tasks = self.fit_tasks_in_available_time(
            sorted_tasks, 
            self.total_available_minutes
        )
        
        # Validate and generate reasoning
        self.validate_schedule()
        self._generate_reasoning()
        
        return self.scheduled_tasks

    def _collect_all_tasks(self, pet_list: List[Pet]) -> List[Task]:
        """Collect all tasks from all pets."""
        all_tasks = []
        for pet in pet_list:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (1=first, 5=last)."""
        return sorted(tasks, key=lambda t: t.priority)

    def fit_tasks_in_available_time(self, tasks: List[Task], available_minutes: int) -> tuple:
        """Fit tasks into available time, return (scheduled, unscheduled)."""
        scheduled = []
        unscheduled = []
        total_time = 0

        for task in tasks:
            if total_time + task.duration <= available_minutes:
                scheduled.append(task)
                total_time += task.duration
            else:
                unscheduled.append(task)

        return scheduled, unscheduled

    def validate_schedule(self) -> bool:
        """Validate the schedule for conflicts."""
        total_duration = sum(task.duration for task in self.scheduled_tasks)
        is_valid = total_duration <= self.total_available_minutes
        return is_valid

    def can_fit_all_tasks(self) -> bool:
        """Check if all tasks can fit in available time."""
        return len(self.unscheduled_tasks) == 0

    def get_schedule_summary(self) -> str:
        """Return a formatted summary of the daily schedule."""
        summary = f"Daily Schedule for {self.date}\n"
        summary += f"Available time: {self.total_available_minutes} minutes\n\n"
        summary += "Scheduled Tasks:\n"
        for i, task in enumerate(self.scheduled_tasks, 1):
            summary += f"{i}. {task.task_name} ({task.duration} min, Priority: {task.priority})\n"
        
        if self.unscheduled_tasks:
            summary += f"\nUnscheduled Tasks ({len(self.unscheduled_tasks)}):\n"
            for task in self.unscheduled_tasks:
                summary += f"- {task.task_name} ({task.duration} min)\n"
        
        return summary

    def get_reasoning(self) -> str:
        """Explain the scheduling decisions."""
        return self.schedule_reasoning

    def _generate_reasoning(self):
        """Generate explanation for scheduling decisions."""
        total_scheduled_time = sum(task.duration for task in self.scheduled_tasks)
        self.schedule_reasoning = (
            f"Scheduled {len(self.scheduled_tasks)} tasks using "
            f"{total_scheduled_time} of {self.total_available_minutes} available minutes. "
            f"Tasks prioritized by importance (1=critical). "
        )
        
        if self.unscheduled_tasks:
            self.schedule_reasoning += (
                f"{len(self.unscheduled_tasks)} lower-priority tasks could not fit."
            )


class PetManager:
    def __init__(self):
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a new pet to the system."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str):
        """Remove a pet by its ID."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def list_pets(self) -> List[Pet]:
        """List all pets."""
        return self.pets

    def find_pet(self, pet_id: str) -> Optional[Pet]:
        """Find a pet by its ID."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a new task to the system."""
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by its ID."""
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        return self.tasks

    def mark_task_completed(self, task_id: str):
        """Mark a task as completed by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_completed()
                break


class PawPalSystem:
    def __init__(self):
        self.owners: List[Owner] = []
        self.pet_manager = PetManager()
        self.task_manager = TaskManager()

    def add_owner(self, owner: Owner):
        """Add a new owner to the system."""
        self.owners.append(owner)

    def run(self):
        """Run the main system loop (to be implemented)."""
        pass
