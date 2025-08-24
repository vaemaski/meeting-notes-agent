# Meeting Notes AI Agent

## Overview
The Meeting Notes AI Agent is a Python application that utilizes Portia AI to process meeting notes, extract actionable items, create Google Calendar events, and send follow-up emails. This application is designed to streamline the management of meeting outcomes and enhance productivity.

## Features
- **Input Validation**: Ensures that meeting notes and attendee emails are valid before processing.
- **Google Calendar Integration**: Automatically creates calendar events for action items with deadlines.
- **Email Integration**: Drafts summary emails for meeting attendees.
- **Demo Mode**: Allows testing of the application without requiring Google authentication.
- **User Feedback**: Provides loading indicators and error messages to enhance user experience.

## Requirements
- Python 3.8+
- Google Cloud Project with enabled APIs (Google Calendar API, Gmail API)
- Valid OAuth 2.0 credentials
- Internet connection for API calls

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment variables:
   - Create a `.env` file in the project root and add your Google API key:
     ```bash
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## Usage
1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8502`.

3. Input your meeting notes and attendee emails in the provided fields.

4. Choose the actions you want the agent to perform (create calendar events, send emails).

5. Click the "Process Notes with Agent" button to execute the agent's tasks.

## Demo Mode
To enable demo mode for testing without authentication:
1. Set the following environment variable:
   ```bash
   DEMO_MODE=true
   python test_demo_mode.py
   ```

2. The application will simulate the agent's actions and provide feedback without requiring Google authentication.

## Troubleshooting
- Ensure that all required APIs are enabled in your Google Cloud Project.
- Check that your OAuth 2.0 credentials are correctly configured.
- If you encounter authentication errors, verify that the redirect URIs are set correctly in the Google Cloud Console.



## Acknowledgments
- Portia AI for providing the underlying AI capabilities.
- Streamlit for creating the user interface.

## Contact
For any questions or feedback, please reach out to [vaishali.ds0228@gmail.com].
