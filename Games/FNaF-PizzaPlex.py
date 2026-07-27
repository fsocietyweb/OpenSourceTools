import random
import time

def start_shift():
    print("\n=== FNaF Pizza Plex ===")
    
    total_task_count = random.randint(25, 50)
    
    possible_tasks = [
        "Reboot security systems",
        "Clean animatronic parts in Parts & Service",
        "Collect Faz-Coins in the Arcade",
        "Cool down pizza ovens in the Main Kitchen",
        "Empty trash compactors in the basement",
        "Clean up party rooms",
        "Restock the Gift Shop",
        "Calibrate security cameras"
    ]

    tasks = []
    for i in range(1, total_task_count + 1):
        task_type = random.choice(possible_tasks)
        tasks.append({
            "id": i,
            "name": f"{task_type} #{i}",
            "duration": random.randint(3, 6),
            "completed": False
        })

    completed_count = 0

    while True:
        print("\n=======================================")
        print(f"=== FNaF Pizza Plex Tasks ({completed_count}/{total_task_count} Completed) ===")
        print("=======================================")
        
        for task in tasks:
            status = "[DONE]" if task["completed"] else "[PENDING]"
            print(f"{task['id']}. {task['name']} {status}")
            
        print("---------------------------------------")
        
        if completed_count == total_task_count:
            print("0. Finish Shift")
        
        choice = input("\n[Choose a Task] >> ").strip()

        if choice == "0" and completed_count == total_task_count:
            print("\n=======================================")
            print("6:00 AM - Shift completed!")
            print("=======================================")
            break

        if choice.isdigit():
            task_id = int(choice)
            selected_task = next((t for t in tasks if t["id"] == task_id), None)

            if selected_task:
                if selected_task["completed"]:
                    print("\n[!] This task is already completed!")
                else:
                    print(f"\n--- Starting: {selected_task['name']} ---")
                    duration = selected_task["duration"]
                    
                    for step in range(1, duration + 1):
                        input("Press [ENTER] to start action...")
                        
                        print("Processing... Please wait...")
                        # Spannungsvolle Pause wie im Spiel (2 bis 4 Sekunden Warten)
                        wait_time = random.uniform(2.0, 4.0)
                        time.sleep(wait_time)
                        
                        progress = int((step / duration) * 100)
                        noise_level = random.randint(15, 95)
                        
                        print(f"Progress: {progress}% | Noise Level: {noise_level}%")
                        
                        if noise_level > 80:
                            print("  [WARNING] High noise level detected!")

                    selected_task["completed"] = True
                    completed_count += 1
                    print(f"\n-> {selected_task['name']} completed!\n")
            else:
                print("\n[!] Invalid Task ID.")
        else:
            print("\n[!] Please enter a valid number.")

# Main Loop
while True:
    print("=== FNaF Pizza Plex ===")
    print("Start Shift?")
    yn = input("[Y/N]: ").strip().lower()

    if yn == "y":
        print("Starting Shift...")
        time.sleep(1)
        start_shift()
        break
    elif yn == "n":
        print("Shift canceled.")
        break
    else:
        print("Invalid input. Please enter 'Y' or 'N'.\n")