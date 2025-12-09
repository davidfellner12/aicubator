# aicubos/main.py
import asyncio
from aicubos.agents import Agent

async def agent_loop(agent: Agent):
    print(f"{agent.name} is ready. Type 'quit' to exit.")
    loop = asyncio.get_event_loop()

    while True:
        try:
            user_input = await loop.run_in_executor(None, input, f"[{agent.name}] You: ")
        except EOFError:
            print(f"\n{agent.name} detected EOF (Ctrl+Z). Shutting down...")
            break

        if user_input.lower() in ["quit", "exit"]:
            print(f"{agent.name} shutting down...")
            break

        reply = agent.respond(user_input)
        print(reply)


async def main():
    # Single agent for Day 1
    alice = Agent("Alice")
    await asyncio.gather(agent_loop(alice))

if __name__ == "__main__":
    asyncio.run(main())
