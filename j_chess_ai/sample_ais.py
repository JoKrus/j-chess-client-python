import j_chess_generated
from . import base_ai


class FoolsMateAi(base_ai.BaseAi):
    moveMap = {
        "w": [j_chess_generated.MoveData(from_value="f2", to="f3"),
              j_chess_generated.MoveData(from_value="g2", to="g4")],
        "b": [j_chess_generated.MoveData(from_value="e7", to="e5"),
              j_chess_generated.MoveData(from_value="d8", to="h4")]
    }

    def make_move(self, await_move: j_chess_generated.AwaitMoveMessage) -> j_chess_generated.MoveData:
        return self.__class__.moveMap[await_move.position.split(" ")[1]][int(await_move.position.split(" ")[-1]) - 1]
