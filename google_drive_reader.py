from google.oauth2 import service_account
from googleapiclient.discovery import build

def init_drive_service():
    creds = service_account.Credentials.from_service_account_file("credentials.json")
    service = build("drive", "v3", credentials=creds)
    return service
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query).execute()
    files = results.get("files", [])
    for file in files:
        print(f"📄 Tên file: {file['name']} — ID: {file['id']}")
    return files
