from aicubos.agents import Agent

def test_calc():
    a = Agent("Tester")
    assert "Result" in a.respond("calc: 2+3")
