import http.client


class Client:
    def __init__(self, host, port, is_white):
        self.connection = http.client.HTTPConnection(host, port)
        self.is_white = is_white
        self.local_moves_cnt = 0

    def connect(self):
        self.connetion.connect()

        self.connection.request('GET', '/is_chess')
        response = self.connection.getresponse()
        response_msg = response.read().decode() 
        return response.getcode() == '200' and response_msg == "YES"

    def send_move(self, frm, to):
        self.connection.request('POST', '', body=' '.join(frm + to))

        response = self.connection.getresponse()
        return response.getcode() == '200'
    
    def try_get_board(self):
        pass

    def has_moved(self):
        self.connection.request('GET', '/moves_cnt')
        response = self.connection.getresponse()
        server_moves_cnt = int(response.read().decode())

        return self.local_moves_cnt == server_moves_cnt
