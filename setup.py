from distutils.core import setup
import py2exe
import pygame
import screeninfo
import math
import random

setup(windows=['main.py'], requires=['py2exe', 'pygame', 'screeninfo'])
