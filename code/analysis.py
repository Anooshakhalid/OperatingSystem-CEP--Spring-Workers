# analysis.py

import matplotlib.pyplot as plt

def generate_visualizations(picker_data):
    # Visualization for fruits picked by each picker
    plt.figure(figsize=(8, 5))
    picker_names = ['Anoosha', 'Laiba', 'Mahnoor']
    fruits_picked = [picker_data[1], picker_data[2], picker_data[3]]

    plt.bar(picker_names, fruits_picked, color=['blue', 'green', 'orange'])
    plt.title('Fruits Picked by Each Picker')
    plt.xlabel('Pickers')
    plt.ylabel('Fruits Picked')
    plt.show()
