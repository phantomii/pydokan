# pyDokan : Dokan for python
#
# Copyright (C) 2010 Eugene Frolov profisphantom@gmail.com
# S.Y.N.A.P.S.E Technology http://pydokan.synapse.net.ru
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#     
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

#
# Dokan : user-mode file system library for Windows
#
# Copyright (C) 2008 Hiroki Asakawa info@dokan-dev.net
#
# http://dokan-dev.net/en
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
#

from ctypes import *

# PYTHON CONSTANT FOR CTYPE
WSTRING = c_wchar_p


WCHAR 							=	c_wchar					
PWCHAR 							= 	WSTRING
USHORT 							= 	c_ushort
ULONG64 						= 	c_ulonglong
PULONGLONG 						= 	c_void_p			# POINTER(ULONG64)
PUCHAR 							= 	POINTER(c_ubyte)
UCHAR 							= 	c_ubyte
BOOL 							= 	c_int
PBOOL 							= 	POINTER(c_int)
LPBOOL							= 	POINTER(c_int)
PULONG 							= 	POINTER(c_ulong)
ULONG 							= 	c_ulong
PDWORD 							= 	POINTER(c_ulong)
DWORD 							= 	c_ulong
LPDWORD 						= 	POINTER(c_ulong)
LPCWSTR 						= 	WSTRING
LPWSTR 							= 	c_void_p			# WSTRING
PWSTR 							= 	WSTRING
LPVOID							= 	c_void_p
LPCVOID 						= 	c_void_p
INT64 							= 	c_longlong
LONGLONG 						= 	INT64
PSECURITY_INFORMATION			=	POINTER(c_ulong)
PSECURITY_DESCRIPTOR			=	c_void_p
HANDLE							=	c_ulong

# FILETIME Start structure
class _FILETIME(Structure):
	pass
	
_FILETIME._fields_ 				= [
	('dwLowDateTime', 			DWORD),
	('dwHighDateTime', 			DWORD),
]

PFILETIME 						= 	POINTER(_FILETIME)
FILETIME 						= 	_FILETIME
# FILETIME End structure

# BY_HANDLE_FILE_INFORMATION Start structure
class _BY_HANDLE_FILE_INFORMATION(Structure):
    pass
    
_BY_HANDLE_FILE_INFORMATION._fields_ = [
    ('dwFileAttributes', 		DWORD),
    ('ftCreationTime', 			FILETIME),
    ('ftLastAccessTime', 		FILETIME),
    ('ftLastWriteTime', 		FILETIME),
    ('dwVolumeSerialNumber',	DWORD),
    ('nFileSizeHigh', 			DWORD),
    ('nFileSizeLow', 			DWORD),
    ('nNumberOfLinks', 			DWORD),
    ('nFileIndexHigh', 			DWORD),
    ('nFileIndexLow', 			DWORD),
]

LPBY_HANDLE_FILE_INFORMATION 	= 	c_void_p	#POINTER(_BY_HANDLE_FILE_INFORMATION)
BY_HANDLE_FILE_INFORMATION 		= 	_BY_HANDLE_FILE_INFORMATION
# BY_HANDLE_FILE_INFORMATION End structure

# WIN32_FIND_DATAW Start structure
class _WIN32_FIND_DATAW(Structure):
    pass
    
_WIN32_FIND_DATAW._fields_ 		= 	[
    ('dwFileAttributes', 		DWORD),
    ('ftCreationTime', 			FILETIME),
    ('ftLastAccessTime', 		FILETIME),
    ('ftLastWriteTime', 		FILETIME),
    ('nFileSizeHigh', 			DWORD),
    ('nFileSizeLow', 			DWORD),
    ('dwReserved0', 			DWORD),
    ('dwReserved1', 			DWORD),
    ('cFileName', 				WCHAR * 260),
    ('cAlternateFileName', 		WCHAR * 14),
	#('extra', WCHAR * 4),
]
PWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)
WIN32_FIND_DATAW = _WIN32_FIND_DATAW
LPWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)
# WIN32_FIND_DATAW End structure


# DOKAN CONVERT START
DOKAN_DRIVER_NAME				=	"dokan.sys"

DOKAN_OPTION_DEBUG				=	1  # ouput debug message
DOKAN_OPTION_STDERR				=	2  # ouput debug message to stderr
DOKAN_OPTION_ALT_STREAM			=	4  # use alternate stream
DOKAN_OPTION_KEEP_ALIVE			=	8  # use auto unmount
DOKAN_OPTION_NETWORK			=	16 # use network drive
DOKAN_OPTION_REMOVABLE			=	32 # use removable drive

# DOKAN_OPTIONS Start structure
class _DOKAN_OPTIONS(Structure):
    pass

