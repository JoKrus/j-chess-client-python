import socket as socket_lib
import j_chess_generated
from j_chess_io.j_chess_io import JChessIOHandler
import uuid
import j_chess_ai.base_ai as base_ai
import j_chess_ai.sample_ais as sample_ais


class Client:
    def __init__(self, my_socket: socket_lib.socket, ai: base_ai):
        self.player_id = str(uuid.uuid4())
        self.j_chess_io_socket = JChessIOHandler(my_socket)
        self.is_running = True
        self.ai = ai

    def run(self):
        self.login()
        self.play()

    def login(self):
        login_msg = j_chess_generated.LoginMessage()
        login_msg.name = "reference_client_python"
        msg = j_chess_generated.JchessMessage()
        msg.login = login_msg
        msg.player_id = self.player_id
        msg.message_type = j_chess_generated.JchessMessageType.LOGIN
        self.j_chess_io_socket.send_j_chess(msg)

        reply = self.j_chess_io_socket.read_j_chess()
        # TODO handle error cases
        assert reply.message_type == j_chess_generated.JchessMessageType.LOGIN_REPLY
        self.player_id = reply.login_reply.new_id
        print(f"login successful with id={self.player_id}")

    def play(self):
        while self.is_running:
            msg = self.j_chess_io_socket.read_j_chess()
            if msg is None:
                continue

            if msg.message_type == j_chess_generated.JchessMessageType.HEART_BEAT:
                self.handle_heart_beat()
            elif msg.message_type == j_chess_generated.JchessMessageType.ACCEPT:
                self.handle_accept()
            elif msg.message_type == j_chess_generated.JchessMessageType.DISCONNECT:
                self.handle_disconnect()
            elif msg.message_type == j_chess_generated.JchessMessageType.MATCH_OVER:
                self.handle_match_over(msg.match_over)
            elif msg.message_type == j_chess_generated.JchessMessageType.MATCH_STATUS:
                self.handle_match_status(msg.match_status)
            elif msg.message_type == j_chess_generated.JchessMessageType.GAME_OVER:
                self.handle_game_over(msg.game_over)
            elif msg.message_type == j_chess_generated.JchessMessageType.AWAIT_MOVE:
                self.handle_await_move(msg.await_move)

    def handle_heart_beat(self):
        pass

    def handle_accept(self):
        pass

    def handle_disconnect(self):
        self.is_running = False

    def handle_match_over(self, match_over: j_chess_generated.MatchOverMessage):
        pass

    def handle_match_status(self, match_status: j_chess_generated.MatchStatusMessage):
        pass

    def handle_game_over(self, game_over: j_chess_generated.GameOverMessage):
        pass

    def handle_await_move(self, await_move: j_chess_generated.AwaitMoveMessage):
        move_data = self.ai.make_move(await_move)
        msg = j_chess_generated.JchessMessage()
        msg.player_id = self.player_id
        msg.message_type = j_chess_generated.JchessMessageType.MOVE
        move_msg = j_chess_generated.MoveMessage()
        move_msg.move = move_data
        msg.move = move_msg
        self.j_chess_io_socket.send_j_chess(msg)
        print(f"played move {move_data}")


if __name__ == '__main__':
    socket = socket_lib.create_connection(("localhost", 5123))
    client = Client(socket, sample_ais.FoolsMateAi())
    client.run()
