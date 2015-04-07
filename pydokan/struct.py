# coding=utf8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

"""Структуры которыми пользуется драйвер dokan

"""

__version__ = '0.1.0'
__author__  = "Eugene Frolov"
__mail__    = "profisphantom@gmail.com"

from ctypes import *
from sys import platform

if platform != 'win32':
    
    # Переопределение WINFUNCTYPE, для избавления от ошибки в операционных 
    # системах отличных от виндовс
    WINFUNCTYPE = CFUNCTYPE


# PYTHON CONSTANT FOR CTYPE
WSTRING                             =   c_wchar_p
WCHAR                               =   c_wchar
PWCHAR                              =   WSTRING
USHORT                              =   c_ushort
ULONG64                             =   c_ulonglong
PULONGLONG                          =   POINTER(ULONG64)
PUCHAR                              =   POINTER(c_ubyte)
UCHAR                               =   c_ubyte
BOOL                                =   c_int
PBOOL                               =   POINTER(c_int)
LPBOOL                              =   POINTER(c_int)
PULONG                              =   POINTER(c_ulong)
ULONG                               =   c_ulong
PDWORD                              =   POINTER(c_ulong)
DWORD                               =   c_ulong
LPDWORD                             =   POINTER(c_ulong)
LPCWSTR                             =   WSTRING
LPWSTR                              =   WSTRING
LPSTR                               =   c_char_p
PWSTR                               =   WSTRING
LPVOID                              =   c_void_p
LPCVOID                             =   c_void_p
INT64                               =   c_longlong
LONGLONG                            =   INT64
PSECURITY_INFORMATION               =   POINTER(c_ulong)
PSECURITY_DESCRIPTOR                =   c_void_p
HANDLE                              =   c_ulong


DOKAN_DRIVER_NAME                   =   "dokan.sys"

# Dokan Options
DOKAN_OPTION_DEBUG                  =   1   # ouput debug message
DOKAN_OPTION_STDERR                 =   2   # ouput debug message to stderr
DOKAN_OPTION_ALT_STREAM             =   4   # use alternate stream
DOKAN_OPTION_KEEP_ALIVE             =   8   # use auto unmount
DOKAN_OPTION_NETWORK                =   16  # use network drive, you need to 
                                            # install Dokan network provider.
DOKAN_OPTION_REMOVABLE              =   32  # use removable drive

DOKAN_VERSION                       =   600 # Dokan version

# DokanMain returns error codes
DOKAN_SUCCESS                       =   0
DOKAN_ERROR                         =   -1  # General Error
DOKAN_DRIVE_LETTER_ERROR            =   -2  # Bad Drive letter
DOKAN_DRIVER_INSTALL_ERROR          =   -3  # Can't install driver
DOKAN_START_ERROR                   =   -4  # Driver something wrong
DOKAN_MOUNT_ERROR                   =   -5  # Can't assign a drive letter
DOKAN_MOUNT_POINT_ERROR             =   -6  # Mount point is invalid


# Windows structure
# FILETIME Start structure
class FILETIME(Structure):
    pass
    
FILETIME._fields_                   =   [
    ('dwLowDateTime',                   DWORD),
    ('dwHighDateTime',                  DWORD),
]

PFILETIME                           =   POINTER(FILETIME)


# BY_HANDLE_FILE_INFORMATION Start structure
class BY_HANDLE_FILE_INFORMATION(Structure):
    pass
    
BY_HANDLE_FILE_INFORMATION._fields_ =   [
    ('dwFileAttributes',                DWORD),
    ('ftCreationTime',                  FILETIME),
    ('ftLastAccessTime',                FILETIME),
    ('ftLastWriteTime',                 FILETIME),
    ('dwVolumeSerialNumber',            DWORD),
    ('nFileSizeHigh',                   DWORD),
    ('nFileSizeLow',                    DWORD),
    ('nNumberOfLinks',                  DWORD),
    ('nFileIndexHigh',                  DWORD),
    ('nFileIndexLow',                   DWORD),
]

LPBY_HANDLE_FILE_INFORMATION        =   POINTER(BY_HANDLE_FILE_INFORMATION)


# WIN32_FIND_DATAW Start structure
class WIN32_FIND_DATAW(Structure):
    pass
    
WIN32_FIND_DATAW._fields_           =   [
    ('dwFileAttributes',                DWORD),
    ('ftCreationTime',                  FILETIME),
    ('ftLastAccessTime',                FILETIME),
    ('ftLastWriteTime',                 FILETIME),
    ('nFileSizeHigh',                   DWORD),
    ('nFileSizeLow',                    DWORD),
    ('dwReserved0',                     DWORD),
    ('dwReserved1',                     DWORD),
    ('cFileName',                       WCHAR * 260),
    ('cAlternateFileName',              WCHAR * 14),
]
PWIN32_FIND_DATAW                   =   POINTER(WIN32_FIND_DATAW)
LPWIN32_FIND_DATAW                  =   POINTER(WIN32_FIND_DATAW)


