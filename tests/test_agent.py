# import unittest
# from agent.meeting_agent import MeetingNotesAgent
# from agent.gemini_processor import GeminiProcessor
# from agent.utils import parse_meeting_context, format_action_items

# class TestMeetingAgent(unittest.TestCase):
    
#     def setUp(self):
#         self.agent = MeetingNotesAgent()
#         self.gemini = GeminiProcessor()
#         self.sample_notes = """
#         Met with Sarah about Project Phoenix
#         Budget approval needed by Thursday
#         John handling technical specs by Friday
#         Marketing follow-up required
#         """
    
#     def test_gemini_processing(self):
#         """Test direct Gemini processing"""
#         result = self.gemini.quick_process(self.sample_notes)
#         self.assertIsInstance(result, str)
#         self.assertTrue(len(result) > 0)
    
#     def test_context_parsing(self):
#         """Test meeting context extraction"""
#         context = parse_meeting_context(self.sample_notes)
#         self.assertIsInstance(context, dict)
#         self.assertIn("meeting_type", context)
    
#     def test_attendee_extraction(self):
#         """Test attendee extraction"""
#         notes_with_email = self.sample_notes + " Contact sarah@company.com"
#         attendees = self.gemini.extract_attendees(notes_with_email)
#         self.assertIsInstance(attendees, list)
    
#     # Add more tests as needed

# if __name__ == '__main__':
#     unittest.main()




# In tests/test_agent.py

import pytest
from agent.meeting_agent import MeetingNotesAgent

# --- Test Data (from your example_notes.txt) ---

standup_notes = """
Weekly team standup - January 24, 2025
Attendees: Sarah (sarah@company.com), John (john.doe@company.com), Mike

Sarah's Updates:
- Working on budget approval for Project Phoenix
- Need approval by Thursday from finance team
"""
standup_attendees = ["sarah@company.com", "john.doe@company.com"]


client_notes = """
Client project review meeting
Date: January 24, 2025
Client: TechCorp Inc.
Present: Alex Thompson (alex@techcorp.com), Jennifer Liu, our project team

Client Feedback:
- Very satisfied with Module A development
- Concerned about Module B timeline slippage
- Need comprehensive demo by March 15th
"""
client_attendees = ["alex@techcorp.com"]


# --- Pytest Tests ---

def test_agent_initialization():
    """Tests if the agent can be created successfully."""
    agent = MeetingNotesAgent()
    assert agent is not None, "Agent should be initialized"
    assert hasattr(agent, "portia"), "Agent should have a Portia instance"

@pytest.mark.parametrize(
    "notes_data, attendees_data, expected_keywords",
    [
        (standup_notes, standup_attendees, ["Project Phoenix", "Thursday"]),
        (client_notes, client_attendees, ["TechCorp", "Module B", "March 15th"]),
    ]
)
def test_agent_with_real_examples(mocker, notes_data, attendees_data, expected_keywords):
    """
    Tests the main run_agent method with different sets of realistic notes.
    This test runs twice, once for each set of parameters defined above.
    """
    # 1. Arrange: Create the agent and mock the `portia.run` method
    agent = MeetingNotesAgent()
    mock_run = mocker.patch.object(agent.portia, 'run')
    
    # Simulate a successful return object from Portia
    class FakePlanRun:
        def __init__(self):
            self.outputs = self
            self.final_output = "Mocked: Actions completed successfully."
            self.id = "mock_plan_123"
    mock_run.return_value = FakePlanRun()

    # 2. Act: Call the method we want to test with the parametrized data
    result = agent.run_agent(
        raw_notes=notes_data,
        attendees=attendees_data,
        context="Test context"
    )

    # 3. Assert: Check if our code behaved as expected
    assert result["success"] is True
    assert result["plan_id"] == "mock_plan_123"

    # Advanced Assertion: Check if the agent's task/prompt was constructed correctly
    # This verifies that the agent received the correct notes.
    mock_run.assert_called_once()
    call_args, call_kwargs = mock_run.call_args
    agent_task_prompt = call_args[0] # The first argument passed to portia.run()
    
    for keyword in expected_keywords:
        assert keyword in agent_task_prompt