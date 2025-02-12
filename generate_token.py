from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
import webbrowser

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def main():
    # Ensure credentials directory exists
    os.makedirs('credentials', exist_ok=True)
    
    # Check if credentials file exists
    credentials_path = 'credentials/client_secret_742366646909-23h8r0jcnl2je4af9urrnk3kro13gs64.apps.googleusercontent.com.json'
    if not os.path.exists(credentials_path):
        print(f"ERROR: Credentials file not found at {credentials_path}")
        print("Please download your Google Cloud OAuth 2.0 Client ID JSON and save it here.")
        webbrowser.open('https://console.cloud.google.com/apis/credentials')
        return

    # The file token.json stores the user's access and refresh tokens
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, SCOPES)
    
    print("\nGoogle Calendar Authorization")
    print("1. A browser window will open for you to authorize the application")
    print("2. Select the Google account you want to use")
    print("3. Grant the requested permissions")
    
    # This will open a browser window for you to authorize the application
    credentials = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    token_path = 'credentials/token.json'
    with open(token_path, 'w') as token:
        token.write(credentials.to_json())
    
    print(f"\nToken generated successfully!")
    print(f"Token saved to: {token_path}")

if __name__ == '__main__':
    main()
