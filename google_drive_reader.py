from google.oauth2 import service_account
from googleapiclient.discovery import build

def init_drive_service():
    creds = service_account.Credentials.from_service_account_file("credentials.json")
    service = build("drive", "v3", credentials=creds)
    return service
