from typing import *
import http.client
import json
from chessLogic.Board import Board

class Client:
    '''Класс клиента, отвественный за запросы к серверу.'''
    def __init__(self, host: LiteralString, port: int, is_white: bool):
        '''
        При создании класса отправляет серверу запрос POST, 
        гласящем о подключении клиента. 

        :param host: адрес сервера, к которому будет подключаться клиент 
        :param port: порт сервера, к которому будет подключаться клиент
        :param is_white: покзывает, играет ли этот клиент за белых.
        '''
        self.address: Tuple[LiteralString, int] = (host, port)
        '''Адрес сервера, к которому будет подключаться клиент'''
        self.is_white: bool = is_white
        '''Состояние, показывающее играет ли этот клиент за белых или за черных'''
        self.local_moves_cnt: int = 0
        '''Число ходов, которые зафиксировал клиент. Необходимо для обновления доски.'''

        conn = http.client.HTTPConnection(host, port)
        conn.request('POST', '/conn')
        conn.close()

    def send_move(self, frm: Tuple[int, int], to: Tuple[int, int]) -> bool:
        '''Метод, отвечающий за отправку хода северу 
        
        :param frm: откуда перенесена фигура.
        :param to: куда перенесена фигура.
        :return: был ли сделан ход'''
        if self.is_white:
            frm = (7 - frm[0], 7 - frm[1])
            to = (7 - to[0], 7 - to[1])

        msg = ' '.join(map(str, frm + to))
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('POST', '/move', body=msg,
                     headers={'Content-Type': 'text/plain', 'Content-Length': '7'})

        response = conn.getresponse()
        return response.getcode()

    def get_board(self) -> Board:
        '''Метод, отвечающий за получение актуального состояния доски с сервера.
        
        :return: версия поля с сервера.'''
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/board')
        response = conn.getresponse()
        b_data = json.loads(response.read().decode())

        moves_cnt = self.get_moves()
        self.local_moves_cnt = moves_cnt

        return Board.deserialize(b_data)

    def get_moves(self) -> int:
        '''Метод, отвечающий за получение кол-ва поизведенных ходов с сервера.

        :return: актуальное кол-во произведенных ходов.
        '''
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/moves_cnt')
        response = conn.getresponse()
        return int(response.read().decode())

    def has_moved(self) -> bool:
        '''Метод, проверяющий был ли произведен ход
        
        :return: был ли произведен ход'''
        server_moves_cnt = self.get_moves()
        return self.local_moves_cnt != server_moves_cnt

    def get_conn(self) -> int:
        '''Метод, возвращающий кол-во подключений к серверу.
        
        :return: кол-во подключений к серверу.'''
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/conn')
        response = conn.getresponse()
        return int(response.read().decode())

    def get_msg(self) -> Dict[LiteralString, LiteralString | bool]:
        '''Метод, получаеющий сообщение для цвета данного клиента.
        
        :return: сообщение для цвета данного клиента.'''
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

    def send_msg(self, text: LiteralString, is_response: bool) -> bool:
        '''Метод, отправляющий сообщение противоположному цвету.
        
        :param text: текст сообщения
        :param is_response: обозначает, является ли отправляемое сообщение ответом на вопрос
        :return: было ли принято сообщение'''
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        color = 'black' if self.is_white else 'white'
        msg = {'response': is_response, 'text': text}
        data = json.dumps(msg)
        conn.request('POST', '/msg/' + color, body=data,
                     headers={'Content-Type': 'text/plain', 'Content-Length': str(len(data))})

        response = conn.getresponse()
        return response.getcode == 200 

    def get_state(self) -> LiteralString | Tuple[LiteralString, LiteralString]:
        '''Метод, получающий состояние на текущий ход с сервера.

        :return: статус игры на текущий ход'''
        host, port = self.address
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/state')
        response = conn.getresponse()

        return response.read().decode()