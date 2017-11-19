# -*- coding: utf-8 -*-

import configparser
import updater

__version__ = updater.get_current()

parser = configparser.ConfigParser()
parser.read('config.ini')

if parser.get('GENERAL', 'Colored') == "1":
    from .colors import *

else:
    from .no_colors import *

from .text import *
from .mailing import *
from .tcp import *
from .generator import *
from .shell import *

