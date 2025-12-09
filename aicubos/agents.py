import json
import os
import re
from datetime import datetime
from tools import TOOLS, TOOL_INFO

MEMORY_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory"
)
LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "tool_usage.log")


class Agent:
    def __init__(self, name):
        self.name = name
        self.memory_file = os.path.join(MEMORY_DIR, f"{self.name}_memory.json")
        self.memory = self.load_memory()

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
    # Tool System (Regex + Commands)
    # ------------------------
    MATH_REGEX = re.compile(r"(\d+[\d\s\+\-\*\/\%\(\)\.]+)")

    def parse_tool_call(self, text):
        t = text.strip().lower()

        # User asked for tool help
        if t == "/tools":
            return "help", None

        # calc: 2+2
        if t.startswith("calc:"):
            return "calculate", t[5:].strip()

        # calc 2+2
        if t.startswith("calc "):
            return "calculate", t[5:].strip()

        # calc(...)
        if t.startswith("calc(") and t.endswith(")"):
            return "calculate", t[5:-1].strip()

        # use <tool>: <payload>
        if t.startswith("use "):
            try:
                part = t[4:]
                tool, payload = part.split(":", 1)
                return tool.strip(), payload.strip()
            except:
                return None

        # tool <tool>: <payload>
        if t.startswith("tool "):
            try:
                part = t[5:]
                tool, payload = part.split(":", 1)
                return tool.strip(), payload.strip()
            except:
                return None

        # Regex-based math detection anywhere in text
        match = self.MATH_REGEX.search(text)
        if match:
            expr = match.group(1).strip()
            return "calculate", expr

        return None

    def use_tool(self, tool_name, payload):
        if tool_name == "help":
            return self.format_tool_help()

        tool = TOOLS.get(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found."

        try:
            result = tool(payload)
            self.log_tool_usage(tool_name, payload)
            return result
        except Exception as e:
            return f"Tool '{tool_name}' failed: {e}"

    def format_tool_help(self):
        lines = ["Available tools:"]
        for name, desc in TOOL_INFO.items():
            lines.append(f"- {name}: {desc}")
        return "\n".join(lines)

    # ------------------------
    # Respond Logic
    # ------------------------
    def respond(self, user_input):
        tool_call = self.parse_tool_call(user_input)

        if tool_call:
            tool_name, payload = tool_call
            result = self.use_tool(tool_name, payload)
            reply = f"[Tool:{tool_name}] → {result}"
        else:
            reply = f"{self.name} remembers you said: {user_input}"

        self.memory.append({"input": user_input, "reply": reply})
        self.save_memory()

        return reply
