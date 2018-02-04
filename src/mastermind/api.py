import uuid
from flask import Flask, request
from flask_restplus import Resource, Api, fields

from mastermind_logic import Color
from game_aggregate import GameCreatedEvent, create_game_status_agregate, make_move, GameStatus
from serializer import serialize_game

APP = Flask(__name__)
API = Api(APP)


class EnumPrint(fields.Raw):
    def format(self, value):
        return value.name


GAMES = {}

PATTERN = fields.List(
    EnumPrint(enum=[e.name for e in Color]),
    example=['GREEN', 'BLUE', 'RED', 'PURPLE']
)
GAME_FIELDS = API.model('GAME', {
    'game_pattern': PATTERN})


@API.route('/create', methods=["post"])
class Game(Resource):
    @API.expect(GAME_FIELDS)
    def post(self):
        all_params = request.get_json()
        game_pattern = tuple(map(lambda color: Color[color], all_params['game_pattern']))
        id_game = uuid.uuid4()
        game_created = GameCreatedEvent(id_game, game_pattern)

        if id_game not in GAMES:
            GAMES[id_game] = []
        GAMES[id_game].append(game_created)
        return {'id_game': id_game.hex}


PLAY_FIELD = API.model('PLAY', {
    'id_game': fields.String,
    'played_pattern': PATTERN
})


@API.route('/play', methods=["post"])
class Play(Resource):
    @API.expect(PLAY_FIELD)
    def post(self):
        all_params = request.get_json()
        id_game = uuid.UUID(all_params['id_game'])
        try:
            played_pattern = tuple(map(lambda color: Color[color], all_params['played_pattern']))
        except KeyError:
            return "We could not parse the color values in the request"

        game = GAMES[id_game]
        game_status = create_game_status_agregate(game)

        if game_status.status == GameStatus.FINISHED:
            return "This game is already finished"
        if len(played_pattern) != len(game_status.game_pattern):
            return "This is not the correct size for a play"

        play_event = make_move(id_game, game_status.game_pattern, played_pattern)
        GAMES[id_game].append(play_event)
        return play_event.result._asdict()


MOVE_RESULT = API.model('Move result', {
    'Black': fields.Integer,
    'White': fields.Integer
})


class ResultPrint(fields.Raw):
    def format(self, value):
        return value.result.Black


@API.route('/status', methods=["get"])
class GameStatusInfo(Resource):
    @API.doc(params={'id_game': 'UUID in 32 hexadecimal format'})
    def get(self):
        id_game = uuid.UUID(request.args.get('id_game'))
        game = GAMES[id_game]
        game_aggregate = create_game_status_agregate(game)
        return serialize_game(game_aggregate)


if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True, port=80)
