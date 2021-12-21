from abc import ABC, abstractmethod
import j_chess_generated


class BaseAi(ABC):
    @abstractmethod
    def make_move(self, await_move: j_chess_generated.AwaitMoveMessage) -> j_chess_generated.MoveData:
        pass
