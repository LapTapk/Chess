'''
Модуль, ответственный за единственный http сервер в приложении.
'''
from typing import *
import http.server
import threading
from chessLogic.Board import Board
import re
import json


server = None
'''
Экземпляр сервера. Пока сервер не инициализирован равняет None
'''
is_init = False
'''Состояние, показывающее инициализирован ли сервер'''


def __start_server() -> None:
    '''Закрытая функция, запускающая сервер и, в случае закрытия 
    приложения, закрывающая его.'''
    try:
        server.serve_forever()
    except:
        server.server_close()
        exit()


def init(address: Tuple[LiteralString, int]) -> None:
    '''Инициализатор сервера. Запускает функцию *__start_server* 
    парралельно основной программе.

    :param address: адрес, который будет иметь запускаемый сервер.
    '''
    global server, is_init
    if is_init:
        raise Exception('Server s already initialized')

    new_brd = Board()
    new_brd.startPosition()
    server = Server(address, ReqauestHandler, new_brd)

    server_thr = threading.Thread(target=__start_server)
    server_thr.daemon = True
    server_thr.start()
    is_init = True


class Server(http.server.HTTPServer):
    '''Сущность сервера http.'''

    def __init__(self, server_address: Tuple[LiteralString, int], handler: http.server.BaseHTTPRequestHandler, brd: Board):
        '''
        :param server_address: адрес сервера.
        :param handler: тип обработчика запросов.
        :param brd: шаматная доска, хранимая на сервере.
        '''
        super().__init__(server_address, handler)
        self.brd: Board = brd
        '''Шахматная доска, хранимая на сервере.'''
        self.moves_cnt: int = 0
        '''Количество проведенных ходов.'''
        self.connected: int = 0
        '''Количество подключенных игроков.'''
        self.msg_black: Dict[LiteralString, LiteralString | bool] | None = None
        '''Сообщение, переданне черным.'''
        self.msg_white: Dict[LiteralString, LiteralString | bool] | None = None
        '''Сообщение, переданное белым.'''
        self.state: LiteralString | Tuple[LiteralString,
                                          LiteralString] = 'neutral'
        '''Поле, хранящее состояние, в каком сейчас находится игра.
        Может быть neutral, (checkmate, color), (palemate, color), 
        где color - цвет игрока, на ходе которого случилось событие'''


class ReqauestHandler(http.server.BaseHTTPRequestHandler):
    '''Класс обработчика запросов для сервера.'''

    def get_msg(self, for_white: bool) -> None:
        '''Метод, отвечающий за отправку сообщения для белых или черных
        клиенту.

        :param for_white: состояние, указывающее на то, должно ли быть передано сообщение для белых или для черных
        '''
        msg = self.server.msg_white if for_white else self.server.msg_black
        data = None
        if msg == None:
            data = b''
        else:
            data = json.dumps(msg).encode()
        self.wfile.write(data)

    def do_GET(self) -> None:
        '''Метод обработки запроса GET. 
        path == /moves_cnt -> отправка move_cnt.
        path == /board -> отправка brd.
        path == /is_chess -> отправляет утверждение, что это сервер для шахмат.
        path == /conn -> отправка connected.
        path == /msg_black|/msg_white -> отправка сообщения для черных|белых.
        path == /state -> отправка состояния на текущий момент'''
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
            self.get_msg(True)
        elif self.path == '/msg/black':
            self.get_msg(False)
        elif self.path == '/state':
            self.wfile.write(str(self.server.state).encode())

    def post_conn(self) -> None:
        '''Метод, отвечающий за прием нового подключившегося клиента.'''
        self.server.connected += 1
        self.send_response(200)
        self.end_headers()

    def post_move(self) -> None:
        '''Метод, отвечающий за прием нового хода. 
        если ход легальный, возвращает код 200, 
        если нелегальный, возвращает 403, 
        если ход передан в некправильнои формате, возвращает 400.
        Если код 200, значит был сделан ход и обновлено число ходов.
        '''
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
        state = self.server.brd.try_move(frm, to)
        if not state and frm != to:
            self.send_response(403)
            self.end_headers()
            return

        if frm != to:
            self.server.moves_cnt += 1
            self.server.state = state
            self.send_response(200)
        else:
            self.send_response(202)
        self.end_headers()

    def post_msg(self, sender_is_white: bool) -> None:
        '''Метод, отвечающий за прием сообещния для белых|черных

        :param sender_is_white: состояние, показывающее от кого было прислано сообщение'''
        msg_sender = self.server.msg_white if sender_is_white else self.server.msg_black
        length = int(self.headers['Content-Length'])
        msg = self.rfile.read(length)
        data = json.loads(msg)

        is_illegal1 = data['response'] and (
            msg_sender == None or msg_sender['response'])
        is_illegal2 = not data['response'] and (
            msg_sender != None and not msg_sender['response'])
        if is_illegal1 or is_illegal2:
            self.send_response(403)
            self.end_headers()
            return

        if sender_is_white:
            self.server.msg_white = None
            self.server.msg_black = data
        else:
            self.server.msg_black = None
            self.server.msg_white = data
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        '''Метод, отвечающий за прием запросов.
        path == /conn -> *post_conn*.
        path == /move -> *post_move*.
        path == /msg/black -> *post_msg(True)*.
        path == /msg/white -> *post_msg(False)*'''
        if self.path == '/conn':
            self.post_conn()
        elif self.path == '/move':
            self.post_move()
        elif self.path == '/msg/black':
            self.post_msg(True)
        elif self.path == '/msg/white':
            self.post_msg(False)
