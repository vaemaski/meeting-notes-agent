# Meeting Notes AI Agent - Setup Guide for Judges

## Overview
This application uses Portia AI with Google Calendar and Gmail integration to process meeting notes, create calendar events, and send follow-up emails.

## Authentication Setup for Judges

### 1. Environment Setup
Judges will need to set up the following environment variables:

```bash
# Create a .env file in the project root
GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Google Cloud Console Setup (For Judges)

Judges will need to:
1. Create a Google Cloud Project
2. Enable the following APIs:
   - Google Calendar API
   - Gmail API
3. Create OAuth 2.0 credentials
4. Configure authorized redirect URIs

### 3. Alternative: Demo Mode

For judging purposes, we recommend using the **demo mode** that shows what the agent would do without requiring actual Google authentication:

#### How to Enable Demo Mode:
1. Set the following environment variable:
```bash
set DEMO_MODE=true
```

2. Run demo file command to check if agent is working fine:
```bash
python test_demo_mode.py
```

### 4. Step-by-Step Authentication Process

When a judge runs the application:

1. **First Run**: The app will detect that authentication is required
2. **Authentication Prompt**: A warning message will appear with an authentication link
3. **Google OAuth Flow**: Clicking the link redirects to Google's authentication page
4. **Permission Granting**: Judge grants permissions for Calendar and Gmail access
5. **Return to App**: After authentication, the app will be fully functional

### 5. Testing Without Full Authentication

Judges can test core functionality without Google authentication by:

1. **Using sample data**: Load the provided meeting note examples
2. **Viewing agent planning**: See how the agent analyzes and plans actions
3. **Checking validation**: Test input validation and error handling
4. **Reviewing UI/UX**: Evaluate the user interface and experience

### 6. Troubleshooting Authentication

Common issues and solutions:

- **"Authentication Required" error**: Click the provided link to authenticate
- **Permission errors**: Ensure all required APIs are enabled in Google Cloud Console
- **Redirect URI mismatch**: Check authorized redirect URIs in Google Cloud Console

### 7. Demo Credentials (Optional)

For quick evaluation, you can provide judges with:
- Pre-configured demo Google account credentials
- Or use the demo mode as described above

## Technical Requirements

- Python 3.8+
- Google Cloud Project with enabled APIs
- Valid OAuth 2.0 credentials
- Internet connection for API calls

## Evaluation Points

Even without full authentication, judges can evaluate:
- ✅ Input validation and error handling
- ✅ Agent planning and reasoning capabilities  
- ✅ UI/UX design and user feedback
- ✅ Code quality and documentation
- ✅ Overall application architecture

For the best evaluation experience, we recommend judges complete the Google authentication process to see the full functionality in action.
