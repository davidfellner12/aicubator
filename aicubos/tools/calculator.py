def calculator_tool(expr: str):
    try:
        return eval(expr)
    except Exception as e:
        return f"Error: {e}"

TOOL_INFO = {
    "name": "calculate",
    "description": "Evaluate math expressions.",
    "entry": calculator_tool
}
