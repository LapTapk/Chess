import http.client
import json
from chessLogic.Board import Board


class Client:
    def __init__(self, host, port, is_white):
        self.connection = http.client.HTTPConnection(host, port)
        self.is_white = is_white
        self.local_moves_cnt = 0

    def send_move(self, frm, to):
        msg = ' '.join(frm + to)
        self.connection.request('POST', '', body=msg)

        response = self.connection.getresponse()
        return response.getcode() == 200
    
    def get_board(self):
        self.connection.request('GET', '/board')
        response = self.connection.getresponse()
        b_data = json.loads(response.read().decode())
        
        self.connection.request('GET', '/moves_cnt')
        response = self.connection.getresponse()
        moves_cnt = int(response.read().decode())
        self.local_moves_cnt = moves_cnt
        
        return Board.deserialize(b_data)
        

    def has_moved(self):
        self.connection.request('GET', '/moves_cnt')
        response = self.connection.getresponse()
        server_moves_cnt = int(response.read().decode())

        return self.local_moves_cnt == server_moves_cnt
