# test_agents.py
import unittest
import os
import shutil
from aicubos.agents import Agent, MEMORY_DIR

class TestAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure the external memory folder exists"""
        os.makedirs(MEMORY_DIR, exist_ok=True)

    def setUp(self):
        """Runs before each test: clean memory folder for a fresh start"""
        self.agent_name = "TestAgent"
        self.agent = Agent(self.agent_name)
        # Remove memory file if it exists
        if os.path.exists(self.agent.memory_file):
            os.remove(self.agent.memory_file)

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.agent.memory_file):
            os.remove(self.agent.memory_file)

    def test_memory_folder_exists(self):
        """Memory folder should exist"""
        self.assertTrue(os.path.exists(MEMORY_DIR))

    def test_respond_returns_string(self):
        """Agent responds with a string"""
        response = self.agent.respond("Hello")
        self.assertIsInstance(response, str)
        self.assertIn("Hello", response)

    def test_memory_saves_input(self):
        """Memory should store user input and response"""
        self.agent.respond("Test message")
        self.assertEqual(len(self.agent.memory), 1)
        self.assertEqual(self.agent.memory[0]["input"], "Test message")

    def test_memory_persistence(self):
        """Memory should persist after reloading agent"""
        self.agent.respond("Persist this")
        # Reload agent
        new_agent = Agent(self.agent_name)
        self.assertEqual(len(new_agent.memory), 1)
        self.assertEqual(new_agent.memory[0]["input"], "Persist this")

    def test_multiple_inputs(self):
        """Agent can store multiple inputs correctly"""
        messages = ["Hi", "How are you?", "Test"]
        for msg in messages:
            self.agent.respond(msg)
        self.assertEqual(len(self.agent.memory), 3)
        self.assertEqual(self.agent.memory[1]["input"], "How are you?")

if __name__ == "__main__":
    unittest.main()
