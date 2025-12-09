import os
import importlib.util

TOOLS = {}
TOOL_INFO = {}

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")

def load_tools():
    """Auto-load all tool modules in the tools/ directory."""
    for filename in os.listdir(TOOLS_DIR):
        if not filename.endswith(".py"):
            continue

        module_path = os.path.join(TOOLS_DIR, filename)
        module_name = f"aicubos.tools.{filename[:-3]}"

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Tool must expose TOOL_INFO dict
        if hasattr(module, "TOOL_INFO"):
            info = module.TOOL_INFO
            name = info["name"]
            TOOLS[name] = info["entry"]
            TOOL_INFO[name] = info.get("description", "(no description)")

# Load tools at import time
load_tools()
