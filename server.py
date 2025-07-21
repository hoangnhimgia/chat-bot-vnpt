from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def tra_loi():
    question = request.json.get("question", "")
    answer = f"Bạn hỏi: '{question}' → trợ lý VNPT sẽ trả lời mượt như gà CSKH nhé 😄"
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
