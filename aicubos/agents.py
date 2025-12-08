# agents.py
import json
import os


MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory")
os.makedirs(MEMORY_DIR, exist_ok=True)

class Agent:
    def __init__(self, name):
        self.name = name
        self.memory_file = os.path.join(MEMORY_DIR, f"{self.name}_memory.json")
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def respond(self, user_input):
        reply = f"{self.name} remembers you said: {user_input}"
        self.memory.append({"input": user_input, "reply": reply})
        self.save_memory()
        return reply
