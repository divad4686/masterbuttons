import unittest
import uuid
from collections import namedtuple


from src.mastermind.mastermind_logic import Color, calculate_move
from src.mastermind.game_aggregate import GameStatus, create_game_status_agregate, GameCreatedEvent, make_move


class Tests(unittest.TestCase):
    game_pattern = (Color.GREEN, Color.BLUE, Color.RED, Color.PURPLE)
    moves = [(Color.YELLOW, Color.YELLOW, Color.BLUE, Color.BLUE),
             (Color.PURPLE, Color.RED, Color.RED, Color.YELLOW),
             (Color.GREEN, Color.PURPLE, Color.GREEN, Color.YELLOW),
             (Color.RED, Color.RED, Color.PURPLE, Color.YELLOW),
             (Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE),
             (Color.GREEN, Color.BLUE, Color.RED, Color.PURPLE)]

    def test_game_logic(self):
        def assert_game(game_pattern, move, expected_black, expected_white, test_number):
            error_msg = 'fail in test number: {0}'.format(test_number)
            result = calculate_move(game_pattern, move)
            self.assertEqual(result.Black, expected_black, msg=error_msg)
            self.assertEqual(result.White, expected_white, msg=error_msg)
            self.assertLessEqual(result.Black + result.White, 4, msg=error_msg)

        test_move = namedtuple("test_move", "move expected_black expected_white")

        moves_to_test = [test_move(self.moves[0], 0, 1),
                         test_move(self.moves[1], 1, 1),
                         test_move(self.moves[2], 1, 1),
                         test_move(self.moves[3], 0, 2),
                         test_move(self.moves[4], 1, 3),
                         test_move(self.moves[5], 4, 0)]

        for idx, move in enumerate(moves_to_test):
            assert_game(self.game_pattern, move.move, move.expected_black, move.expected_white, idx)

        with self.assertRaises(ValueError):
            calculate_move([Color.RED], [Color.BLUE])

    def test_game_aggregate(self):
        events = []
        game_created = GameCreatedEvent(uuid.uuid4(), self.game_pattern)
        events.append(game_created)

        for move in self.moves:
            played_event = make_move(game_created.id_game, self.game_pattern, move)
            events.append(played_event)

        # This move should not affect the aggregate because the game is finished
        invalid_move = (Color.GREEN, Color.BLUE, Color.RED, Color.PURPLE)
        played_event = make_move(game_created.id_game, self.game_pattern, invalid_move)
        events.append(played_event)

        # Multiple calls should be inmutable
        game_status = create_game_status_agregate(events)
        game_status = create_game_status_agregate(events)
        game_status = create_game_status_agregate(events)

        self.assertEqual(game_status.game_pattern, game_created.game_pattern)
        self.assertEqual(len(game_status.plays_played), len(self.moves))
        self.assertEqual(game_status.plays_played[3].played_pattern, self.moves[3])
        self.assertEqual(game_status.status, GameStatus.FINISHED)

    def test_aggregate_states(self):
        events = []
        game_created = GameCreatedEvent(uuid.uuid4(), self.game_pattern)
        events.append(game_created)

        first_move = self.moves[0]

        played_event = make_move(game_created.id_game, self.game_pattern, first_move)
        events.append(played_event)

        game_status = create_game_status_agregate(events)
        self.assertEqual(game_status.status, GameStatus.PLAYING)

        second_move = self.moves[-1]
        played_event = make_move(game_created.id_game, self.game_pattern, second_move)
        events.append(played_event)

        game_status = create_game_status_agregate(events)
        self.assertEqual(game_status.status, GameStatus.FINISHED)


if __name__ == '__main__':
    unittest.main()