_DOKAN_OPTIONS._pack_ 			=	4
_DOKAN_OPTIONS._fields_ 		= 	[
	('MountPoint',				LPCWSTR),	# mount point "M:\" (drive letter) or "C:\mount\dokan" (path in NTFS)
	('ThreadCount',				USHORT),	# number of threads to be used
	('Options',					ULONG),		# combination of DOKAN_OPTIONS_*
	('GlobalContext',			ULONG64),	# FileSystem can use this variable
]
DOKAN_OPTIONS					= 	_DOKAN_OPTIONS
PDOKAN_OPTIONS					= 	POINTER(_DOKAN_OPTIONS)
# DOKAN_OPTIONS End structure

# DOKAN_FILE_INFO Start structure
class _DOKAN_FILE_INFO(Structure):
	pass

_DOKAN_FILE_INFO._pack_			=	4
_DOKAN_FILE_INFO._fields_		=	[
	('Context',					ULONG64),		# FileSystem can use this variable
	('DokanContext',			ULONG64),		# Don't touch this
	('DokanOptions',			PDOKAN_OPTIONS),# A pointer to DOKAN_OPTIONS which was  passed to DokanMain.
	('ProcessId',				ULONG),			# process id for the thread that originally requested a given I/O operation
	('IsDirectory',				UCHAR),			# requesting a directory file
	('DeleteOnClose',			UCHAR),			# Delete on when "cleanup" is called
	('PagingIo',				UCHAR),			# Read or write is paging IO.
	('SynchronousIo',			UCHAR),			# Read or write is synchronous IO.
	('Nocache',					UCHAR),			# No use cache
	('WriteToEndOfFile',		UCHAR),			# If true, write to the current end of file instead of Offset parameter.
]
DOKAN_FILE_INFO					=	_DOKAN_FILE_INFO
PDOKAN_FILE_INFO				=	POINTER(_DOKAN_FILE_INFO)
# DOKAN_FILE_INFO End structure

# FillFileData
#   add an entry in FindFiles
#   return 1 if buffer is full, otherwise 0
#   (currently never return 1)
PFillFindData					=	WINFUNCTYPE(
	c_int,
	PWIN32_FIND_DATAW,
	PDOKAN_FILE_INFO
)
#def PFillFindData(self, Win32FindDataW, DokanFileIndo):
#	return self._dll.PFillFindData(WIN32_FIND_DATAW(Win32FindDataW), PDOKAN_FILE_INFO(DokanFileIndo))

# FuncDef
CreateFileFuncType				= 	WINFUNCTYPE(
	c_int,
	LPCWSTR,						# FileName
	DWORD,							# DesiredAccess
	DWORD,							# ShareMode
	DWORD,							# CreationDisposition
	DWORD,							# FlagsAndAttributes
	#HANDLE,						# TemplateFile
	PDOKAN_FILE_INFO
)
OpenDirectoryFuncType			=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PDOKAN_FILE_INFO
)
CreateDirectoryFuncType			=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PDOKAN_FILE_INFO
)
# When FileInfo->DeleteOnClose is true, you must delete the file in Cleanup.
CleanupFuncType					=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PDOKAN_FILE_INFO
)
CloseFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PDOKAN_FILE_INFO
)
ReadFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	LPCVOID,							# Buffer
	DWORD,								# NumberOfBytesToWrite
	LPDWORD,							# NumberOfBytesWritten
	#c_void_p,							# NumberOfBytesWritten
	LONGLONG,							# Offset
	PDOKAN_FILE_INFO
)
WriteFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,  							# FileName
	LPCVOID,  							# Buffer
	DWORD,    							# NumberOfBytesToWrite
	LPDWORD,  							# NumberOfBytesWritten
	LONGLONG, 							# Offset
	PDOKAN_FILE_INFO
)
FlushFileBuffersFuncType		=	WINFUNCTYPE(
	c_int,
	LPCWSTR, 							# FileName
	PDOKAN_FILE_INFO
)
GetFileInformationFuncType		=	WINFUNCTYPE(
	c_int,
	LPCWSTR,          					# FileName
	LPBY_HANDLE_FILE_INFORMATION, 		# Buffer
	PDOKAN_FILE_INFO
)
FindFilesFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PFillFindData,						# call this function with PWIN32_FIND_DATAW
										# (see PFillFindData definition)
	PDOKAN_FILE_INFO
)
# You should implement either FindFiles or FindFilesWithPattern
FindFilesWithPatternFuncType	=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	LPCWSTR,							# SearchPattern
	PFillFindData,						# call this function with PWIN32_FIND_DATAW
	PDOKAN_FILE_INFO
)
SetFileAttributesFuncType		=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	DWORD,								# FileAttributes
	PDOKAN_FILE_INFO
)
SetFileTimeFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	POINTER(FILETIME),					# CreationTime
	POINTER(FILETIME),					# LastAccessTime
	POINTER(FILETIME),					# LastWriteTime
	PDOKAN_FILE_INFO
)
# You should not delete file on DeleteFile or DeleteDirectory.
# When DeleteFile or DeleteDirectory, you must check whether
# you can delete or not, and return 0 (when you can delete it)
# or appropriate error codes such as -ERROR_DIR_NOT_EMPTY,
# -ERROR_SHARING_VIOLATION.
# When you return 0 (ERROR_SUCCESS), you get Cleanup with
# FileInfo->DeleteOnClose set TRUE, you delete the file.
DeleteFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PDOKAN_FILE_INFO
)
DeleteDirectoryFuncType			=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PDOKAN_FILE_INFO
)
MoveFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# ExistingFileName
	LPCWSTR,							# NewFileName
	BOOL,								# ReplaceExisiting
	PDOKAN_FILE_INFO
)
SetEndOfFileFuncType			=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	LONGLONG,							# Length
	PDOKAN_FILE_INFO
)
SetAllocationSizeFuncType		=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	LONGLONG,							# Length
	PDOKAN_FILE_INFO
)
LockFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	LONGLONG,							# ByteOffset
	LONGLONG,							# Length
	PDOKAN_FILE_INFO
)
UnlockFileFuncType				=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	LONGLONG,							# ByteOffset
	LONGLONG,							# Length
	PDOKAN_FILE_INFO
)
GetFileSecurityFuncType			=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PSECURITY_INFORMATION,				# A pointer to SECURITY_INFORMATION value being requested
	PSECURITY_DESCRIPTOR,				# A pointer to SECURITY_DESCRIPTOR buffer to be filled
	ULONG,								# length of Security descriptor buffer
	PULONG,								# LengthNeeded
	PDOKAN_FILE_INFO
)

