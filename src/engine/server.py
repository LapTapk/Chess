import http.server


cur_sender = None
cur_receiver = None

http.server.HTTPServer()

class Server(http.server.HTTPServer):
    def __init__(self, server_adress, handler, brd):
        super.__init__(server_adress, handler)
        self.last_move = last_move


class ReqauestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        if self.path == '/last_move':
            last_move = self.server.last_move()
            self.wfile.write(' '.join(last_move).encode())

    def do_POST(self):
        self.send_response(200)

        if self.path == 