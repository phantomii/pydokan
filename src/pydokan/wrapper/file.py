# coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

from . import FlagsWrapper
from ..consts import *
from ..struct import *

class AccessMode(FlagsWrapper):
    flags = [
        ('GENERIC_ALL',     GENERIC_ALL),
        ('GENERIC_EXECUTE', GENERIC_EXECUTE),
        ('GENERIC_WRITE',   GENERIC_WRITE),
        ('GENERIC_READ',    GENERIC_READ),
        
        ('STANDARD_RIGHTS_ALL',     STANDARD_RIGHTS_ALL),
        ('SPECIFIC_RIGHTS_ALL', SPECIFIC_RIGHTS_ALL),
        ('FILE_ALL_ACCESS',      FILE_ALL_ACCESS),
        
        ('STANDARD_RIGHTS_READ',    STANDARD_RIGHTS_READ),
        ('STANDARD_RIGHTS_WRITE',   STANDARD_RIGHTS_WRITE),
        ('STANDARD_RIGHTS_EXECUTE', STANDARD_RIGHTS_EXECUTE),
        
        ('FILE_GENERIC_EXECUTE', FILE_GENERIC_EXECUTE),
        ('FILE_GENERIC_READ',    FILE_GENERIC_READ),
        ('FILE_GENERIC_WRITE',   FILE_GENERIC_WRITE),
        
        ('DELETE',       DELETE),
        ('READ_CONTROL', READ_CONTROL),
        ('WRITE_DAC',    WRITE_DAC),
        ('WRITE_OWNER',  WRITE_OWNER),
        ('SYNCHRONIZE',  SYNCHRONIZE),
        
        ('FILE_READ_DATA',            FILE_READ_DATA),
        ('FILE_LIST_DIRECTORY',       FILE_LIST_DIRECTORY),
        ('FILE_ADD_FILE',             FILE_ADD_FILE),
        ('FILE_WRITE_DATA',           FILE_WRITE_DATA),
        ('FILE_ADD_SUBDIRECTORY',     FILE_ADD_SUBDIRECTORY),
        ('FILE_APPEND_DATA',          FILE_APPEND_DATA),
        ('FILE_CREATE_PIPE_INSTANCE', FILE_CREATE_PIPE_INSTANCE),
        ('FILE_READ_EA',              FILE_READ_EA),
        ('FILE_WRITE_EA',             FILE_WRITE_EA),
        ('FILE_EXECUTE',              FILE_EXECUTE),
        ('FILE_TRAVERSE',             FILE_TRAVERSE),
        ('FILE_DELETE_CHILD',         FILE_DELETE_CHILD),
        ('FILE_READ_ATTRIBUTES',      FILE_READ_ATTRIBUTES),
        ('FILE_WRITE_ATTRIBUTES',     FILE_WRITE_ATTRIBUTES)
    ]
    
class ShareMode(FlagsWrapper):
    flags = [
        ('FILE_SHARE_NULL',   FILE_SHARE_NULL),
        ('FILE_SHARE_READ',   FILE_SHARE_READ),
        ('FILE_SHARE_WRITE',  FILE_SHARE_WRITE),
        ('FILE_SHARE_DELETE', FILE_SHARE_DELETE)
    ]
    
class CreationDisposition(FlagsWrapper):
    flags = [
        ('CREATE_NEW',        CREATE_NEW),
        ('CREATE_ALWAYS',     CREATE_ALWAYS),
        ('OPEN_EXISTING',     OPEN_EXISTING),
        ('OPEN_ALWAYS',       OPEN_ALWAYS),
        ('TRUNCATE_EXISTING', TRUNCATE_EXISTING)
    ]
    
    def debug_repr(self):
        flags = [f for f, m in self.flags if self == m]
        debug = ' | '.join(flags) if len(flags) else '0'
        return debug

class FlagsAndAttributes(FlagsWrapper):
    flags = [
        ('FILE_ATTRIBUTE_READONLY',            FILE_ATTRIBUTE_READONLY),
        ('FILE_ATTRIBUTE_HIDDEN',              FILE_ATTRIBUTE_HIDDEN),
        ('FILE_ATTRIBUTE_SYSTEM',              FILE_ATTRIBUTE_SYSTEM),
        ('FILE_ATTRIBUTE_DIRECTORY',           FILE_ATTRIBUTE_DIRECTORY),
        ('FILE_ATTRIBUTE_ARCHIVE',             FILE_ATTRIBUTE_ARCHIVE),
        ('FILE_ATTRIBUTE_DEVICE',              FILE_ATTRIBUTE_DEVICE),
        ('FILE_ATTRIBUTE_NORMAL',              FILE_ATTRIBUTE_NORMAL),
        ('FILE_ATTRIBUTE_TEMPORARY',           FILE_ATTRIBUTE_TEMPORARY),
        ('FILE_ATTRIBUTE_SPARSE_FILE',         FILE_ATTRIBUTE_SPARSE_FILE),
        ('FILE_ATTRIBUTE_REPARSE_POINT',       FILE_ATTRIBUTE_REPARSE_POINT),
        ('FILE_ATTRIBUTE_COMPRESSED',          FILE_ATTRIBUTE_COMPRESSED),
        ('FILE_ATTRIBUTE_OFFLINE',             FILE_ATTRIBUTE_OFFLINE),
        ('FILE_ATTRIBUTE_NOT_CONTENT_INDEXED', FILE_ATTRIBUTE_NOT_CONTENT_INDEXED),
        ('FILE_ATTRIBUTE_ENCRYPTED',           FILE_ATTRIBUTE_ENCRYPTED),
        ('FILE_ATTRIBUTE_VIRTUAL',             FILE_ATTRIBUTE_VIRTUAL),
        
        ('FILE_FLAG_POSIX_SEMANTICS',    FILE_FLAG_POSIX_SEMANTICS),
        ('FILE_FLAG_OPEN_NO_RECALL',     FILE_FLAG_OPEN_NO_RECALL),
        ('FILE_FLAG_OPEN_REPARSE_POINT', FILE_FLAG_OPEN_REPARSE_POINT),
        ('FILE_FLAG_BACKUP_SEMANTICS',   FILE_FLAG_BACKUP_SEMANTICS),
        ('FILE_FLAG_DELETE_ON_CLOSE',    FILE_FLAG_DELETE_ON_CLOSE),
        ('FILE_FLAG_SEQUENTIAL_SCAN',    FILE_FLAG_SEQUENTIAL_SCAN),
        ('FILE_FLAG_RANDOM_ACCESS',      FILE_FLAG_RANDOM_ACCESS),
        ('FILE_FLAG_NO_BUFFERING',       FILE_FLAG_NO_BUFFERING),
        ('FILE_FLAG_OVERLAPPED',         FILE_FLAG_OVERLAPPED),
        ('FILE_FLAG_WRITE_THROUGH',      FILE_FLAG_WRITE_THROUGH)
    ]