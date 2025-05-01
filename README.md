# 🌸 Spring Workers Simulation

Welcome to the **Spring Workers Simulation**!  
This Python script simulates a small team of workers (pickers and a loader) collecting mangoes from a tree, putting them into crates, and finally loading them onto a truck.

---

##  Team Members

- **Anoosha** - Picker 1  
- **Laiba** - Picker 2  
- **Mahnoor** - Picker 3  
- **Loader** - Loads full crates onto the truck  

---

##  How It Works

- The **tree** starts with a number of mangoes.
- **Pickers**:
  - Pick one fruit at a time from the tree.
  - Place it into a **crate**.
  - If the crate gets full, they notify the **loader**.
- **Loader**:
  - Waits until a crate is full.
  - Then loads the crate into the **truck**.
- The process continues until all fruits are picked and loaded.

---

##  How It’s Built

- Uses **generators** to simulate concurrency (step-by-step turns).
- A simple **scheduler** (list) manages turn-taking between pickers and the loader.
- **Mutexes and Semaphores** are used to safely manage shared resources like the tree and crate.

---

##  How To Run

1. Make sure you have **Python 3.12.2** installed.
2. Save the code to a file (e.g., `spring_workers.py`).
3. Open your terminal or command prompt.
4. Run the script:

```bash
python spring_workers.py



