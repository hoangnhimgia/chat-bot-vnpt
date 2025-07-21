from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def tra_loi():
    question = request.json.get("question", "")
    answer = f"Bạn hỏi: '{question}' → Gà CSKH VNPT đang tìm hiểu để trả lời đúng chuẩn 😎"
    return jsonify({"answer": answer})
