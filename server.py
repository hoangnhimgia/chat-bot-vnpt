from google_drive_reader import init_drive_service, list_files_in_folder, download_file, read_file_content
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
def search_drive_for_answer(question):
    folder_id = "134xELd1joo7EtYiABV67BkuWKZAGmJiL"  # thay bằng mã folder Drive Bot-Tailieu
    service = init_drive_service()
    files = list_files_in_folder(service, folder_id)

    all_content = ""
    for file in files:
        file_name = file['name']
        file_id = file['id']
        local_name = f"temp_{file_name}"
        download_file(service, file_id, local_name)
        content = read_file_content(local_name)
        all_content += f"\n--- {file_name} ---\n{content}"

    # Gợi ý tìm đoạn liên quan theo câu hỏi (demo)
    if question.lower() in all_content.lower():
        return f"✅ Có nội dung liên quan tới câu hỏi: '{question}' → Gà CSKH đang tra đúng văn bản nội bộ 🐣📂"
    else:
        return f"⏳ Không tìm thấy đoạn trùng khớp. Gà CSKH vẫn đang lục tài liệu để trả lời chuẩn nha 🐣📂"
@app.route("/chat", methods=["POST"])
def tra_loi():
    question = request.json.get("question", "")
    answer = search_drive_for_answer(question)
    return jsonify({"answer": answer})