# Dokan structure
# DOKAN_OPTIONS Start structure
class DOKAN_OPTIONS(Structure):
    pass

DOKAN_OPTIONS._pack_                =   4
DOKAN_OPTIONS._fields_              =   [
    ('Version',                         USHORT), # Supported Dokan Version, ex.
                                                 # "530" (Dokan ver 0.5.3)
    ('ThreadCount',                     USHORT), # number of threads to be used
    ('Options',                         ULONG),  # combination of DOKAN_OPTIONS_*
    ('GlobalContext',                   ULONG64),# FileSystem can use this variable
    ('MountPoint',                      LPCWSTR),# mount point "M:\" (drive letter)
                                                 # or "C:\mount\dokan" (path in NTFS)
]

PDOKAN_OPTIONS                      =   POINTER(DOKAN_OPTIONS)


# DOKAN_FILE_INFO Start structure
class DOKAN_FILE_INFO(Structure):
    pass

DOKAN_FILE_INFO._pack_              =   4
DOKAN_FILE_INFO._fields_            =   [
    ('Context',                         ULONG64), # FileSystem can use this variable
    ('DokanContext',                    ULONG64), # Don't touch this
    ('DokanOptions',                    PDOKAN_OPTIONS),# A pointer to DOKAN_OPTIONS
                                                  # which was  passed to DokanMain.
    ('ProcessId',                       ULONG),   # process id for the thread that 
                                                  # originally requested a given I/O 
                                                  # operation
    ('IsDirectory',                     UCHAR),   # requesting a directory file
    ('DeleteOnClose',                   UCHAR),   # Delete on when "cleanup" is called
    ('PagingIo',                        UCHAR),   # Read or write is paging IO.
    ('SynchronousIo',                   UCHAR),   # Read or write is synchronous IO.
    ('Nocache',                         UCHAR),   # No use cache
    ('WriteToEndOfFile',                UCHAR),   # If true, write to the current 
                                                  # end of file instead of Offset 
                                                  # parameter.
]

PDOKAN_FILE_INFO                    =   POINTER(DOKAN_FILE_INFO)


# Function define
# FillFileData
#   add an entry in FindFiles
#   return 1 if buffer is full, otherwise 0
#   (currently never return 1)
PFillFindData                       =    WINFUNCTYPE(
    c_int,
    PWIN32_FIND_DATAW,
    PDOKAN_FILE_INFO
)


CreateFileFuncType                  =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    DWORD,                              # DesiredAccess
    DWORD,                              # ShareMode
    DWORD,                              # CreationDisposition
    DWORD,                              # FlagsAndAttributes
    PDOKAN_FILE_INFO
)


OpenDirectoryFuncType               =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                           # FileName
    PDOKAN_FILE_INFO
)


CreateDirectoryFuncType             =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                           # FileName
    PDOKAN_FILE_INFO
)


CleanupFuncType                     =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PDOKAN_FILE_INFO
)


CloseFileFuncType                   =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PDOKAN_FILE_INFO
)


ReadFileFuncType                    =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LPCVOID,                            # Buffer
    DWORD,                              # NumberOfBytesToWrite
    LPDWORD,                            # NumberOfBytesWritten
    LONGLONG,                           # Offset
    PDOKAN_FILE_INFO
)


WriteFileFuncType                   =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LPCVOID,                            # Buffer
#    LPSTR,                              # Buffer
    DWORD,                              # NumberOfBytesToWrite
    LPDWORD,                            # NumberOfBytesWritten
    LONGLONG,                           # Offset
    PDOKAN_FILE_INFO
)


FlushFileBuffersFuncType            =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PDOKAN_FILE_INFO
)


GetFileInformationFuncType          =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LPBY_HANDLE_FILE_INFORMATION,       # Buffer
    PDOKAN_FILE_INFO
)


FindFilesFuncType                   =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PFillFindData,                      # call this function with PWIN32_FIND_DATAW
                                        # (see PFillFindData definition)
    PDOKAN_FILE_INFO
)


FindFilesWithPatternFuncType        =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LPCWSTR,                            # SearchPattern
    PFillFindData,                      # call this function with PWIN32_FIND_DATAW
    PDOKAN_FILE_INFO
)


SetFileAttributesFuncType           =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    DWORD,                              # FileAttributes
    PDOKAN_FILE_INFO
)


