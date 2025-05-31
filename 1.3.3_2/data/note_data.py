import json

def load_data():
    with open("data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)
        return notes

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)