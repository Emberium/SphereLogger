# -*- coding: utf-8 -*-

from SPLib import template_txt, tcp_template_txt


def generate_mail(login, password, server, port, receiver,
                  output, screen_logger=False):

    with open('templates/mail-screen-logger-template.py' if screen_logger else 'templates/mail-template.py', 'r'
              ) as f:
        template = f.read()

    with open('output/' + output, 'w', encoding='utf-8') as f:
        f.write(template_txt.format(
            login=login,
            password=password,
            smtp=server,
            port=port,
            rec=receiver
        ) + template)

    return True


def generate_tcp(host, port, output):

    with open('templates/tcp-template.py', 'r') as f:
        template = f.read()

    with open('output/' + output, 'w') as f:
        f.write(tcp_template_txt.format(
            port=port,
            host=host
        ) + template)

    return True
