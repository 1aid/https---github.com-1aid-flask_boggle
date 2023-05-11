from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_home_route(self):
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"<h1>Boggle Game</h1>", response.data)
            self.assertIn(b"<form>", response.data)
            self.assertIn(b"<input type=\"submit\" value=\"Submit\">", response.data)

    def test_guess_route_valid_word_on_board(self):
        with self.client:
            with app.test_request_context():
                boggle_game = Boggle()
                board = boggle_game.make_board()
                session["board"] = board

                # Get a valid word from the board
                valid_word = boggle_game.words[0]

                response = self.client.post("/guess", data={"guess": valid_word})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["result"], "ok")

    def test_guess_route_valid_word_not_on_board(self):
        with self.client:
            with app.test_request_context():
                boggle_game = Boggle()
                board = boggle_game.make_board()
                session["board"] = board

                # Generate a valid word that is not on the board
                valid_word_not_on_board = "TEST"

                response = self.client.post("/guess", data={"guess": valid_word_not_on_board})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["result"], "not-on-board")

    def test_guess_route_invalid_word(self):
        with self.client:
            response = self.client.post("/guess", data={"guess": "INVALID"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["result"], "not-a-word")
