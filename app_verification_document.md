# Football Matches Calendar - Google OAuth Verification Document

## Application Overview
- **Name**: Football Matches Calendar
- **Purpose**: Automated Football Match Event Tracking
- **Type**: Personal Utility Application

## Functionality Description
The application performs the following core functions:
1. Fetches football match data from sports APIs
2. Generates calendar events for upcoming matches
3. Imports events to Google Calendar for personal tracking

## Data Access and Usage
### Requested Scopes
- `https://www.googleapis.com/auth/calendar.events`
  - Purpose: Create and manage calendar events
  - Scope Limited To: 
    - Adding match events
    - No read or modification of existing events

### Data Handling Practices
- **Data Minimization**: Only creates events related to football matches
- **Temporary Storage**: Match data is not persistently stored
- **User Control**: 
  - User initiates each calendar import
  - Events can be manually deleted by user

## Privacy and Security
### Data Protection
- No personal user data is collected or stored
- Calendar interactions are read-write for match events only
- OAuth token stored locally with user's explicit consent

### Security Measures
- Uses OAuth 2.0 for secure authentication
- Requires explicit user authorization for each run
- No third-party data sharing
- Runs only on user's local machine

## Screenshots
[Note: Actual screenshots would be attached during verification process]
- Fetch Matches Script Interface
- Calendar Event Generation Process
- OAuth Consent Screen

## Technical Details
- **Language**: Python
- **Authentication**: Google OAuth 2.0
- **Platforms**: Desktop (Windows)
- **Dependencies**: 
  - google-api-python-client
  - google-auth-oauthlib

## User Consent and Control
1. Application requires manual authorization
2. User can revoke access at any time in Google Account settings
3. No automatic or background data collection

## Contact Information
- **Developer Email**: [Your Email]
- **Support**: GitHub Issues or Direct Contact

## Terms of Use
This is a personal utility application developed for individual use, 
designed to simplify football match tracking through calendar integration.
