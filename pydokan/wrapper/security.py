#coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

from . import FlagsWrapper
from ..consts import *

class SecurityInfo(FlagsWrapper):
    flags = [
        ('OWNER_SECURITY_INFORMATION',     OWNER_SECURITY_INFORMATION),
        ('GROUP_SECURITY_INFORMATION',     GROUP_SECURITY_INFORMATION),
        ('DACL_SECURITY_INFORMATION',      DACL_SECURITY_INFORMATION),
        ('SACL_SECURITY_INFORMATION',      SACL_SECURITY_INFORMATION),
        ('LABEL_SECURITY_INFORMATION',     LABEL_SECURITY_INFORMATION),
        ('ATTRIBUTE_SECURITY_INFORMATION', ATTRIBUTE_SECURITY_INFORMATION),
        ('SCOPE_SECURITY_INFORMATION',     SCOPE_SECURITY_INFORMATION)
    ]
    
    # Значение приходит по ссылке
    by_pointer = True
