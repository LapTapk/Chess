import http.server
import asyncio
from chessLogic.Board import Board
import re

async def init(adress):
    new_brd = Board()
    server = Server(adress, ReqauestHandler, new_brd)

    try:
        await asyncio.run(server.serve_forever)
    except:
        server.server_close()
        exit()

class Server(http.server.HTTPServer):
    def __init__(self, server_adress, handler, brd):
        super.__init__(server_adress, handler)
        self.brd = brd
        self.moves_cnt = 0


class ReqauestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        if self.path == '/moves_cnt':
            self.wfile.write(str(self.server.moves_cnt).encode())
        elif self.path == '/board':
            self.wfile.write(self.server.brd.serialize())

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
        