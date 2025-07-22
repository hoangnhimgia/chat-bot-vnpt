from flask import Flask, request, jsonify
from flask_cors import CORS
from google_drive_reader import (
    init_drive_service,
    list_files_in_folder,
    download_file,
    read_file_content
)

app = Flask(__name__)
CORS(app)

def search_drive_for_answer(question):
    folder_id = "134xELd1joo7EtYiABV67BkuWKZAGmJiL"
    service = init_drive_service()
    files = list_files_in_folder(service, folder_id)

    all_content = ""
    for file in files:
        file_name = file['name']
        file_id = file['id']
        local_name = f"temp_{file_name}"

        try:
            download_file(service, file_id, local_name)
            content = read_file_content(local_name)
            if content:
                all_content += f"\n--- {file_name} ---\n{content}"
            else:
                print(f"⚠️ File rỗng hoặc không đọc được: {file_name}")
        except Exception as e:
            print(f"❌ Lỗi khi xử lý file {file_name}: {e}")

    if not all_content:
        return f"⏳ Gà chưa tìm được nội dung nào để tra. Kiểm tra lại file trong Drive nha 🐣📂"

    if question.lower() in all_content.lower():
        return f"✅ Có nội dung liên quan tới câu hỏi: '{question}' → Gà CSKH đang tra đúng văn bản nội bộ 🐣📂"
    else:
        return f"❌ Không khớp chính xác câu hỏi trong tài liệu. Bạn thử hỏi rõ hơn nhé 🐣📂"



@app.route("/chat", methods=["POST"])
def tra_loi():
    question = request.json.get("question", "")
    answer = search_drive_for_answer(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