SetFileSecurityFuncType			=	WINFUNCTYPE(
	c_int,
	LPCWSTR,							# FileName
	PSECURITY_INFORMATION,
	PSECURITY_DESCRIPTOR,				# SecurityDescriptor
	ULONG,								# SecurityDescriptor length
	PDOKAN_FILE_INFO
)

# Neither GetDiskFreeSpace nor GetVolumeInformation
# save the DokanFileContext->Context.
# Before these methods are called, CreateFile may not be called.
# (ditto CloseFile and Cleanup)

# see Win32 API GetDiskFreeSpaceEx
GetDiskFreeSpaceFuncType		=	WINFUNCTYPE(
	c_int,
	PULONGLONG,							# FreeBytesAvailable
	PULONGLONG,							# TotalNumberOfBytes
	PULONGLONG,							# TotalNumberOfFreeBytes
	PDOKAN_FILE_INFO
)
# see Win32 API GetVolumeInformation
GetVolumeInformationFuncType	=	WINFUNCTYPE(
	c_int,
	LPWSTR,								# VolumeNameBuffer
	DWORD,								# VolumeNameSize in num of chars
	LPDWORD,							# VolumeSerialNumber
	LPDWORD,							# MaximumComponentLength in num of chars
	LPDWORD,							# FileSystemFlags
	LPWSTR,								# FileSystemNameBuffer
	DWORD,								# FileSystemNameSize in num of chars
	PDOKAN_FILE_INFO
)
UnmountFuncType					=	WINFUNCTYPE(
	c_int,
	PDOKAN_FILE_INFO
)
# FuncDef

# _DOKAN_OPERATIONS Start structure
class _DOKAN_OPERATIONS(Structure):
	"""
	When an error occurs, return negative value.
	Usually you should return GetLastError() * -1.

	CreateFile
	  If file is a directory, CreateFile (not OpenDirectory) may be called.
	  In this case, CreateFile should return 0 when that directory can be opened.
	  You should set TRUE on DokanFileInfo->IsDirectory when file is a directory.
	  When CreationDisposition is CREATE_ALWAYS or OPEN_ALWAYS and a file already exists,
	  you should return ERROR_ALREADY_EXISTS(183) (not negative value)
	"""
	pass
	
