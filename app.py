from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle
import traceback

app = Flask(__name__)
app.secret_key = "boggle"

boggle_game = Boggle()

@app.route("/")
def home():
    # Generate a new board
    board = boggle_game.make_board()

    # Store the board in the session for later use
    session["board"] = board

    # Render the template and pass the board to it
    return render_template("home.html", board=board)

@app.route("/guess", methods=["POST"])
def guess():
    try:
        guess = request.form.get("guess")

        # Check if the guess is a valid word in the dictionary
        if guess.lower() in boggle_game.words:
            # Check if the word is valid on the board
            result = boggle_game.check_valid_word(session["board"], guess.lower())
            if result == "ok":
                response = {"result": "ok"}
            elif result == "not-on-board":
                response = {"result": "not-on-board"}
            else:
                response = {"result": "not-a-word"}
        else:
            response = {"result": "not-a-word"}

        # Return the response as JSON
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()  # Print the exception traceback
        error_message = "An error occurred: " + str(e)
        response = {"result": "error", "error_message": error_message}
        return jsonify(response)

if __name__ == "__main__":
    app.debug = True  # Enable debug mode
    app.run(debug=True, pin="568-020-342", use_evalex=False)

