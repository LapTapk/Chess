import http.server
import threading
from chessLogic.Board import Board
import re

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
    print(address)

    server_thr = threading.Thread(target=__start_server)
    server_thr.daemon = True
    server_thr.start()


class Server(http.server.HTTPServer):
    def __init__(self, server_address, handler, brd):
        super().__init__(server_address, handler)
        self.brd = brd
        self.moves_cnt = 0
        self.connected = 0


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
                print(400)
                self.send_response(400, message="Bad format")
                self.end_headers()
                return

            nums = list(map(int, move.split()))
            frm, to = (nums[0], nums[1]), (nums[2], nums[3])
            moved = self.server.brd.try_move(frm, to)
            if not moved:
                print(403)
                self.send_response(403)
                self.end_headers()
                return

            self.server.moves_cnt += 1
            self.send_response(200)
            self.end_headers()
