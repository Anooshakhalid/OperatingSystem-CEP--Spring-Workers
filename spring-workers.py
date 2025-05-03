# Group Members:
# Mahnoor Zia (CS-22101)
# Anoosha Khalid (CS-22104)
# Laiba Iqrar (CS-22112)


import threading
import time
import random
from datetime import datetime



# ----------------------------- GLOBAL CONFIGURATION --------------------------
CRATE_CAPACITY = 12
TOTAL_FRUITS = 55



# ----------------------------- COLORS FOR PRINTING ----------------------------------------
COLOR_PINK = "\033[38;5;213m"
COLOR_BRIGHT_WHITE = "\033[97m"
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"



# ----------------------------- LOGGER FUNCTION FOR TRACKING--------------------------------
def log(message, section="", indent=0):
    timestamp = datetime.now().strftime("%H:%M:%S")
    section_labels = {
        "picker": f"\n{COLOR_BLUE}[ PICKER ACTIVITY ]{COLOR_RESET}",
        "loader": f"\n{COLOR_GREEN}[ LOADER ACTIVITY ]{COLOR_RESET}",
        "tree": f"\n{COLOR_CYAN}[ FRUIT TREE ]{COLOR_RESET}",
        "final": f"\n{COLOR_YELLOW}[ FINAL SUMMARY ]{COLOR_RESET}"
    }
    label = section_labels.get(section, "")
    if label:
        print(label)
    print(f"{' ' * indent}{COLOR_YELLOW}[{timestamp}]{COLOR_RESET} {message}")



# ---------------------------- SHARED RESOURCES ----------------------------------
tree = list(range(1, TOTAL_FRUITS + 1))
crate = []
truck = []

mutex = threading.Lock()
semaphore_full = threading.Semaphore(0)       # Loader waits on this when crate is full
semaphore_space = threading.Semaphore(0)      # Pickers wait when crate is full

pickers = 3
pickers_in_critical_section = 0



# ---------------------------- PICKER THREAD --------------------------------------
def picker(picker_id):
    global pickers, pickers_in_critical_section
    picker_names = {1: "Anoosha", 2: "Laiba", 3: "Mahnoor"}
    picker_name = picker_names[picker_id]

    while True:
        mutex.acquire()
        pickers_in_critical_section += 1

        if not tree:
            pickers_in_critical_section -= 1
            pickers -= 1
            log(f"{picker_name} has finished picking and is exiting.", section="picker", indent=4)
            print(" " * 4 + "Tree is bare.")

            if len(crate) > 0:
                semaphore_full.release()  # Notify loader in case it's the final crate
            mutex.release()
            return


        if len(crate) == CRATE_CAPACITY:
            pickers_in_critical_section -= 1
            mutex.release()
            semaphore_space.acquire()  # Wait for loader to clear crate
            continue


        fruit = tree.pop(0)
        crate.append(fruit)
        log(f"{picker_name} picked fruit {fruit}.", section="picker", indent=4)
        print(" " * 4 + f"Current crate size: {len(crate)}/{CRATE_CAPACITY}")


        if len(crate) == CRATE_CAPACITY:
            log(f"{picker_name} has filled the crate with {CRATE_CAPACITY} fruits.", section="picker", indent=4)
            print(" " * 4 + "Found crate full. Notifying loader.")
            semaphore_full.release()

        pickers_in_critical_section -= 1
        mutex.release()
        time.sleep(random.uniform(0.05, 0.2))



# ---------------------------- LOADER THREAD --------------------------------------
def loader():
    while True:
        semaphore_full.acquire()
        mutex.acquire()

        if len(crate) == CRATE_CAPACITY:
            log("Loader triggered! Crate is full.", section="loader", indent=2)
            print(" " * 4 + "Loading it to truck...")
            truck.append(crate[:])
            crate.clear()
            for _ in range(pickers):  # Wake up all pickers waiting
                semaphore_space.release()
            mutex.release()
            time.sleep(0.2)
            continue

        if pickers == 0 and pickers_in_critical_section == 0 and crate:
            log("Loader detected partially filled crate after pickers finished.", section="loader", indent=2)
            print(" " * 4 + "Loader is moving the final partial crate to the truck.")
            truck.append(crate[:])
            crate.clear()
            log("Loader has completed all operations and is exiting.", section="loader", indent=2)
            mutex.release()
            return

        if pickers == 0 and pickers_in_critical_section == 0 and not crate:
            log("Loader has completed all operations and is exiting.", section="loader", indent=2)
            mutex.release()
            return

        mutex.release()
        time.sleep(0.1)



# ---------------------------- MAIN --------------------------------------
def main():
    print("\n┌────────────────────────────────────────────────────────────┐")
    print(f"          {COLOR_PINK} 🌸 SPRING WORKERS SIMULATION START 🌸 {COLOR_RESET}")
    print("└────────────────────────────────────────────────────────────┘")

    print("\nYay! Mango season has started, it's time to pluck the mangoes from the tree!")
    print("Pickers: 1 - Anoosha | 2 - Laiba | 3 - Mahnoor\n")

    log(f"Fruits available on the tree: ", section="tree")
    for i in range(0, len(tree), 10):
        print(" " * 4 + ' '.join(map(str, tree[i:i + 10])))

    picker_threads = [threading.Thread(target=picker, args=(i,)) for i in range(1, 4)]
    loader_thread = threading.Thread(target=loader)

    for t in picker_threads:
        t.start()
    loader_thread.start()

    for t in picker_threads:
        t.join()
    loader_thread.join()

    log("", section="final")



    # printing the summary
    print("\nFruits in the Truck (Boxed in 12 per row):")
    for idx, crate in enumerate(truck, 1):
        print(f"\n[ Crate {idx} ]")
        print(f"{COLOR_GREEN}┌────────────────────────────────────────────┐{COLOR_RESET}")
        for i in range(0, len(crate), 12):
            fruits_row = ' '.join(map(str, crate[i:i+12]))
            print(f" {fruits_row:<40} ")
        print(f"{COLOR_GREEN}└────────────────────────────────────────────┘{COLOR_RESET}")
        print(f"({len(crate)} fruits)")

    print(f"\nTotal crates loaded: {len(truck)}")
    print(f"{COLOR_GREEN}Spring harvest has been successfully completed. Thank you, workers!{COLOR_RESET}\n")



# ---------------------------- START THE SIMULATION --------------------------------------
if __name__ == '__main__':
    main()
