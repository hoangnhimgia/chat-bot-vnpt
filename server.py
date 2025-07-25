import os
from flask import Flask, request, jsonify
from google_drive_reader import init_drive_service, list_files_in_folder, download_file, read_file_content

app = Flask(__name__)  # ✅ Dòng này là “trái tim” Flask cần có

from google_drive_reader import init_drive_service, list_files_in_folder, download_file, read_file_content

def search_drive_for_answer(question):
    folder_id = "134xELd1joo7EtYiABV67BkuWKZAGmJiL"
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

    # ✅ Fix đoạn này đúng 4 khoảng trắng
    if results:
        return "\n\n".join(results)
    else:
        return "⚠️ Gà chưa tìm được nội dung nào khớp câu hỏi trong các tài liệu hiện có. Bạn thử hỏi rõ hơn hoặc kiểm tra lại file Drive nha 📂"

# ✅ Flask khởi động sau cùng, thụt lề đúng
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"answer": "❗Bạn chưa nhập câu hỏi. Vui lòng thử lại nhé."})

    answer = search_drive_for_answer(question)
    return jsonify({"answer": answer})



