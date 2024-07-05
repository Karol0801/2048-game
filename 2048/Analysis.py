import json
import matplotlib.pyplot as plt
import numpy as np

class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.generation = None
        self.population = None
        self.scores = None
        self.max_tiles = None
        self.max_dict = None

    def load_data(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                data = json.loads(last_line)
                self.generation = data.get("generation")
                self.population = data.get("population")
                self.scores = data.get("scores")
                self.max_tiles = data.get("max_tiles")
                self.max_dict = data.get("max_dict")

# Przykład użycia:
loader1 = DataLoader("test_no_random.json")
loader2 = DataLoader("test_random.json")
loader1.load_data()
loader2.load_data()

def plot_bar_chart(data1, data2):
    labels1 = list(data1.keys())
    values1 = list(data1.values())
    labels2 = list(data2.keys())
    values2 = list(data2.values())

    x = np.arange(len(labels1))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width/2, values1, width, label='No Random', color='b')
    bars2 = ax.bar(x + width/2, values2, width, label='Random', color='r')

    ax.set_xlabel("Tiles")
    ax.set_ylabel("Counts")
    ax.set_title("Count tiles in last generation")
    ax.set_xticks(x)
    ax.set_xticklabels(labels1)
    ax.legend()

    plt.xticks(rotation=90)

    plt.show()

# Replace loader1.max_dict and loader2.max_dict with actual data dictionaries
plot_bar_chart(loader1.max_dict, loader2.max_dict)
