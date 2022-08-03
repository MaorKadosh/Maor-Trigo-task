import socket
import time
import threading

class Gate:
        """
    A class used to represent Gate-Mock status

    ...

    Attributes
    ----------
    open : Boolean variable - True or False
        The status of the gate is open
    close : Boolean variable - True or False
        The status of the gate is close
    deley : int
        I'm decide to use thread- We don’t want to cause any downtime, but we also don’t want to wait longer than necessary to finish the migration. 
        Threads are a method of doing concurrency in Python. You can run multiple threads at once to increase your application’s throughput.

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
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
            # Threade for making delay of 3 seconds - during these seconds the gate will remain open.
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
