from flask import Flask, render_template, jsonify, request, session
import sqlite3
from gen_plan import generate_plan
from select_ex import select_exercises_covering_muscles
from helpers import get_names
from update import process_update

app = Flask(__name__)
app.secret_key = "tajnehaslo123"  # wymagane do sesji

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_input", methods=["POST"])
def submit_input():
    data = request.get_json()
    session["user_input"] = data
    return jsonify({"status": "ok"})

@app.route("/get_data")
def get_data():
    user_input = session.get("user_input")
    if not user_input:
        return jsonify({"error": "User input missing"}), 400

    print("✅ USER INPUT:")
    print(user_input)  # 👈 ZOBACZ CO PRZYCHODZI Z FORMULARZA
    # 🔁 Użyj danych użytkownika z formularza (lub fallback na user_input_1 jeśli chcesz)

    conn = sqlite3.connect("trening.db")
    filtered_ids = generate_plan(user_input, conn)
    chosen_exercises, activation = select_exercises_covering_muscles(filtered_ids, conn)
    conn.close()

    chosen_ids = [ex["id"] for ex in chosen_exercises]
    available_ids = [i for i in filtered_ids if i not in chosen_ids]

    current = get_names(chosen_ids)
    available = get_names(available_ids)

    # zapisz initial chosen do sesji
    session["chosen_ids"] = chosen_ids

    return jsonify({
        "current": current,
        "available": available,
        "activation": activation
    })

@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()
    action = data.get("action")
    ex_id = data.get("id")

    if "chosen_ids" not in session:
        session["chosen_ids"] = []

    chosen = session["chosen_ids"]
    result = process_update(action, ex_id, chosen)
    session["chosen_ids"] = result["chosen"]

    return jsonify({
        "current": result["current"],
        "available": result["available"],
        "activation": result["activation"]
    })

if __name__ == "__main__":
    app.run(debug=True)