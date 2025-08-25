import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Imports for the new, unified agent ---
from agent.meeting_agent import MeetingNotesAgent
from agent.utils import create_sample_notes, format_agent_run_for_display # <-- Updated imports

# Page configuration (remains the same)
st.set_page_config(
    page_title="Meeting Notes AI Agent",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (remains the same)
st.markdown("""
<style>
    /* Your custom CSS remains here */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 2rem;
    }
    .success-banner {
        background: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header (remains the same)
    st.markdown("""
    <div class="main-header">
        <h1>📝 Meeting Notes AI Agent</h1>
        <p>Transform rambling meeting notes into clear action items with AI-powered intelligence</p>
        <small>Powered by Portia AI + Gemini | Built for AgentHack 2025</small>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Simplified session state ---
    if 'agent' not in st.session_state:
        st.session_state.agent = MeetingNotesAgent() # <-- Only the agent is needed now
    if "processing_history" not in st.session_state:
        st.session_state.processing_history = []
    if "auth_required" not in st.session_state:
        st.session_state.auth_required = False
    if "auth_url" not in st.session_state:
        st.session_state.auth_url = ""
        
    
    # In app.py

    # --- Sidebar with updated controls ---
    with st.sidebar:
        st.header("⚙️ Agent Controls")
    
        st.subheader("Actions to Perform")
        create_calendar_events = st.checkbox("Create Calendar Events", value=True, help="Agent will use its tools to create Google Calendar events for items with deadlines.")
        send_emails = st.checkbox("Send Follow-up Email", value=False, help="Agent will draft and send a summary email to attendees.")
        


        st.subheader("📋 Quick Start / Load Examples")
    
        # --- Option 1: Load structured samples from utils.py ---
        sample_notes = create_sample_notes()
        for i, sample in enumerate(sample_notes):
            if st.button(f"Load: {sample['title']}", key=f"sample_{i}"):
                st.session_state.sample_notes = sample['notes']
                import re
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', sample['notes'])
                st.session_state.sample_emails = ", ".join(emails)
                st.rerun()

          # --- Main content area (mostly the same) ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Input Meeting Notes")
        default_text = st.session_state.get('sample_notes', '')
        meeting_notes = st.text_area(
            "Paste your meeting notes here:",
            value=default_text,
            height=300,
        )
        
        default_emails = st.session_state.get('sample_emails', '')
        attendee_emails = st.text_input(
            "Attendee emails (comma-separated):",
            value=default_emails,
            placeholder="sarah@company.com, john@company.com"
        )
    
    with col2:
        st.subheader("🚀 Processing")
        if meeting_notes:
            word_count = len(meeting_notes.split())
            st.metric("Word Count", word_count)
        
        process_button = st.button(
            "🤖 Process Notes with Agent", 
            type="primary",
            disabled=not meeting_notes or not attendee_emails,
            use_container_width=True
        )

    # --- New, Unified Processing Logic ---
    if process_button:
        attendees = [email.strip() for email in attendee_emails.split(',')]
        
        # Build dynamic instructions for the agent based on UI controls
        context_instructions = "Please perform the following actions:\n"
        if create_calendar_events:
            context_instructions += "- For every action item with a clear deadline, use your calendar tool to create a Google Calendar event.\n"
        if send_emails:
            context_instructions += "- Use your email tool to send a summary email to all meeting attendees.\n"
        else:
            # If not sending an email, ask it to draft one so the user can see it
            context_instructions += "- Draft a concise summary email that includes the key decisions and action items.\n"

        # Create a progress container to show agent activity
        progress_container = st.empty()
        progress_container.info("🤖 Agent is analyzing notes, forming a plan, and executing, this may take a while please be patient")
        
        start_time = datetime.now()
        
        # --- Single, powerful call to the agent ---
        agent_result = st.session_state.agent.run_agent(
            raw_notes=meeting_notes,
            attendees=attendees,
            context=context_instructions,
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Clear the progress container
        progress_container.empty()

        # --- Display results using the new formatter ---
        if agent_result["success"]:
            st.markdown('<div class="success-banner">✅ Agent has completed its tasks!</div>', unsafe_allow_html=True)
            
            st.metric("Processing Time", f"{processing_time:.1f}s")
            
            # Use the formatter from utils.py to create a beautiful output
            display_output = format_agent_run_for_display(agent_result["result"])
            st.markdown("---")
            st.markdown("## 📋 Agent Action Summary")
            st.markdown(display_output)

            # Save to history
            st.session_state.processing_history.append({
                "timestamp": datetime.now(),
                "processing_time": processing_time,
                "input_length": len(meeting_notes),
                "result": display_output # Save the formatted output
            })

        else:
            # Check if authentication is required
            error_msg = agent_result["error"]
            if "OAuth required for google" in error_msg or "authentication" in error_msg.lower():
                # Extract the authentication URL from the error message
                import re
                url_match = re.search(r'https://[^\s]+', error_msg)
                if url_match:
                    st.session_state.auth_required = True
                    st.session_state.auth_url = url_match.group(0)
                    st.warning("🔐 Authentication Required")
                    st.markdown("### Google Authentication Required")
                    st.markdown("To use calendar and email features, you need to authenticate with Google:")
                    st.markdown(f"[Click here to authenticate]({st.session_state.auth_url})")
                    st.markdown("After authenticating, click the button below to continue processing.")
                    
                    if st.button("🔄 Continue After Authentication"):
                        st.session_state.auth_required = False
                        st.rerun()
                else:
                    st.error(f"❌ Authentication required but URL not found: {error_msg}")
            else:
                st.error(f"❌ Agent failed: {error_msg}")

    # History expander (can remain the same)
    if st.session_state.processing_history:
        with st.expander("📊 Processing History", expanded=False):
            # Your history display logic can go here
            history_df = pd.DataFrame(st.session_state.processing_history)
            st.dataframe(history_df[['timestamp', 'processing_time', 'input_length']])


if __name__ == "__main__":
    main()