import http.server
import threading
from chessLogic.Board import Board
import re

server = None
waiting = True
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


def wait_until_connection():
    global waiting
    waiting = True
    while waiting:
        pass


class Server(http.server.HTTPServer):
    def __init__(self, server_address, handler, brd):
        super().__init__(server_address, handler)
        self.brd = brd
        self.moves_cnt = 0


class ReqauestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response('200')

        if self.path == '/moves_cnt':
            self.wfile.write(str(self.server.moves_cnt).encode())
        elif self.path == '/board':
            self.wfile.write(self.server.brd.serialize())
        elif self.path == '/is_chess':
            self.wfile.write('YES'.encode())
            

    def do_POST(self):
        move = self.rfile.read().decode()

        coords_pat = r'\d \d \d \d'
        mtch = re.match(move, coords_pat)
        if not mtch:
            self.send_error(400, message="Bad format")
            return  
        
        nums = list(map(int, coords_pat.split()))
        frm, to = (nums[0], nums[1]), (nums[2], nums[3])
        moved = self.server.brd.try_move(frm, to)
        if not moved:
            self.send_error(403)

        self.server.moves_cnt += 1
        self.send_response(200)
        
    def do_CONNECT(self):
        print('hola')
        global waiting
        waiting = False
        self.send_response(200)
        