_DOKAN_OPERATIONS._pack_		=	4
_DOKAN_OPERATIONS._fields_		=	[
	('CreateFile',				CreateFileFuncType),	
	('OpenDirectory',			OpenDirectoryFuncType),
	('CreateDirectory',			CreateDirectoryFuncType),
	('Cleanup',					CleanupFuncType),
	('CloseFile',				CloseFileFuncType),
	('ReadFile',				ReadFileFuncType),
	('WriteFile',				WriteFileFuncType),
	('FlushFileBuffers',		FlushFileBuffersFuncType),
	('GetFileInformation',		GetFileInformationFuncType),
	('FindFiles',				FindFilesFuncType),
	('FindFilesWithPattern',	FindFilesWithPatternFuncType),
	('SetFileAttributes',		SetFileAttributesFuncType),
	('SetFileTime',				SetFileTimeFuncType),
	('DeleteFile',				DeleteFileFuncType),
	('DeleteDirectory',			DeleteDirectoryFuncType),
	('MoveFile',				MoveFileFuncType),
	('SetEndOfFile',			SetEndOfFileFuncType),
	('SetAllocationSize',		SetAllocationSizeFuncType),
	('LockFile',				LockFileFuncType),
	('UnlockFile',				UnlockFileFuncType),
	('GetFileSecurity',			GetFileSecurityFuncType),
	('SetFileSecurity',			SetFileSecurityFuncType),
	('GetDiskFreeSpace',		GetDiskFreeSpaceFuncType),
	('GetVolumeInformation',	GetVolumeInformationFuncType),
	('Unmount',					UnmountFuncType),
]

DOKAN_OPERATIONS 				= 	_DOKAN_OPERATIONS
PDOKAN_OPERATIONS				=	POINTER(_DOKAN_OPERATIONS)
# _DOKAN_OPERATIONS End structure

# DokanMain returns error codes
DOKAN_SUCCESS					=	0
DOKAN_ERROR						=	-1 		# General Error
DOKAN_DRIVE_LETTER_ERROR		=	-2		# Bad Drive letter
DOKAN_DRIVER_INSTALL_ERROR		=	-3 		# Can't install driver
DOKAN_START_ERROR				=	-4 		# Driver something wrong
DOKAN_MOUNT_ERROR				=	-5 		# Can't assign a drive letter
DOKAN_MOUNT_POINT_ERROR			=	-6		# Mount point is invalid

# The public names defined by a module are determined by 
# checking the module's namespace for a variable named __all__
__all__ 						= 	[
	'LONGLONG', 'LPWIN32_FIND_DATAW', '_BY_HANDLE_FILE_INFORMATION', 
	'PFillFindData', 'PDWORD', 'FILETIME', 'PWIN32_FIND_DATAW', 
	'DOKAN_FILE_INFO', 'PULONGLONG', 'DWORD', 'LPBOOL', '_FILETIME', 
	'_WIN32_FIND_DATAW', 'LPBY_HANDLE_FILE_INFORMATION', 'ULONG', 
	'PWCHAR', '_DOKAN_FILE_INFO', 'ULONG64', 'BY_HANDLE_FILE_INFORMATION', 
	'_DOKAN_OPERATIONS', 'PUCHAR', 'PFILETIME', 'PDOKAN_OPTIONS', 
	'WIN32_FIND_DATAW', 'PBOOL', 'UCHAR', 'LPCVOID', 'LPCWSTR', 
	'PDOKAN_OPERATIONS', 'DOKAN_OPTIONS', 'LPWSTR', 'INT64', 
	'PDOKAN_FILE_INFO', 'PWSTR', 'DOKAN_OPERATIONS', 'USHORT', 'LPVOID', 
	'LPDWORD', 'BOOL', 'PULONG', 'WCHAR', '_DOKAN_OPTIONS', 
	'PSECURITY_DESCRIPTOR', 'PSECURITY_INFORMATION', 'DOKAN_OPTION_DEBUG',
	'DOKAN_OPTION_STDERR', 'DOKAN_OPTION_ALT_STREAM', 'DOKAN_OPTION_KEEP_ALIVE',
	'DOKAN_OPTION_NETWORK', 'DOKAN_OPTION_REMOVABLE', 'CreateFileFuncType',
	'OpenDirectoryFuncType', 'CreateDirectoryFuncType', 'CleanupFuncType',
	'CloseFileFuncType', 'ReadFileFuncType', 'WriteFileFuncType',
	'FlushFileBuffersFuncType', 'GetFileInformationFuncType',
	'FindFilesFuncType', 'FindFilesWithPatternFuncType', 
	'SetFileAttributesFuncType', 'SetFileTimeFuncType', 'DeleteFileFuncType',
	'DeleteDirectoryFuncType', 'MoveFileFuncType', 'SetEndOfFileFuncType',
	'SetAllocationSizeFuncType', 'LockFileFuncType', 'UnlockFileFuncType',
	'GetFileSecurityFuncType', 'SetFileSecurityFuncType', 
	'GetDiskFreeSpaceFuncType', 'GetVolumeInformationFuncType', 'UnmountFuncType'
]
