# coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

from . import FlagsWrapper, StructWrapper
from ..struct import *

class DokanOptions(FlagsWrapper):
    flags = [
        ('DOKAN_OPTION_DEBUG',      DOKAN_OPTION_DEBUG),
        ('DOKAN_OPTION_STDERR',     DOKAN_OPTION_STDERR),
        ('DOKAN_OPTION_ALT_STREAM', DOKAN_OPTION_ALT_STREAM),
        ('DOKAN_OPTION_KEEP_ALIVE', DOKAN_OPTION_KEEP_ALIVE),
        ('DOKAN_OPTION_NETWORK',    DOKAN_OPTION_NETWORK),
        ('DOKAN_OPTION_REMOVABLE',  DOKAN_OPTION_REMOVABLE),
    ]
    
class DokanFileInfo(StructWrapper):
    fields = [
            ('Context',          'context'),
            ('DokanContext',     'dokan_context'),
            ('DokanOptions',     'dokan_options'),
            ('ProcessId',        'process_id'),
            ('IsDirectory',      'is_directory'),
            ('DeleteOnClose',    'delete_on_close'),
            ('PagingIo',         'paging_io'),
            ('SynchronousIo',    'synchronous_io'),
            ('Nocache',          'no_cache'),
            ('WriteToEndOfFile', 'write_to_end_of_file')
        ]
    
    multiline = True
    
    field = StructWrapper.field
    field_bool = StructWrapper.field_bool
    field_opts = lambda x: property(lambda s: DokanOptionsStruct(getattr(s.struct, x)),
                                    lambda s, v: setattr(s.struct, x, v))
    
    context              = field('Context')
    dokan_context        = field('DokanContext')
    dokan_options        = field_opts('DokanOptions')
    process_id           = field('ProcessId')
    is_directory         = field_bool('IsDirectory')
    delete_on_close      = field('DeleteOnClose')
    paging_io            = field('PagingIo') 
    synchronous_io       = field('SynchronousIo')
    no_cache             = field('Nocache')
    write_to_end_of_file = field('WriteToEndOfFile')
    
class DokanOptionsStruct(StructWrapper):
    fields = [
        ('Version',       'version'),
        ('ThreadCount',   'thread_count'),
        ('Options',       'options'),
        ('GlobalContext', 'global_context'),
        ('MountPoint',    'mount_point')
    ]
    
    field = StructWrapper.field
    field_opts = lambda x: property(lambda s: DokanOptions(getattr(s.struct, x)),
                                    lambda s, v: setattr(s.struct, x, v))  
      
    version        = field('Version')
    thread_count   = field('ThreadCount')
    options        = field_opts('Options')
    global_context = field('GlobalContext')
    mount_point    = field('MountPoint')