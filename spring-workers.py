#CLASSICAL SYNCHRONIZATION PROBLEM

import random
from datetime import datetime



# --------------- GLOBAL CONFIGURATION ---------------
# Constants
CRATE_CAPACITY = 12
TOTAL_FRUITS = 50



# --------------- LOGGER FUNCTION ---------------
def log(msg, section="", indent=0):
    timestamp = datetime.now().strftime("%H:%M:%S")
    label = {
        "picker": "\n*************   PICKER ACTIVITY   *************",
        "loader": "\n*************   LOADER ACTIVITY   *************",
        "tree": "\n*************   FRUIT TREE   *************",
        "final": "\n*************   FINAL SUMMARY   *************"
    }.get(section, "")
    if label:
        print(label)
    print(f"{' ' * indent}[{timestamp}] {msg}")



# --------------- NAME MAPPING FOR PICKERS ---------------
PICKER_NAMES = {1: "Anoosha", 2: "Laiba", 3: "Mahnoor"}



# --------------- SIMPLE SEMAPHORE CLASS ---------------
class Semaphore:
    def __init__(self, value=0):
        self.value = value
        self.queue = []

    def wait(self, current):
        if self.value > 0:
            self.value -= 1
            return True
        else:
            self.queue.append(current)
            return False

    def signal(self):
        if self.queue:
            next_thread = self.queue.pop(0)
            scheduler.insert(0, next_thread)
        else:
            self.value += 1



# --------------- SIMPLE MUTEX CLASS ---------------
class Mutex:
    def __init__(self):
        self.locked = False
        self.queue = []

    def acquire(self, current):
        if not self.locked:
            self.locked = True
            return True
        else:
            self.queue.append(current)
            return False

    def release(self):
        if self.queue:
            next_thread = self.queue.pop(0)
            scheduler.insert(0, next_thread)
        else:
            self.locked = False



# --------------- SHARED RESOURCES ---------------
tree = []
crate = []
truck = []
tree_mutex = Mutex()
crate_mutex = Mutex()
crate_full = Semaphore(0)
crate_empty = Semaphore(1)
done_flags = [False, False, False]



# --------------- SCHEDULER ---------------
# It is an array(list) that manages pickers and loader one by one, giving each a turn until all are done
scheduler = []



# --------------- PICKER PROCESS ---------------
def picker(picker_id):
    picker_name = PICKER_NAMES[picker_id]
    while True:
        if not tree_mutex.acquire(current_thread): yield
        if tree:
            fruit = tree.pop(0)
            log(f"{picker_name} picked fruit {fruit}", section="picker", indent=4)
        else:
            tree_mutex.release()
            log(f"{picker_name} found tree empty. Stopping fruit picking due to broadcast.", section="picker", indent=4)
            break
        tree_mutex.release()

        while crate_empty.value == 0:
            yield

        if not crate_mutex.acquire(current_thread): yield
        crate.append(fruit)
        log(f"{picker_name} placed fruit {fruit} in crate ({len(crate)}/{CRATE_CAPACITY})\n", indent=6)
        if len(crate) == CRATE_CAPACITY:
            log(f"{picker_name} found crate full. Notifying loader", indent=6)
            crate_empty.value = 0
            crate_full.signal()
        crate_mutex.release()

        for _ in range(random.randint(1, 2)):
            yield

    done_flags[picker_id - 1] = True
    log(f"{picker_name} completed. Tree is bare.", indent=4)
    yield



# --------------- LOADER PROCESS ---------------
def loader():
    crate_count = 0
    while True:
        if not crate_full.wait(current_thread): yield

        if not crate_mutex.acquire(current_thread): yield
        if len(crate) == CRATE_CAPACITY:
            log("Loader triggered! Crate is full. Loading it to truck", section="loader", indent=2)
            truck.append(list(crate))
            crate_count += 1
            crate.clear()
            log(f"Loader placed crate in truck (Total crates: {crate_count})\n", indent=4)
            crate_empty.signal()
        crate_mutex.release()

        if all(done_flags) and not tree:
            break
        yield

    # Handle final partial crate
    if crate:
        if not crate_mutex.acquire(current_thread): yield
        log("Loader detected partially filled crate after pickers finished.", section="loader", indent=2)
        truck.append(list(crate))
        crate_count += 1
        crate.clear()
        log(f"Final crate placed in truck (Total crates: {crate_count})", indent=4)
        crate_mutex.release()

    log("Loader completed all operations. Exiting.\n", section="loader", indent=2)
    yield



# --------------- MAIN FUNCTION ---------------
def main():


    # --------------- START SIMULATION ---------------
    print("┌---------------------------------------------------------┐")
    print("           🌸 SPRING WORKERS SIMULATION START 🌸          ")
    print("└---------------------------------------------------------┘")


    # Announcing the mango season start and listing pickers
    print("\nYay! Mango season has started, it's time to pluck the mangoes from the tree!")
    print("Three pickers are:\nP1 - Anoosha\nP2 - Laiba\nP3 - Mahnoor\n")



    # --------------- INITIALIZING FRUIT TREE ---------------
    global tree
    # Populate the tree with fruits (numbers from 1 to TOTAL_FRUITS)
    tree = [i + 1 for i in range(TOTAL_FRUITS)]

    # Log the initial fruit status on the tree
    log(f"Fruits on tree: {tree}\n", section="tree")



    # --------------- CREATE AND SCHEDULE PROCESSES ---------------
    global scheduler
    # Create and schedule the picker processes and loader process
    scheduler = [
        picker(1),  # Picker 1 (Anoosha)
        picker(2),  # Picker 2 (Laiba)
        picker(3),  # Picker 3 (Mahnoor)
        loader()    # Loader process
    ]



    # --------------- SIMULATION LOOP ---------------
    # Run the scheduled processes until all are completed
    while scheduler:
        current = scheduler.pop(0)  # Get the next process from the scheduler
        global current_thread
        current_thread = current
        try:
            next(current)  # Execute the next step of the process
            scheduler.append(current)  # Re-add the process to scheduler if it's still active
        except StopIteration:
            pass  # Process has completed, do not re-add it



    # --------------- FINAL SUMMARY ---------------
    log("", section="final")
    # Log the contents of each crate in the truck
    for i, crate in enumerate(truck, 1):
        print(f"Crate {i}: {crate} ({len(crate)} fruits)")


    # Print total number of crates in the truck
    print(f"\nTotal crates in truck: {len(truck)}")


    # Final message
    print("All fruits picked and loaded successfully.\n")


# --------------- START THE SIMULATION ---------------
main()
