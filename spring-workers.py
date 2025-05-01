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
