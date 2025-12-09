from aicubos.agents import Agent
import asyncio

class MultiAgentManager:
    def __init__(self):
        self.agents = {}

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    async def send_message(self, sender_name, recipient_name, message):
        sender = self.agents.get(sender_name)
        recipient = self.agents.get(recipient_name)
        if not sender or not recipient:
            return f"Error: Sender or recipient not found."

        # Sender can log message
        sender.memory.append({"sent_to": recipient_name, "message": message})
        sender.save_memory()

        # Recipient responds
        reply = recipient.respond(message)
        recipient.memory.append({"received_from": sender_name, "message": message, "reply": reply})
        recipient.save_memory()
        return reply

    async def broadcast(self, sender_name, message):
        replies = {}
        for name, agent in self.agents.items():
            if name == sender_name:
                continue
            replies[name] = await self.send_message(sender_name, name, message)
        return replies
