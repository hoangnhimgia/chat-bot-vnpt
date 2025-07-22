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
def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    with open(file_name, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print(f"✅ Đã tải: {file_name}")
def read_file_content(file_path):
    if file_path.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_path.endswith(".docx"):
        import docx2txt
        return docx2txt.process(file_path)
    else:
        return ""
