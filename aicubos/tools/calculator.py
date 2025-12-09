from pydantic import BaseModel, ValidationError

class CalcInput(BaseModel):
    expression: str

def calculator_tool(data):
    # Accept dict or CalcInput
    if isinstance(data, dict):
        try:
            data = CalcInput(**data)
        except ValidationError as e:
            return f"Invalid input: {e}"

    try:
        return eval(data.expression)
    except Exception as e:
        return f"Error: {e}"

TOOL_INFO = {
    "name": "calculate",
    "description": "Evaluate Python math expressions using structured input.",
    "entry": calculator_tool
}
