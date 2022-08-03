import socket
import time
import threading

class Gate:
    def __init__(self):
        '''
        :param
        '''
        self.__is_open = False

    def open(self):
        self.__is_open = True

    def close(self):
        self.__is_open = False

    def is_open(self):
        return self.__is_open

    def deley(self):
        time.sleep(3)
        self.close()


gate = Gate()
while True:
    try:
        with socket.socket() as s:
            host = 'gate-mock'
            port = 5050

            s.bind((host, port))
            print(f'socket binded to {port}')
            s.listen()
            con, addr = s.accept()
            with con:
                while True:
                    data = con.recv(1)
                    match data:
                        case b'o':
                            if gate.is_open():
                                con.sendall(b'9')
                            else:
                                gate.open()
                                con.sendall(b'0')
                                threads = []
                                thread = threading.Thread(target=gate.deley)
                                threads.append(thread)
                                thread.start()
                        case b's':
                            if gate.is_open():
                                con.sendall(b'o')
                            else:
                                con.sendall(b'c')
                        case _:
                                con.sendall(b'9')
    except Exception as e:
        print(e)
