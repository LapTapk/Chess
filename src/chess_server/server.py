import http.server
import threading
from chessLogic.Board import Board
import re
import json

server = None
is_init = False


def __start_server():
    try:
        server.serve_forever()
    except:
        server.server_close()
        exit()


def init(address):
    global server, is_init
    if is_init:
        raise Exception('Server s already initialized')

    is_init = True
    new_brd = Board()
    server = Server(address, ReqauestHandler, new_brd)

    server_thr = threading.Thread(target=__start_server)
    server_thr.daemon = True
    server_thr.start()


class Server(http.server.HTTPServer):
    def __init__(self, server_address, handler, brd):
        super().__init__(server_address, handler)
        self.brd = brd
        self.moves_cnt = 0
        self.connected = 0
        self.msg_black = None
        self.msg_white = None


class ReqauestHandler(http.server.BaseHTTPRequestHandler):
    def check_for_new_con(self):
        self.server.connected.add(self.address_string)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        if self.path == '/moves_cnt':
            self.wfile.write(str(self.server.moves_cnt).encode())
        elif self.path == '/board':
            self.wfile.write(self.server.brd.serialize().encode())
        elif self.path == '/is_chess':
            self.wfile.write('YES'.encode())
        elif self.path == '/conn':
            self.wfile.write(str(self.server.connected).encode())
        elif self.path == '/msg/white':
            data = json.dump(self.server.msg_white)
            self.wfile.write(data)
        elif self.path == '/msg/black':
            data = json.dump(self.server.msg_black)
            self.wfile.write(data)

    def do_POST(self):
        if self.path == '/conn':
            self.server.connected += 1
            self.send_response(200)
            self.end_headers()
        elif self.path == '/move':
            length = int(self.headers['Content-Length'])
            move = self.rfile.read(length).decode()

            coords_pat = r'\d \d \d \d'
            mtch = re.match(coords_pat, move)
            if not mtch:
                self.send_response(400, message="Bad format")
                self.end_headers()
                return

            nums = list(map(int, move.split()))
            frm, to = (nums[0], nums[1]), (nums[2], nums[3])
            moved = self.server.brd.try_move(frm, to)
            if not moved:
                self.send_response(403)
                self.end_headers()
                return

            self.server.moves_cnt += 1
            self.send_response(200)
            self.end_headers()
        elif self.path == '/msg/black':
            length = int(self.headers['Content-Length'])
            msg = self.rfile.read(length)
            data = json.dump(msg)

            is_illegal1 = data['response'] and (
                self.server.msg_white == None or self.msg_white['response'])
            is_illegal2 = not data['reponse'] and not self.msg_white['response']
            if is_illegal1 or is_illegal2:
                self.send_response(403)
                self.end_headers()
                return

            self.server.msg_black = data
            self.send_response(200)
            self.end_headers()
        elif self.path == '/msg/white':
            length = int(self.headers['Content-Length'])
            msg = self.rfile.read(length)
            data = json.dump(msg)

            is_illegal1 = data['response'] and (
                self.server.msg_black == None or self.server.msg_black['response'])
            is_illegal2 = not data['reponse'] and not self.server.msg_black['response']
            if is_illegal1 or is_illegal2:
                self.send_response(403)
                self.end_headers()
                return

            self.server.msg_white = data
            self.send_response(200)
            self.end_headers()
