import os
from google_drive_reader import init_drive_service, list_files_in_folder, download_file, read_file_content

def search_drive_for_answer(question):
    folder_id = "134xELd1joo7EtYiABV67BkuWKZAGmJiL"  # Folder gốc Bot-Tailieu
    service = init_drive_service()
    files = list_files_in_folder(service, folder_id)

    results = []
    q_lower = question.lower()

    for file in files:
        file_name = file['name']
        file_id = file['id']
        local_path = f"temp_{file_name}"

        try:
            download_file(service, file_id, local_path)
            content = read_file_content(local_path)
            if not content:
                continue

            content_lower = content.lower()
            if q_lower in content_lower:
                idx = content_lower.index(q_lower)
                excerpt = content[max(0, idx - 300): idx + 300]
                results.append(f"📄 **{file_name}**:\n{excerpt.strip()}")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý {file_name}: {e}")

    if results:
        return "\n\n".join(results)
    else:
        return "⚠️ Gà chưa tìm được nội dung nào khớp câu hỏi trong các tài liệu hiện có. Bạn thử hỏi rõ hơn hoặc kiểm tra lại file Drive nha 🐣📂"
