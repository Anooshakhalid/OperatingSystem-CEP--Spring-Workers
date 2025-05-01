import random
from datetime import datetime

# Global Configuration
CRATE_CAPACITY = 12
TOTAL_FRUITS = 50

# Logger
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

# Name mapping
PICKER_NAMES = {1: "Anoosha", 2: "Laiba", 3: "Mahnoor"}

# Simple Semaphore
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

# Simple Mutex
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

# Shared Resources
tree = []
crate = []
truck = []
tree_mutex = Mutex()
crate_mutex = Mutex()
crate_full = Semaphore(0)
crate_empty = Semaphore(1)
done_flags = [False, False, False]
broadcast_done = False



# Scheduler
scheduler = []

# Picker process
def picker(picker_id):
    global broadcast_done
    picker_name = PICKER_NAMES[picker_id]
    while True:
        if broadcast_done:
            log(f"{picker_name} received broadcast. Stopping picker.", section="picker", indent=4)
            break

        if not tree_mutex.acquire(current_thread): yield
        if tree:
            fruit = tree.pop(0)
            log(f"{picker_name} picked fruit {fruit}", section="picker", indent=4)
        else:
            tree_mutex.release()
            if not broadcast_done:
                broadcast_done = True
                log(f"{picker_name} found tree empty. Broadcast: Tree is empty. Stopping all pickers.", section="picker", indent=4)
            else:
                log(f"{picker_name} received broadcast. Stopping fruit picking due to broadcast.", section="picker", indent=4)
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
