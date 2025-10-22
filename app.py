from flask import Flask, render_template, request, session
import json
import os #TODO
#from dotenv import load_dotenv
import secrets



app = Flask(__name__) #creates Flask instance; app is now used to handle incoming web requests
app.secret_key= secrets.token_hex(16) 

# Load the rules
with open("rules.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

questions = rules["questions"]
header = rules["header"]


# Just to make shure -> doesnt hurt :) clears the session before we do anything (to make sure the history is accurate)
@app.before_request
def clear_session_on_restart():
    if not session.get("_init"):
        session.clear()
        session["_init"] = True


@app.route("/", methods=["GET", "POST"]) # @app.route turns python code into http responses
def index():

    if "answers" not in session: #creates an empty session dictionary that stores answers (answeres will be stored as question-answer-touples)
        session["answers"] = {}

    answers = session["answers"]

    # Start at question 1 unless user posts answers
    current_question_id = "Q1"
    legal_reasons = None

    if request.method == "POST":
        current_question_id = request.form["next_question"]
        choice = request.form["choice"]
        answers[current_question_id] = choice
        session["answers"] = answers #update the stored answers

        # Determine next step based on the user's answer
        next_q = questions[request.form["question_id"]]["choices"][choice]["next_question"]

        if next_q == "result_page":
            # Display final legal reasoning
            legal_reasons = questions[request.form["question_id"]]["choices"][choice].get("legal_reason", [])
            return render_template(
                "index.html",
                header=header,
                result_page=True,
                legal_reasons=legal_reasons,
                answers=answers,
                questions=questions
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

@app.route("/restart")
def restart():
    session.clear()
    session["_init"] = True
    return index()

if __name__ == "__main__":
    app.run(debug=True)