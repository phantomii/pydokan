#coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

# Filesystem Flags
# @link: http://msdn.microsoft.com/en-us/library/aa364993(v=vs.85).aspx
FILE_CASE_SENSITIVE_SEARCH        = 0x00000001
FILE_CASE_PRESERVED_NAMES         = 0x00000002
FILE_UNICODE_ON_DISK              = 0x00000004
FILE_PERSISTENT_ACLS              = 0x00000008
FILE_FILE_COMPRESSION             = 0x00000010
FILE_VOLUME_QUOTAS                = 0x00000020
FILE_SUPPORTS_SPARSE_FILES        = 0x00000040
FILE_SUPPORTS_REPARSE_POINTS      = 0x00000080
#FILE_SUPPORTS_REMOTE_STORAGE    = 0x00000100
#FS_LFN_APIS                     = 0x00004000
FILE_VOLUME_IS_COMPRESSED         = 0x00008000
FILE_SUPPORTS_OBJECT_IDS          = 0x00010000
FILE_SUPPORTS_ENCRYPTION          = 0x00020000
FILE_NAMED_STREAMS                = 0x00040000
FILE_READ_ONLY_VOLUME             = 0x00080000
FILE_SEQUENTIAL_WRITE_ONCE        = 0x00100000
FILE_SUPPORTS_TRANSACTIONS        = 0x00200000
FILE_SUPPORTS_HARD_LINKS          = 0x00400000
FILE_SUPPORTS_EXTENDED_ATTRIBUTES = 0x00800000
FILE_SUPPORTS_OPEN_BY_FILE_ID     = 0x01000000
FILE_SUPPORTS_USN_JOURNAL         = 0x02000000

# File Attributes
# @link: http://msdn.microsoft.com/en-us/library/gg258117(v=VS.85).aspx
FILE_ATTRIBUTE_MYFILE                = 0x00000000 # What's this?
FILE_ATTRIBUTE_READONLY            = 0x1
FILE_ATTRIBUTE_HIDDEN              = 0x2
FILE_ATTRIBUTE_SYSTEM              = 0x4
FILE_ATTRIBUTE_DIRECTORY           = 0x10
FILE_ATTRIBUTE_ARCHIVE             = 0x20
FILE_ATTRIBUTE_DEVICE              = 0x40
FILE_ATTRIBUTE_NORMAL              = 0x80
FILE_ATTRIBUTE_TEMPORARY           = 0x100
FILE_ATTRIBUTE_SPARSE_FILE         = 0x200
FILE_ATTRIBUTE_REPARSE_POINT       = 0x400
FILE_ATTRIBUTE_COMPRESSED          = 0x800
FILE_ATTRIBUTE_OFFLINE             = 0x1000
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x2000
FILE_ATTRIBUTE_ENCRYPTED           = 0x4000
FILE_ATTRIBUTE_VIRTUAL             = 0x10000

# File flags
# @link: http://msdn.microsoft.com/en-us/library/aa363858(v=VS.85).aspx
FILE_FLAG_POSIX_SEMANTICS    = 0x0100000
FILE_FLAG_OPEN_NO_RECALL     = 0x00100000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_BACKUP_SEMANTICS   = 0x02000000
FILE_FLAG_DELETE_ON_CLOSE    = 0x04000000
FILE_FLAG_SEQUENTIAL_SCAN    = 0x08000000
FILE_FLAG_RANDOM_ACCESS      = 0x10000000
FILE_FLAG_NO_BUFFERING       = 0x20000000
FILE_FLAG_OVERLAPPED         = 0x40000000
FILE_FLAG_WRITE_THROUGH      = 0x80000000
# @todo: And what about SECURITY_SQOS_PRESENT?

# Share mode
# @link: http://msdn.microsoft.com/en-us/library/aa363858(v=VS.85).aspx
FILE_SHARE_NULL   = 0x0
FILE_SHARE_READ   = 0x1
FILE_SHARE_WRITE  = 0x2
FILE_SHARE_DELETE = 0x4

# Access mode
# Generic access rights
# @link: http://msdn.microsoft.com/en-us/library/cc245520(v=PROT.10).aspx
GENERIC_ALL     = 0x10000000
GENERIC_EXECUTE = 0x20000000
GENERIC_WRITE   = 0x40000000
GENERIC_READ    = 0x80000000

