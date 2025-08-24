import os
import re
from datetime import datetime
from typing import Dict, List
from portia import Config, Portia, StorageClass
from portia.tool_registry import DefaultToolRegistry
from portia.cli import CLIExecutionHooks

class MeetingNotesAgent:
    def __init__(self):
        """
        Initializes the Portia AI agent.
        The agent is configured to use the tools available in the registry,
        such as Google Calendar, Gmail, etc.
        """
        self.config = Config.from_default(
            storage_class=StorageClass.CLOUD,
            model="gemini-1.5-flash"  # Using a powerful and fast model
        )
        
        # This registry gives the agent access to tools like calendar and email.
        # Ensure your environment is authenticated with Google Cloud for these to work.
        self.portia = Portia(
            config=self.config,
            tools=DefaultToolRegistry(self.config),
            execution_hooks=CLIExecutionHooks(),
        )

        # --- Add this debug line ---
        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"--- DEBUG: GOOGLE_API_KEY loaded as: {api_key} ---")
        # 

    # In agent/meeting_agent.py

    def run_agent(self, raw_notes: str, attendees: List[str], context: str = "") -> Dict:
        """
        Main method to process notes, create events, and send follow-ups in one go.
        Supports demo mode for testing without authentication.
        """
        
        # Input validation
        if not raw_notes or not raw_notes.strip():
            return {
                "success": False,
                "error": "Meeting notes cannot be empty.",
                "result": "Please provide valid meeting notes."
            }
        
        if not attendees:
            return {
                "success": False,
                "error": "At least one attendee email is required.",
                "result": "Please provide at least one attendee email address."
            }
        
        # Validate email format for attendees
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        valid_emails = []
        for email in attendees:
            if re.match(email_pattern, email):
                valid_emails.append(email)
            else:
                print(f"Warning: Invalid email format: {email}")
        
        if not valid_emails:
            return {
                "success": False,
                "error": "No valid email addresses provided.",
                "result": "Please provide valid email addresses for attendees."
            }
        
        # Check for demo mode
        demo_mode = os.getenv("DEMO_MODE", "").lower() == "true"
        
        # --- Get the current date to provide context to the agent ---
        current_date = datetime.now().strftime("%Y-%m-%d")

        task = f"""
        ROLE: You are a professional meeting assistant AI. Your goal is to process the meeting notes, 
        extract actionable items, schedule them in the calendar, and send a summary email.

        CONTEXT:
        - Today's date is {current_date}. Use this to resolve relative dates like 'today', 'tomorrow', 'next week'.
        - {context}
        - DEMO MODE: {demo_mode}

        MEETING NOTES:
        ---
        {raw_notes}
        ---

        MEETING ATTENDEES (email addresses):
        - {', '.join(valid_emails)}

        INSTRUCTIONS:
        1.  **Analyze**: Read the notes to identify all action items, owners, and deadlines.
        2.  **Schedule**: For every action item with a deadline, use your calendar tool to create a Google Calendar event.
        3.  **Summarize & Notify**: Draft and send a concise summary email to all attendees.

        ---
       
        """
        
        print("🤖 Portia Agent is planning and executing the task...")
        print(f"DEBUG - Task content length: {len(task)} characters")
        print(f"DEBUG - Valid emails: {valid_emails}")
        print(f"DEBUG - Demo mode: {demo_mode}")
        
        try:
            print("DEBUG - About to call self.portia.run()")
            
            if demo_mode:
                # Simulate agent response for demo purposes
                print("DEBUG - Running in demo mode (simulated response)")
                # Create a simulated plan run response
                class MockPlanRun:
                    def __init__(self):
                        self.id = "demo-plan-12345"
                        self.outputs = type('obj', (object,), {
                            'final_output': f"DEMO MODE: Agent analyzed meeting notes and identified action items. Would create calendar events for deadlines and draft summary email to {', '.join(valid_emails)}."
                        })()
                
                plan_run = MockPlanRun()
                print("DEBUG - Demo mode simulation completed successfully")
            else:
                # Real agent execution
                plan_run = self.portia.run(query=task,
                                          end_user="meeting_organizer",
                                          tools=["portia:google:gmail:draft_email", "portia:google:gcalendar:create_event"])
                print("DEBUG - self.portia.run() completed successfully")
            
            return {
                "success": True,
                "result": plan_run, # Return the full plan_run object for formatting
                "plan_id": plan_run.id if hasattr(plan_run, 'id') else None,
                "timestamp": datetime.now().isoformat(),
                "demo_mode": demo_mode
            }
            
        except Exception as e:
            print(f"An error occurred: {e}")
            error_msg = str(e)
            
            # Check if this is an authentication error that can be handled in demo mode
            if demo_mode and ("authentication" in error_msg.lower() or "oauth" in error_msg.lower()):
                print("DEBUG - Authentication error in demo mode, providing simulated response")
                class MockPlanRun:
                    def __init__(self):
                        self.id = "demo-auth-error-12345"
                        self.outputs = type('obj', (object,), {
                            'final_output': f"DEMO MODE: Authentication would be required here for real Google Calendar and Gmail access. Agent identified action items in the meeting notes."
                        })()
                
                return {
                    "success": True,
                    "result": MockPlanRun(),
                    "plan_id": "demo-auth-plan",
                    "timestamp": datetime.now().isoformat(),
                    "demo_mode": True,
                    "auth_required": True
                }
            
            return {
                "success": False,
                "error": error_msg,
                "result": f"Failed to process meeting notes: {error_msg}"
            }
