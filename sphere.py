#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 SphereLogger
# Written by Ember
# https://github.com/Emberium/SphereLogger

from SPLib import *

import configparser
import updater
import sys


if __name__ == '__main__':

    _current = updater.get_current()
    _newest = updater.get_newest()

    if _current != _newest:
        if input(c_magenta('Update available. Do you want to install %s version? (Y/n)' % _newest)).upper() == 'Y':
            updater.update()

            print(c_magenta('Successful updated to %s'))
            sys.exit(0)

    parser = configparser.ConfigParser()
    parser.read('config.ini')

    sh = SphereShell(config=parser)
    sh.cmdloop()
