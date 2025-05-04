# 🌸 Spring Workers Simulation

Welcome to the **Spring Workers Simulation**!  
This Python script simulates a small team of workers (pickers and a loader) collecting mangoes from a tree, putting them into crates, and finally loading them onto a truck.

---

##  Team Members

- **Anoosha Khalid** - Picker 1  
- **Laiba Iqrar** - Picker 2  
- **Mahnoor Zia** - Picker 3  
- **Loader** - Loads full crates onto the truck  

---

##  How It Works

- The **tree** starts with a number of mangoes.
- **Pickers**:
  - Only one picker picks one fruit at a time from the tree.
  - Place it into a **crate**.
  - If the crate gets full, they notify the **loader**.
- **Loader**:
  - Waits until a crate is full.
  - Then loads the crate into the **truck**.
- The process continues until all fruits are picked and loaded.

---

##  How It’s Built

- Built using **Python's `threading` module** to simulate concurrency.
- **Threads**:
  - 3 picker threads
  - 1 loader thread
- **Thread synchronization** is handled by:
  - `threading.Lock` for mutual exclusion on shared resources (`tree`, `crate`, `truck`)
  - `threading.Semaphore` for coordination between pickers and the loader
- Color-coded logging and time-stamped output make the simulation easy to follow.

---


##  How To Run

1. Make sure you have **Python 3.12.2** installed.
2. Save the code to a file (e.g., `spring_workers.py`).
3. Open your terminal or command prompt.
4. Run the script: python spring_workers.py

---

##  Contact

For any questions, suggestions, or collaboration opportunities, feel free to reach out:
- Email: anooshakhalid999@gmail.com









