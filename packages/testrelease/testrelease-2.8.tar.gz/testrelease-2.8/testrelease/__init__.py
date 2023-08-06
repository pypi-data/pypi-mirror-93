
from ._version import __version__


__author__ = 'testrelease'
__copyright__ = 'Copyright 2020'

__license__ = "BSD 3-Clause License"

__all__ = ['testrelease']

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(current_dir) 

from .utils import (
    say,
    yell
    )





