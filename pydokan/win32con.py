# coding=utf8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

# Disk Flags
FILE_CASE_SENSITIVE_SEARCH                                          = 0x00000001
FILE_CASE_PRESERVED_NAMES                                           = 0x00000002
FILE_UNICODE_ON_DISK                                                = 0x00000004
FILE_PERSISTENT_ACLS                                                = 0x00000008
FILE_FILE_COMPRESSION                                               = 0x00000010
FILE_VOLUME_QUOTAS                                                  = 0x00000020
FILE_SUPPORTS_SPARSE_FILES                                          = 0x00000040
FILE_SUPPORTS_REPARSE_POINTS                                        = 0x00000080
FILE_SUPPORTS_REMOTE_STORAGE                                        = 0x00000100
FS_LFN_APIS                                                         = 0x00004000
FILE_VOLUME_IS_COMPRESSED                                           = 0x00008000
FILE_SUPPORTS_OBJECT_IDS                                            = 0x00010000
FILE_SUPPORTS_ENCRYPTION                                            = 0x00020000
FILE_NAMED_STREAMS                                                  = 0x00040000
FILE_READ_ONLY_VOLUME                                               = 0x00080000
FILE_SEQUENTIAL_WRITE_ONCE                                          = 0x00100000
FILE_SUPPORTS_EXTENDED_ATTRIBUTES                                   = 0x00800000
FILE_SUPPORTS_HARD_LINKS                                            = 0x00400000
FILE_SUPPORTS_OPEN_BY_FILE_ID                                       = 0x01000000
FILE_SUPPORTS_TRANSACTIONS                                          = 0x00200000
FILE_SUPPORTS_USN_JOURNAL                                           = 0x02000000


# File Attributes
FILE_ATTRIBUTE_MYFILE                                               = 0x00000000
FILE_ATTRIBUTE_READONLY                                             = 0x00000001
FILE_ATTRIBUTE_HIDDEN                                               = 0x00000002
FILE_ATTRIBUTE_SYSTEM                                               = 0x00000004
FILE_ATTRIBUTE_DIRECTORY                                            = 0x00000010
FILE_ATTRIBUTE_ARCHIVE                                              = 0x00000020
FILE_ATTRIBUTE_ENCRYPTED                                            = 0x00000040
FILE_ATTRIBUTE_NORMAL                                               = 0x00000080
FILE_ATTRIBUTE_TEMPORARY                                            = 0x00000100
FILE_ATTRIBUTE_SPARSE_FILE                                          = 0x00000200
FILE_ATTRIBUTE_REPARSE_POINT                                        = 0x00000400
FILE_ATTRIBUTE_COMPRESSED                                           = 0x00000800
FILE_ATTRIBUTE_OFFLINE                                              = 0x00001000
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED                                  = 0x00002000
FILE_ATTRIBUTE_VIRTUAL                                              = 0x00010000

# Share mode
FILE_SHARE_READ                                                     = 1
FILE_SHARE_WRITE                                                    = 2
FILE_SHARE_DELETE                                                   = 4

# Access mode
GENERIC_ALL                                                         = 0x10000000
GENERIC_EXECUTE                                                     = 0x20000000
GENERIC_WRITE                                                       = 0x40000000
GENERIC_READ                                                        = 0x80000000

FILE_READ_DATA                                                      = 1
FILE_LIST_DIRECTORY                                                 = 1
FILE_WRITE_DATA                                                     = 2
FILE_ADD_FILE                                                       = 2
FILE_APPEND_DATA                                                    = 4
FILE_ADD_SUBDIRECTORY                                               = 4
FILE_CREATE_PIPE_INSTANCE                                           = 4
FILE_READ_EA                                                        = 8
FILE_READ_PROPERTIES                                                = 8
FILE_WRITE_EA                                                       = 16
FILE_WRITE_PROPERTIES                                               = 16
FILE_EXECUTE                                                        = 32
FILE_TRAVERSE                                                       = 32
FILE_DELETE_CHILD                                                   = 64
FILE_READ_ATTRIBUTES                                                = 128
FILE_WRITE_ATTRIBUTES                                               = 256
STANDARD_RIGHTS_READ                                                = 0x20000
STANDARD_RIGHTS_WRITE                                               = 0x20000
STANDARD_RIGHTS_EXECUTE                                             = 0x20000
STANDARD_RIGHTS_REQUIRED                                            = 0xF0000
SYNCHRONIZE                                                         = 0x100000
FILE_ALL_ACCESS      = (STANDARD_RIGHTS_REQUIRED|SYNCHRONIZE|0x1FF)
FILE_GENERIC_READ    = (STANDARD_RIGHTS_READ|FILE_READ_DATA|FILE_READ_ATTRIBUTES|
                        FILE_READ_EA|SYNCHRONIZE)
FILE_GENERIC_WRITE   = (STANDARD_RIGHTS_WRITE|FILE_WRITE_DATA|FILE_WRITE_ATTRIBUTES|
                        FILE_WRITE_EA|FILE_APPEND_DATA|SYNCHRONIZE)
FILE_GENERIC_EXECUTE = (STANDARD_RIGHTS_EXECUTE|FILE_READ_ATTRIBUTES|FILE_EXECUTE|
                        SYNCHRONIZE)

# Description
CREATE_NEW                                                          = 1
CREATE_ALWAYS                                                       = 2
OPEN_EXISTING                                                       = 3
OPEN_ALWAYS                                                         = 4
TRUNCATE_EXISTING                                                   = 5

#ERRORS
ERROR_FILE_NOT_FOUND                                                = 2
ERROR_PATH_NOT_FOUND                                                = 3
ERROR_ACCESS_DENIED                                                 = 5
ERROR_INVALID_HANDLE                                                = 6
ERROR_LOCK_VIOLATION                                                = 33
ERROR_FILE_EXISTS                                                   = 80
ERROR_ALREADY_ASSIGNED                                              = 85
ERROR_DISK_FULL                                                     = 112
ERROR_DIR_NOT_EMPTY                                                 = 145
ERROR_PATH_BUSY                                                     = 148
ERROR_NOT_LOCKED                                                    = 158
ERROR_LOCK_FAILED                                                   = 167
ERROR_ALREADY_EXISTS                                                = 183
ERROR_LOCKED                                                        = 212
ERROR_INVALID_LOCK_RANGE                                            = 307