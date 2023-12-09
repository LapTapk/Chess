import http.client


class Client:
    def __init__(self, host, port):
        self.connection = http.client.HTTPConnection(host, port)

    def send_move(self, frm, to):
        self.connection.request('POST', '', body=' '.join(frm + to))

        response = self.connection.getresponse()
        return response.getcode() == '200'
    
    def try_get_board(self):
        pass
