# -*- coding: utf-8 -*-

import socket
import threading
import pickle


class Listener(object):

    def __init__(self, port):

        self.l = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', port))
        self.socket.listen(1)
        self.clients = {}
        self.conn = None
        self.exit = False

    def listener(self):
        while not self.exit:
            try:
                self.l.acquire()
                self.accept_conn()

            except:
                pass

            finally:
                self.l.release()

    def start_listener(self):
        thread = threading.Thread(target=self.listener)
        thread.start()

    def accept_conn(self):
        conn, adr = self.socket.accept()
        self.clients[adr[0]] = conn

    def listen(self):

        data = self.conn.recv(4098)
        if data:
            return pickle.loads(data)

        return None
