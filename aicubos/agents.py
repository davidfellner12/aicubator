import json
import os
import re
from datetime import datetime
from aicubos.tools import TOOLS, TOOL_INFO

MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
PERSONALITY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "personalities")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "tool_usage.log")


class Agent:
    MATH_REGEX = re.compile(r"(\d+[\d\s\+\-\*\/\%\(\)\.]+)")

    def __init__(self, name, personality_file=None):
        self.name = name
        self.memory_file = os.path.join(MEMORY_DIR, f"{self.name}_memory.json")
        self.memory = self.load_memory()
        self.load_personality(personality_file)

    # ------------------------
    # Personality
    # ------------------------
    def load_personality(self, filename):
        self.personality = {
            "style": "neutral",
            "preferred_tools": [],
            "response_prefix": f"{self.name} says:",
            "tone": "formal"
        }
        if filename:
            path = os.path.join(PERSONALITY_DIR, filename)
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                    self.personality.update(data)

    # ------------------------
    # Logging
    # ------------------------
    def log_tool_usage(self, tool_name, payload):
        with open(LOG_FILE, "a") as f:
            msg = f"{datetime.now()} | {self.name} used tool: {tool_name} | payload=\"{payload}\""
            f.write(msg + "\n")

    # ------------------------
    # Memory
    # ------------------------
    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    # ------------------------
    # Tool & Context Logic
    # ------------------------
    def parse_tool_call(self, text):
        t = text.strip().lower()
        tools, payloads = [], []

        # Regex-based math detection
        match = self.MATH_REGEX.search(text)
        if match:
            tools.append("calculate")
            payloads.append({"expression": match.group(1).strip()})
            return tools, payloads

        # Context-aware selection based on preferred tools
        if self.personality.get("preferred_tools"):
            tools = self.personality["preferred_tools"]
            payloads = [{"expression": text} if t=="calculate" else text for _ in tools]
            return tools, payloads

        return [], [text]

    def use_tool(self, tool_name, payload):
        tool = TOOLS.get(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found."
        try:
            result = tool(payload)
            self.log_tool_usage(tool_name, payload)
            return result
        except Exception as e:
            return f"Tool '{tool_name}' failed: {e}"

    def chain_tools(self, tools, payloads):
        results = []
        for tool_name, payload in zip(tools, payloads):
            results.append(self.use_tool(tool_name, payload))
        return results

    # ------------------------
    # Respond Logic
    # ------------------------
    def respond(self, user_input):
        tools, payloads = self.parse_tool_call(user_input)

        if tools:
            results = self.chain_tools(tools, payloads)
            reply = " | ".join([f"[Tool:{t}] → {r}" for t, r in zip(tools, results)])
        else:
            reply = f"{self.personality.get('response_prefix', self.name + ' says:')} {user_input}"

        self.memory.append({"input": user_input, "reply": reply})
        self.save_memory()
        return reply
