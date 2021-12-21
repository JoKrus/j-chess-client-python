import socket as socket_lib
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from j_chess_generated import JchessMessage


class JChessIOHandler:
    def __init__(self, socket: socket_lib.socket):
        self.socket = socket
        self.parser = XmlParser()
        self.config = SerializerConfig(pretty_print=False)
        self.serializer = XmlSerializer(config=self.config)

    def read_msg(self):
        msg_len = self.read_header()
        xml = self.socket.recv(msg_len).decode("utf-8")
        return xml

    def read_header(self):
        return int.from_bytes(self.socket.recv(4), "big")

    def read_j_chess(self):
        xml = self.read_msg()
        return self.xml_to_j_chess(xml)

    def xml_to_j_chess(self, xml):
        return self.parser.from_string(xml, JchessMessage)

    def send_j_chess(self, j_chess_msg: JchessMessage):
        msg = self.j_chess_to_xml(j_chess_msg)
        # TODO check if bug
        length = len(msg)
        length_bytes = length.to_bytes(4, "big")

        self.socket.send(length_bytes + f"{msg}".encode('utf-8'))

    def j_chess_to_xml(self, j_chess_msg: JchessMessage):
        return self.serializer.render(j_chess_msg)
