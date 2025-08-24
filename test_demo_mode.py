import os
import sys
sys.path.append('.')

from agent.meeting_agent import MeetingNotesAgent

# Test the demo mode functionality
def test_demo_mode():
    print("Testing demo mode functionality...")
    
    # Set demo mode environment variable
    os.environ['DEMO_MODE'] = 'true'
    
    # Create agent instance
    agent = MeetingNotesAgent()
    
    # Test with sample data
    sample_notes = """
    Team meeting with sarah@company.com and mike@company.com
    
    Sarah needs budget approval by Thursday for Project Phoenix
    John will complete technical specifications by Friday
    Mike is handling the marketing campaign launch next week
    """
    
    attendees = ["sarah@company.com", "mike@company.com"]
    
    print("Running agent in demo mode...")
    result = agent.run_agent(sample_notes, attendees, "Test context")
    
    print(f"Result: {result['success']}")
    if result['success']:
        print(f"Demo mode: {result.get('demo_mode', False)}")
        print(f"Output: {result['result'].outputs.final_output}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_demo_mode()
