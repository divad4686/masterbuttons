def serialize_enum_list(enum_list):
    return list(map(lambda enum: enum.name, enum_list))


def serialize_result(result):
    return {"Black": result.Black, "White": result.White}


def serialize_play(play):
    return {"played_pattern": serialize_enum_list(play.played_pattern), "result": serialize_result(play.result)}


def serialize_plays(plays):
    return list(map(serialize_play, plays))


def serialize_game(game):
    return {"status": game.status.name, "game_pattern": serialize_enum_list(game.game_pattern), "plays_played": serialize_plays(game.plays_played)}
