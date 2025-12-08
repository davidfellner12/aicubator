# aicubos/tools.py

def calculator_tool(expression: str):
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

TOOLS = {
    "calculate": calculator_tool
}