SetFileTimeFuncType                 =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    FILETIME,                           # CreationTime
    FILETIME,                           # LastAccessTime
    FILETIME,                           # LastWriteTime
    PDOKAN_FILE_INFO
)


DeleteFileFuncType                  =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PDOKAN_FILE_INFO
)


DeleteDirectoryFuncType             =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PDOKAN_FILE_INFO
)


MoveFileFuncType                    =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # ExistingFileName
    LPCWSTR,                            # NewFileName
    BOOL,                               # ReplaceExisiting
    PDOKAN_FILE_INFO
)


SetEndOfFileFuncType                =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LONGLONG,                           # Length
    PDOKAN_FILE_INFO
)


SetAllocationSizeFuncType           =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LONGLONG,                           # Length
    PDOKAN_FILE_INFO
)


LockFileFuncType                    =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LONGLONG,                           # ByteOffset
    LONGLONG,                           # Length
    PDOKAN_FILE_INFO
)


UnlockFileFuncType                  =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    LONGLONG,                           # ByteOffset
    LONGLONG,                           # Length
    PDOKAN_FILE_INFO
)


GetDiskFreeSpaceFuncType            =   WINFUNCTYPE(
    c_int,
    PULONGLONG,                         # FreeBytesAvailable
    PULONGLONG,                         # TotalNumberOfBytes
    PULONGLONG,                         # TotalNumberOfFreeBytes
    PDOKAN_FILE_INFO
)


GetVolumeInformationFuncType        =   WINFUNCTYPE(
    c_int,
    c_void_p,                           # VolumeNameBuffer
    DWORD,                              # VolumeNameSize in num of chars
    LPDWORD,                            # VolumeSerialNumber
    LPDWORD,                            # MaximumComponentLength in num of chars
    LPDWORD,                            # FileSystemFlags
    c_void_p,                           # FileSystemNameBuffer
    DWORD,                              # FileSystemNameSize in num of chars
    PDOKAN_FILE_INFO
)


UnmountFuncType                     =   WINFUNCTYPE(
    c_int,
    PDOKAN_FILE_INFO
)


GetFileSecurityFuncType             =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PSECURITY_INFORMATION,              # A pointer to SECURITY_INFORMATION value
                                        # being requested
    PSECURITY_DESCRIPTOR,               # A pointer to SECURITY_DESCRIPTOR buffer
                                        # to be filled
    ULONG,                              # length of Security descriptor buffer
    PULONG,                             # LengthNeeded
    PDOKAN_FILE_INFO
)


SetFileSecurityFuncType             =   WINFUNCTYPE(
    c_int,
    LPCWSTR,                            # FileName
    PSECURITY_INFORMATION,              # SecurityInformation
    PSECURITY_DESCRIPTOR,               # SecurityDescriptor
    ULONG,                              # SecurityDescriptor length
    PDOKAN_FILE_INFO
)


# _DOKAN_OPERATIONS Start structure
class DOKAN_OPERATIONS(Structure):
    pass
    
DOKAN_OPERATIONS._pack_             =   4
DOKAN_OPERATIONS._fields_           =   [
    ('CreateFile',                      CreateFileFuncType),    
    ('OpenDirectory',                   OpenDirectoryFuncType),
    ('CreateDirectory',                 CreateDirectoryFuncType),
    ('Cleanup',                         CleanupFuncType),
    ('CloseFile',                       CloseFileFuncType),
    ('ReadFile',                        ReadFileFuncType),
    ('WriteFile',                       WriteFileFuncType),
    ('FlushFileBuffers',                FlushFileBuffersFuncType),
    ('GetFileInformation',              GetFileInformationFuncType),
    ('FindFiles',                       FindFilesFuncType),
    ('FindFilesWithPattern',            FindFilesWithPatternFuncType),
    ('SetFileAttributes',               SetFileAttributesFuncType),
    ('SetFileTime',                     SetFileTimeFuncType),
    ('DeleteFile',                      DeleteFileFuncType),
    ('DeleteDirectory',                 DeleteDirectoryFuncType),
    ('MoveFile',                        MoveFileFuncType),
    ('SetEndOfFile',                    SetEndOfFileFuncType),
    ('SetAllocationSize',               SetAllocationSizeFuncType),
    ('LockFile',                        LockFileFuncType),
    ('UnlockFile',                      UnlockFileFuncType),
    ('GetDiskFreeSpace',                GetDiskFreeSpaceFuncType),
    ('GetVolumeInformation',            GetVolumeInformationFuncType),
    ('Unmount',                         UnmountFuncType),
    ('GetFileSecurity',                 GetFileSecurityFuncType),
    ('SetFileSecurity',                 SetFileSecurityFuncType),
]

PDOKAN_OPERATIONS                       =    POINTER(DOKAN_OPERATIONS)