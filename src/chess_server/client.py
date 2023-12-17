import http.client
import json
from chessLogic.Board import Board
from engine import message_communication


class Client:
    def __init__(self, host, port, is_white):
        self.address = (host, port)
        self.is_white = is_white
        self.local_moves_cnt = 0

        conn = http.client.HTTPConnection(host, port)
        conn.request('POST', '/conn')
        conn.close()

    def send_move(self, frm, to):
        if self.is_white:
            frm = (7 - frm[0], 7 - frm[1])
            to = (7 - to[0], 7 - to[1])

        msg = ' '.join(map(str, frm + to))
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('POST', '/move', body=msg,
                     headers={'Content-Type': 'text/plain', 'Content-Length': '7'})

        response = conn.getresponse()
        return response.getcode() == 200

    def get_board(self):
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/board')
        response = conn.getresponse()
        b_data = json.loads(response.read().decode())

        moves_cnt = self.get_moves()
        self.local_moves_cnt = moves_cnt

        return Board.deserialize(b_data)

    def get_moves(self):
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/moves_cnt')
        response = conn.getresponse()
        return int(response.read().decode())

    def has_moved(self):
        server_moves_cnt = self.get_moves()
        return self.local_moves_cnt != server_moves_cnt

    def get_conn(self):
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/conn')
        response = conn.getresponse()
        return int(response.read().decode())

    def get_msg(self):
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        color = 'white' if self.is_white else 'black'
        conn.request('GET', '/msg/' + color)
        response = conn.getresponse()
        data = response.read()

        if data == b'':
            return None

        data = json.loads(data)
        return data

    def send_msg(self, text, is_response):
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        color = 'black' if self.is_white else 'white'
        msg = {'response': is_response, 'text': text}
        data = json.dumps(msg)
        conn.request('POST', '/msg/' + color, body=data,
                     headers={'Content-Type': 'text/plain', 'Content-Length': str(len(data))})

        response = conn.getresponse()
        return response.getcode == 200 
