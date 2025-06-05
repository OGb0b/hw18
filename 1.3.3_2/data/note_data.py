import json

def load_data():
    with open("C:/Users/safin/OneDrive/Desktop/python/hw_18/hw18/1.3.3_2/data/node.json", "r", encoding="utf-8") as file:
        notes = json.load(file)
        return notes

def save_data(data):
    with open("C:/Users/safin/OneDrive/Desktop/python/hw_18/hw18/1.3.3_2/data/node.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)