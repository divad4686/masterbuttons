from enum import Enum
from functools import reduce
from collections import namedtuple
from mastermind_logic import calculate_move

GameCreatedEvent = namedtuple("GameCreatedEvent", "id_game game_pattern")
PlayerPlayedEvent = namedtuple("PlayerPlayedEvent", "id_game played_pattern result")


class GameStatus(Enum):
    PLAYING = 1
    FINISHED = 2


GameStatusAggregate = namedtuple("GameStatusAggregate", "game_pattern plays_played status")


def apply_event_game_status(game_status, event):
    if isinstance(event, GameCreatedEvent):
        game = GameStatusAggregate(event.game_pattern, game_status.plays_played, game_status.status)
        return game

    if isinstance(event, PlayerPlayedEvent) and game_status.status == GameStatus.PLAYING:
        plays = game_status.plays_played
        plays.append(event)
        status = game_status.status
        if event.result.Black == 4:
            status = GameStatus.FINISHED
        game = GameStatusAggregate(game_status.game_pattern, plays, status)
        return game

    return game_status


def create_game_status_agregate(events):
    return reduce(apply_event_game_status, events, GameStatusAggregate(None, [], GameStatus.PLAYING))


def make_move(id_game, game_pattern, played_pattern):
    move_result = calculate_move(game_pattern, played_pattern)
    return PlayerPlayedEvent(id_game, played_pattern, move_result)
