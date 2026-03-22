from flask import Flask, request, jsonify, render_template
from ai_ensemble_bot import ask

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    prefer = data.get("prefer", "auto")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    result = ask(prompt, prefer=prefer)
    raw_data = result.get("raw", {})

    response = {
    "chosen_provider": result.get("chosen_provider"),
    "chosen_answer": result.get("chosen"),
    "analysis": result.get("analysis"),
    "gemini_raw": raw_data.get("gemini"),
    "openai_raw": raw_data.get("openai")
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
