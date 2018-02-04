import os
import unittest
import requests

host = os.getenv("mastermind_host", "http://localhost")
createUrl = host + "/create"
playUrl = host + "/play"
gameDataUrl = host + "/status"


class EncToEndTest(unittest.TestCase):
    def test_input_pattern_deserealization(self):
        # CREATE GAME
        game_payload = {"game_pattern": ["GREEN", "BLUE", "RED", "PURPLE"]}
        response = requests.post(createUrl, json=game_payload)
        data = response.json()
        id_game = data["id_game"]
        self.assertEqual(len(id_game), 32)

        # MAKE SOME PLAYS
        first_play = {"id_game": id_game, "played_pattern": ["BLUE", "GREEN", "RED", "BLACK"]}
        response = requests.post(playUrl, json=first_play)
        data = response.json()
        self.assertEqual(data["Black"], 1)
        self.assertEqual(data["White"], 2)

        second_play = {"id_game": id_game, "played_pattern": ["GREEN", "BLUE", "RED", "PURPLE"]}
        response = requests.post(playUrl, json=second_play)
        data = response.json()
        self.assertEqual(data["Black"], 4)
        self.assertEqual(data["White"], 0)

        # get game data
        payload = {"id_game": id_game}
        response = requests.get(gameDataUrl, params=payload)
        data = response.json()
        self.assertEqual(data["status"], "FINISHED")
        self.assertEqual(len(data["plays_played"]), 2)


if __name__ == '__main__':
    unittest.main()
