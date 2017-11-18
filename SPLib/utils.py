# -*- coding: utf-8 -*-


def c_red(text):
    return '\033[91m' + str(text) + '\033[0m'


def c_blue(text):
    return '\33[94m' + str(text) + '\033[0m'


def c_yellow(text):
    return '\33[93m' + str(text) + '\033[0m'


def c_white(text):
    return '\33[97m' + str(text) + '\033[0m'


def c_magenta(text):
    return '\033[1;35m' + str(text) + '\033[0m'


def c_green(text):
    return '\033[1;32m' + str(text) + '\033[0m'
