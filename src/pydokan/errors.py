# coding=utf8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'


class PlatformNotSupported(Exception): pass


class ErrorVersionDokan(Exception): pass


class AccessDenie(Exception): pass


class DublicateClose(Exception): pass