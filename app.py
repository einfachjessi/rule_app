from flask import Flask, render_template, request
import json

app = Flask(__name__) #creates Flask instance; app is now used to handle incoming web requests

# Load the rules
with open("rules.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

questions = rules["questions"]
header = rules["header"]


@app.route("/", methods=["GET", "POST"]) # @app.route turns python code into http responses
def index():
    # Start at question 1 unless user posts answers
    current_question_id = "1"
    legal_reasons = None

    if request.method == "POST":
        current_question_id = request.form["next_question"]
        choice = request.form["choice"]

        # Determine next step based on the user's answer
        next_q = questions[request.form["question_id"]]["choices"][choice]["next_question"]

        if next_q == "result_page":
            # Display final legal reasoning
            legal_reasons = questions[request.form["question_id"]]["choices"][choice].get("legal_reason", [])
            return render_template(
                "index.html",
                header=header,
                result_page=True,
                legal_reasons=legal_reasons
            )
        else:
            current_question_id = next_q

    # Show next question
    current_question = questions[current_question_id]
    return render_template( #finds index.html in the \templates folder
        "index.html",
        header=header,
        question_id=current_question_id,
        question=current_question,
        result_page=False
    )


if __name__ == "__main__":
    app.run(debug=True)