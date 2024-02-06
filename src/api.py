import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def auth():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        
    creds = None
    # token.json stores the user's access and refresh tokens, and auto-created 
    # when authorization flow completes for the 1st time.
    if os.path.exists("auth/token.json"):
        creds = Credentials.from_authorized_user_file("auth/token.json", SCOPES)
    # If there are no (valid) credentials available, log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "auth/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials
            with open("auth/token.json", "w") as token:
                token.write(creds.to_json())
    
    return creds


def get_values(creds, spreadsheet_id, range_name):
    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        return rows
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def write_values(creds, spreadsheet_id, range_name, value_input_option):
    try:
        service = build("sheets", "v4", credentials=creds)
        values = [
            [
                "/"
            ],
        ]
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        return result
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error