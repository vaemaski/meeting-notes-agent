from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional

# def parse_meeting_context(text: str) -> Dict:
#     """Extract meeting metadata from notes"""
    
#     context = {
#         "date": None,
#         "attendees": [],
#         "meeting_type": "General Meeting",
#         "duration": None
#     }
    
#     # Extract dates
#     date_patterns = [
#         r'\b(\d{1,2}/\d{1,2}/\d{4})\b',
#         r'\b(\d{1,2}-\d{1,2}-\d{4})\b',
#         r'\b(today|yesterday|tomorrow)\b'
#     ]
    
#     for pattern in date_patterns:
#         match = re.search(pattern, text.lower())
#         if match:
#             context["date"] = match.group(1)
#             break
    
#     # Extract attendees (simple email detection)
#     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     context["attendees"] = re.findall(email_pattern, text)
    
#     # Detect meeting type
#     meeting_types = {
#         "standup": ["standup", "daily", "scrum"],
#         "review": ["review", "retrospective", "retro"],
#         "planning": ["planning", "roadmap", "strategy"],
#         "interview": ["interview", "hiring", "candidate"]
#     }
    
#     text_lower = text.lower()
#     for meeting_type, keywords in meeting_types.items():
#         if any(keyword in text_lower for keyword in keywords):
#             context["meeting_type"] = meeting_type.title() + " Meeting"
#             break
    
#     return context

# def format_action_items(raw_output: str) -> Dict:
#     """Parse and format agent output for display"""
    
#     sections = {
#         "action_items": [],
#         "decisions": [],
#         "follow_ups": [],
#         "urgent": []
#     }
    
#     current_section = None
    
#     for line in raw_output.split('\n'):
#         line = line.strip()
        
#         if '## 🎯 ACTION ITEMS' in line:
#             current_section = "action_items"
#         elif '## 🔑 KEY DECISIONS' in line:
#             current_section = "decisions"
#         elif '## 📧 FOLLOW-UP' in line or '## 📞 FOLLOW-UPS' in line:
#             current_section = "follow_ups"
#         elif '## ⚠️ URGENT' in line:
#             current_section = "urgent"
#         elif line.startswith('- ') and current_section:
#             sections[current_section].append(line[2:])  # Remove '- '
    
#     return sections

# def create_sample_notes() -> List[Dict]:
#     """Sample meeting notes for testing"""
    
#     return [
#         {
#             "title": "Weekly Team Standup",
#             "notes": """
#             Team standup meeting with Sarah (sarah@company.com), John, and Mike
            
#             Sarah mentioned the budget approval is needed by Thursday for Project Phoenix
#             John will complete technical specifications by Friday
#             Mike is handling the marketing campaign launch next week
            
#             Decisions made:
#             - Push product launch date to next month due to budget delays
#             - Weekly check-ins every Tuesday at 2 PM
#             - Sarah to follow up with finance team about budget
            
#             Action items:
#             - Budget approval: Sarah (Due: Thursday)
#             - Tech specs: John (Due: Friday) 
#             - Marketing materials: Mike (Due: Next Monday)
#             - Schedule finance meeting: Sarah (ASAP)
#             """
#         },
#         {
#             "title": "Client Project Review",
#             "notes": """
#             Met with client representatives about Q1 deliverables
#             Present: Alex (alex@client.com), Jennifer, our team
            
#             Client feedback:
#             - Happy with progress on Module A
#             - Concerns about timeline for Module B
#             - Need demo by March 15th
            
#             Next steps:
#             - Prepare demo environment by March 10th
#             - Address Module B timeline concerns
#             - Weekly status calls on Fridays at 3 PM
#             - Send updated project timeline by end of week
#             """
#         }
#     ]


# In agent/utils.py

from portia import PlanRun


def format_agent_run_for_display(plan_run) -> str:
    """
    Parses the agent's execution plan and creates a user-friendly
    Markdown summary of the actions taken.
    """
    if not plan_run:
        return "The agent did not return a valid plan."

    final_summary = ""
    # The final output is often nested in plan_run.outputs.final_output
    if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
        final_summary = plan_run.outputs.final_output
    # Sometimes it's directly on the object
    elif hasattr(plan_run, 'final_output'):
        final_summary = plan_run.final_output

    if final_summary:
        markdown_output = "## ✅ Agent Task Completed!\n\n"
        markdown_output += "Here is the agent's summary:\n\n"
        markdown_output += f"> {final_summary}"
        return markdown_output
    else:
        return "The agent ran, but its output could not be formatted."

def create_sample_notes() -> list[dict]:
    """Provides sample meeting notes for testing or demos."""
    return [
        {
            "title": "Weekly Team Standup",
            "notes": """
Date: today
Attendees: sarah@company.com, John, Mike (mike@company.com)

Sarah needs budget approval by Thursday for Project Phoenix.
John will finalize the tech specs by EOD Friday.
Mike is launching the marketing campaign next week.
Decision: The product launch will be pushed to next month.
Sarah to schedule a follow-up with the finance team ASAP.
            """
        },
        {
            "title": "Client Project Review",
            "notes": """
Date: yesterday
Attendees: alex@client.com, jennifer@client.com, our team

Client is happy with Module A but has concerns about the timeline for Module B.
They need a live demo scheduled for March 15th, 2026.
Action: Our team needs to prepare the demo environment by March 10th.
Action: Send an updated project timeline to the client by the end of this week.
            """
        }
    ]