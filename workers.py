# Group Members: 
# Mahnoor Zia (CS-22101), Anoosha Khalid (CS-22104), Laiba Iqrar (CS-22112)
# OS Project: Fruit Harvest Synchronization
# GitHub: github.com/Anooshakhalid/OperatingSystem-CEP--Spring-Workers

import threading
import time
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Configuration (tuned during testing)
CRATE_CAPACITY = 12
TOTAL_FRUITS = 55  
NUM_PICKERS = 3

# Shared resources
fruit_tree = list(range(1, TOTAL_FRUITS + 1))
current_crate = []
truck = []
active_pickers = NUM_PICKERS
pick_timestamps = []  # For time analysis
crate_history = []     # For crate analysis

# Synchronization primitives
tree_lock = threading.Lock()
crate_full = threading.Semaphore(0)
crate_available = threading.Semaphore(0)

def log_action(message, category="PICKER"):
    """Custom logger we developed during debugging"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {category:8} => {message}")

def picker_worker(worker_id):
    global active_pickers
    worker_names = {1: "Anoosha", 2: "Laiba", 3: "Mahnoor"}
    name = worker_names[worker_id]
    
    # Added retry counter for debugging
    retries = 0  
    
    while True:
        with tree_lock:
            # Exit condition
            if not fruit_tree:
                active_pickers -= 1
                log_action(f"{name} exits - tree empty", "EXIT")
                if current_crate:
                    crate_full.release()  # Final crate
                return
            
            # Crate full handling (this was tricky!)
            if len(current_crate) == CRATE_CAPACITY:
                crate_available.acquire()
                
            # Main picking logic
            fruit = fruit_tree.pop(0)
            current_crate.append(fruit)
            
            # Data collection for visualization
            pick_timestamps.append(time.time())
            
            log_action(f"{name} picked {fruit} (Crate: {len(current_crate)}/{CRATE_CAPACITY})", "PICK")
            
            # Crate management
            if len(current_crate) == CRATE_CAPACITY:
                log_action(f"{name} signaled full crate", "SIGNAL")
                crate_full.release()
                
        # Randomized delay to prevent starvation
        time.sleep(random.uniform(0.1, 0.3))

def loader_worker():
    crate_counter = 1
    while True:
        crate_full.acquire()
        
        with tree_lock:
            if len(current_crate) == CRATE_CAPACITY:
                # Record crate status before emptying
                crate_history.append({
                    'time': time.time(),
                    'count': CRATE_CAPACITY,
                    'type': 'full'
                })
                
                truck.append(current_crate.copy())
                current_crate.clear()
                log_action(f"Loaded crate {crate_counter} (Full)", "LOAD")
                crate_counter += 1
                [crate_available.release() for _ in range(active_pickers)]
                
            # Handle final partial crate
            elif active_pickers == 0:
                if current_crate:
                    crate_history.append({
                        'time': time.time(),
                        'count': len(current_crate),
                        'type': 'partial'
                    })
                    truck.append(current_crate.copy())
                    log_action(f"Loaded final crate ({len(current_crate)} fruits)", "LOAD")
                log_action("Loader exiting", "EXIT")
                return


def analyze_performance():
    """Our performance analysis function"""
    if not crate_history:
        print("No crate data to analyze")
        return

    plt.figure(figsize=(12, 6))
    
    # Fruits picked over time
    plt.subplot(1, 2, 1)
    if pick_timestamps:
        times = [t - pick_timestamps[0] for t in pick_timestamps]
        plt.plot(times, range(1, len(times)+1), color='#2ca02c')
        plt.title("Fruits Picked Over Time")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Total Fruits Picked")
    else:
        plt.text(0.5, 0.5, 'No picking data', 
                ha='center', va='center')
    
    # Crate utilization
    plt.subplot(1, 2, 2)
    crate_counts = [c['count'] for c in crate_history]
    colors = ['#1f77b4' if c['type'] == 'full' else '#ff7f0e' 
             for c in crate_history]
    
    plt.bar(range(len(crate_history)), crate_counts,
            width=0.6, color=colors,
            edgecolor='black', linewidth=1)
    
    plt.title("Crate Utilization")
    plt.xlabel("Crate Number")
    plt.ylabel("Fruits per Crate")
    plt.yticks(np.arange(0, CRATE_CAPACITY+1, 2))
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#1f77b4', label='Full Crates'),
        Patch(facecolor='#ff7f0e', label='Partial Crates')
    ]
    plt.legend(handles=legend_elements)
    
    plt.tight_layout()
    plt.savefig('harvest_analysis.png')
    plt.show()
def main():
    print("""
    ====================================
        Fruit Harvest Simulation
    (Developed for OS Course Project)
    ====================================
    """)
    
    # Initial state
    log_action(f"Starting with {TOTAL_FRUITS} fruits", "INIT")
    print("Initial tree state:", fruit_tree[:10], "...\n")
    
    # Create workers
    pickers = [threading.Thread(target=picker_worker, args=(i,)) 
               for i in range(1,4)]
    loader = threading.Thread(target=loader_worker)
    
    # Start simulation
    start_time = time.time()
    for p in pickers:
        p.start()
    loader.start()
    
    # Wait for completion
    for p in pickers:
        p.join()
    loader.join()
    
    # Results
    print("\nFinal Results:")
    print(f"Total crates: {len(truck)}")
    print(f"Simulation duration: {time.time()-start_time:.2f}s")
    
    # Generate analysis
    analyze_performance()

if __name__ == "__main__":
    main()