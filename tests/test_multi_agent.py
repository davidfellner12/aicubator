import asyncio
from aicubos.agents import Agent
from aicubos.multiagent import MultiAgentManager

# ------------------------
# Setup agents
# ------------------------
alice = Agent("Alice", personality_file="alice.json")
bob = Agent("Bob", personality_file="bob.json")

manager = MultiAgentManager()
manager.add_agent(alice)
manager.add_agent(bob)

# ------------------------
# Test cases
# ------------------------
async def test_send_message():
    # Alice sends a math expression to Bob
    reply = await manager.send_message("Alice", "Bob", "calc 7*6")
    print("Bob replies:", reply)
    assert reply == "[Tool:calculate] → 42", f"Unexpected reply: {reply}"

    # Bob sends a normal message to Alice
    reply2 = await manager.send_message("Bob", "Alice", "Hello Alice!")
    print("Alice replies:", reply2)
    assert reply2.startswith("Alice says:"), f"Unexpected reply: {reply2}"

async def test_broadcast():
    # Alice broadcasts to all other agents
    replies = await manager.broadcast("Alice", "Hello everyone!")
    print("Broadcast replies:", replies)

    # Check that replies are correct and from expected agents
    for agent_name, message in replies.items():
        if agent_name == "Bob":
            assert message.startswith("Bob says:"), f"Unexpected broadcast reply: {message}"

# ------------------------
# Run tests
# ------------------------
async def main():
    print("Running test_send_message...")
    await test_send_message()
    print("Running test_broadcast...")
    await test_broadcast()
    print("All multi-agent tests passed ")

if __name__ == "__main__":
    asyncio.run(main())