# Standard access rights
# @link: http://msdn.microsoft.com/en-us/library/aa374892(v=VS.85).aspx
DELETE       = 0x00010000
READ_CONTROL = 0x00020000
WRITE_DAC    = 0x00040000
WRITE_OWNER  = 0x00080000
SYNCHRONIZE  = 0x00100000

STANDARD_RIGHTS_READ    = READ_CONTROL
STANDARD_RIGHTS_WRITE   = READ_CONTROL
STANDARD_RIGHTS_EXECUTE = READ_CONTROL

STANDARD_RIGHTS_ALL      = 0x001F0000
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SPECIFIC_RIGHTS_ALL      = 0x0000FFFF

# File specific access rights
# @link: http://msdn.microsoft.com/en-us/library/gg258116(v=VS.85).aspx
FILE_READ_DATA            = 0x1
FILE_LIST_DIRECTORY       = 0x1
FILE_ADD_FILE             = 0x2
FILE_WRITE_DATA           = 0x2
FILE_ADD_SUBDIRECTORY     = 0x4
FILE_APPEND_DATA          = 0x4
FILE_CREATE_PIPE_INSTANCE = 0x4
FILE_READ_EA              = 0x8
FILE_WRITE_EA             = 0x10
FILE_EXECUTE              = 0x20
FILE_TRAVERSE             = 0x20
FILE_DELETE_CHILD         = 0x40
FILE_READ_ATTRIBUTES      = 0x80
FILE_WRITE_ATTRIBUTES     = 0x100

# Generic access rights for files and directories
# @link: http://msdn.microsoft.com/en-us/library/aa364399(v=VS.85).aspx
FILE_GENERIC_EXECUTE = FILE_EXECUTE | \
                       FILE_READ_ATTRIBUTES | \
                       STANDARD_RIGHTS_EXECUTE | \
                       SYNCHRONIZE
                        
FILE_GENERIC_READ = FILE_READ_ATTRIBUTES | \
                    FILE_READ_DATA | \
                    FILE_READ_EA | \
                    STANDARD_RIGHTS_READ | \
                    SYNCHRONIZE

FILE_GENERIC_WRITE = FILE_APPEND_DATA | \
                     FILE_WRITE_ATTRIBUTES | \
                     FILE_WRITE_DATA | \
                     FILE_WRITE_EA | \
                     STANDARD_RIGHTS_WRITE | \
                     SYNCHRONIZE

# А это точно правильно? Не STANDARD_RIGHTS_ALL | SPECIFIC_RIGHTS_ALL? 
# Странный какой-то этот WinNT.h...
FILE_ALL_ACCESS = STANDARD_RIGHTS_REQUIRED | \
                  SYNCHRONIZE | \
                  0x1FF

# Creation disposition
# @link: http://msdn.microsoft.com/en-us/library/aa363858(v=VS.85).aspx
CREATE_NEW        = 1
CREATE_ALWAYS     = 2
OPEN_EXISTING     = 3
OPEN_ALWAYS       = 4
TRUNCATE_EXISTING = 5

#ERRORS
ERROR_SUCCESS                                                       = 0
ERROR_FILE_NOT_FOUND                                                = 2
ERROR_PATH_NOT_FOUND                                                = 3
ERROR_ACCESS_DENIED                                                 = 5
ERROR_INVALID_HANDLE                                                = 6
ERROR_FILE_EXISTS                                                   = 80
ERROR_ALREADY_ASSIGNED                                              = 85
ERROR_DIR_NOT_EMPTY                                                 = 145
ERROR_PATH_BUSY                                                     = 148
ERROR_ALREADY_EXISTS                                                = 183

# Security information
# @link: http://msdn.microsoft.com/en-us/library/windows/desktop/aa446654(v=vs.85).aspx
OWNER_SECURITY_INFORMATION     = 0x1
GROUP_SECURITY_INFORMATION     = 0x2
DACL_SECURITY_INFORMATION      = 0x4
SACL_SECURITY_INFORMATION      = 0x8
LABEL_SECURITY_INFORMATION     = 0x10
ATTRIBUTE_SECURITY_INFORMATION = 0x20
SCOPE_SECURITY_INFORMATION     = 0x40
