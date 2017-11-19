#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 SphereLogger
# Written by Ember
# https://github.com/Emberium/SphereLogger

from SPLib import *

import configparser


if __name__ == '__main__':

    parser = configparser.ConfigParser()
    parser.read('config.ini')

    sh = SphereShell(config=parser)
    sh.cmdloop()
