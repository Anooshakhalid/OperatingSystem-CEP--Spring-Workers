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




# Scheduler
scheduler = []


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



