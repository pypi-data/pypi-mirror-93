


__author__ = 'testrelease'
__copyright__ = 'Copyright 2020'

__license__ = "BSD 3-Clause License"

#__all__ = ['Testrelease']
print(__version__)
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(current_dir) 

from .utils import (
    say,
    yell
    )

'''
class Testrelease():

    def __init__(self):
        print('Testrelease initialized.')

'''
