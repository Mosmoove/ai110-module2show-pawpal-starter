from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

def main():
    """Main entry point for PawPal+ system demo."""
    
    # Create Owner
    owner = Owner(
        name="Mohamed Awad",
        email="mohamed@example.com",
        phone="555-0123",
        time_available_daily=180  # 3 hours available
    )
    owner.set_preferences({"task_order": ["walk", "feed", "play"], "time_slots": {}})
    
    # Create Pet 1: Dog
    dog = Pet(
        pet_id="dog_001",
        name="Max",
        species="Dog",
        age=3,
        owner_id="mohamed_001",
        health_conditions=["slight allergy to chicken"]
    )
    
    # Create Pet 2: Cat
    cat = Pet(
        pet_id="cat_001",
        name="Whiskers",
        species="Cat",
        age=5,
        owner_id="mohamed_001",
        health_conditions=[]
    )
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create Tasks for Dog (Max)
    task_walk = Task(
        task_id="task_001",
        task_name="Morning Walk",
        pet_id="dog_001",
        duration=30,
        priority=1,  # Critical
        time_window=(7, 9),
        frequency="daily",
        description="Take Max for a morning walk in the park"
    )
    
    task_feed_dog = Task(
        task_id="task_002",
        task_name="Feed Dog",
        pet_id="dog_001",
        duration=10,
        priority=1,  # Critical
        time_window=(8, 20),
        frequency="daily",
        description="Feed Max his regular dog food"
    )
    
    task_play_dog = Task(
        task_id="task_003",
        task_name="Play with Dog",
        pet_id="dog_001",
        duration=45,
        priority=3,  # Medium
        time_window=(10, 18),
        frequency="daily",
        description="Interactive play session with toys"
    )
    
    # Create Tasks for Cat (Whiskers)
    task_feed_cat = Task(
        task_id="task_004",
        task_name="Feed Cat",
        pet_id="cat_001",
        duration=5,
        priority=1,  # Critical
        time_window=(8, 20),
        frequency="daily",
        description="Feed Whiskers her wet and dry food"
    )
    
    task_groom_cat = Task(
        task_id="task_005",
        task_name="Brush Cat",
        pet_id="cat_001",
        duration=20,
        priority=2,  # High
        time_window=(14, 17),
        frequency="daily",
        description="Brush Whiskers to prevent matting"
    )
    
    task_litter = Task(
        task_id="task_006",
        task_name="Clean Litter Box",
        pet_id="cat_001",
        duration=10,
        priority=2,  # High
        time_window=(9, 21),
        frequency="daily",
        description="Clean and refill litter box"
    )
    
    # Add tasks to pets
    dog.add_task(task_walk)
    dog.add_task(task_feed_dog)
    dog.add_task(task_play_dog)
    
    cat.add_task(task_feed_cat)
    cat.add_task(task_groom_cat)
    cat.add_task(task_litter)
    
    # Create scheduler and generate schedule
    scheduler = Scheduler(owner=owner, schedule_date=date.today())
    scheduler.generate_daily_schedule(owner, owner.pets)
    
    # Print schedule with enhanced formatting
    print_formatted_schedule(scheduler, owner)


def print_formatted_schedule(scheduler: Scheduler, owner: Owner):
    """Print the daily schedule in a clear, readable format."""
    
    print("\n" + "="*70)
    print(" " * 20 + "🐾 PAWPAL+ DAILY SCHEDULE 🐾")
    print("="*70)
    print(f"\n📅 Date: {scheduler.date.strftime('%A, %B %d, %Y')}")
    print(f"👤 Owner: {owner.name}")
    print(f"⏰ Available Time: {scheduler.total_available_minutes} minutes")
    print(f"🐕 Pets: {', '.join([pet.name for pet in owner.pets])}")
    
    # Scheduled tasks
    print("\n" + "-"*70)
    print("✅ SCHEDULED TASKS")
    print("-"*70)
    
    if scheduler.scheduled_tasks:
        total_duration = 0
        for i, task in enumerate(scheduler.scheduled_tasks, 1):
            total_duration += task.duration
            
            # Find pet name
            pet_name = next((pet.name for pet in owner.pets if pet.pet_id == task.pet_id), "Unknown")
            
            # Priority indicator
            priority_icons = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "⚪"}
            priority_labels = {1: "CRITICAL", 2: "HIGH", 3: "MEDIUM", 4: "LOW", 5: "OPTIONAL"}
            priority_icon = priority_icons.get(task.priority, "❓")
            priority_label = priority_labels.get(task.priority, "UNKNOWN")
            
            # Time window
            time_info = f"  {task.time_window[0]:02d}:00 - {task.time_window[1]:02d}:00" if task.time_window else "  Flexible"
            
            print(f"\n{i}. {priority_icon} {task.task_name}")
            print(f"   Pet: {pet_name}")
            print(f"   Duration: {task.duration} minutes")
            print(f"   Priority: {priority_label} ({task.priority}/5)")
            print(f"   Time Window: {time_info}")
            print(f"   Description: {task.description}")
        
        print(f"\n{'─'*70}")
        print(f"Total Scheduled Time: {total_duration} minutes")
    else:
        print("No tasks scheduled.")
    
    # Unscheduled tasks
    if scheduler.unscheduled_tasks:
        print("\n" + "-"*70)
        print("❌ UNSCHEDULED TASKS (NOT ENOUGH TIME)")
        print("-"*70)
        
        for task in scheduler.unscheduled_tasks:
            pet_name = next((pet.name for pet in owner.pets if pet.pet_id == task.pet_id), "Unknown")
            priority_labels = {1: "CRITICAL", 2: "HIGH", 3: "MEDIUM", 4: "LOW", 5: "OPTIONAL"}
            priority_label = priority_labels.get(task.priority, "UNKNOWN")
            
            print(f"\n• {task.task_name} ({task.duration} min) - {pet_name}")
            print(f"  Priority: {priority_label}")
            print(f"  Reason: Unable to fit in available time")
    
    # Scheduling reasoning
    print("\n" + "-"*70)
    print("💭 SCHEDULING REASONING")
    print("-"*70)
    print(f"\n{scheduler.get_reasoning()}")
    
    # Summary
    print("\n" + "="*70)
    print(f"Summary: {len(scheduler.scheduled_tasks)} tasks scheduled, "
          f"{len(scheduler.unscheduled_tasks)} tasks unscheduled")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()