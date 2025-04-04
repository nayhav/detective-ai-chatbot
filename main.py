# main.py
from flask import Flask, render_template, request, jsonify
from chatbot_logic import ask_gemini, get_intro, get_suspect_info, get_clues
from case_data import CASE_DETAILS  

app = Flask(__name__)

@app.route("/")
def home():
    """Render the main UI."""
    return render_template("index.html")

@app.route("/start", methods=["GET"])
def start():
    """Begin the detective game."""
    return jsonify({"message": get_intro()})

@app.route("/suspects", methods=["GET"])
def suspects():
    """Get suspect details."""
    return jsonify({"message": get_suspect_info()})

@app.route("/clues", methods=["GET"])
def clues():
    """Get discovered clues."""
    return jsonify({"message": get_clues()})

@app.route("/ask", methods=["POST"])
def ask():
    """Detective asks a question to Gemini AI."""
    data = request.json
    user_id = data.get("user_id", "default_user")  # Use a default ID if missing
    user_input = data.get("question", "").strip()

    if not user_input:
        return jsonify({"response": "Please provide a valid question."}), 400

    try:
        ai_response = ask_gemini(user_id, user_input)
        return jsonify(ai_response)  # Ensure JSON format
    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500


@app.route("/accuse", methods=["POST"])
def accuse():
    """User makes a final accusation."""
    data = request.json
    accused = data.get("suspect", "").strip()

    if not accused:
        return jsonify({"error": "Please provide a suspect."}), 400

    if accused.lower() not in [s.lower() for s in CASE_DETAILS["suspects"].keys()]:
        return jsonify({"error": "Invalid suspect."}), 400

    if accused.lower() == CASE_DETAILS["killer"].lower():
        return jsonify({"message": "Correct! You solved the mystery!"})
    else:
        return jsonify({"message": "Wrong accusation! The real killer is still at large."})

if __name__ == "__main__":
    app.run(debug=True)
