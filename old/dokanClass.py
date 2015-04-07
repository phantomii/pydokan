from dokanHeader import *
from ctypes import *
# DOKANAPI CLASS

class DokanAPI():
	
	def __init__(self, DriverLetterOrMountPoint, DriverOption):
		self.DriverLerrerOrMountPoint = DriverLetterOrMountPoint
		self.DriverOption = DriverOption
		self.DokanDLL = windll.dokan
	
	def DokanMain(self, DokanOptions, DokanOperations):
		return int(self.DokanDLL.DokanMain(
			PDOKAN_OPTIONS(DokanOptions), 
			PDOKAN_OPERATIONS(DokanOperations)
		))
	
	def DokanUnmount(self, DriveLetter):
		return bool(self.DokanDLL.DokanUnmount(
			WCHAR(DriveLetter)
		))
		
	# DokanIsNameInExpression
	#   check whether Name can match Expression
	#   Expression can contain wildcard characters (? and *)
	def DokanIsNameInExpression(self, Expression, Name, IgnoreCase):
		return bool(self.DokanDLL.DokanIsNameInExpression(
			LPCWSTR(Expression),				# matching pattern
			LPCWSTR(Name),						# file name
			BOOL(IgnoreCase)
		))
	
	def DokanVersion(self):
		return long(self.DokanDLL.DokanVersion())
		
	def DokanDriverVersion(self):
		return long(self.DokanDLL.DokanDriverVersion())
	
	# DokanResetTimeout
	# extends the time out of the current IO operation in driver.
	def DokanResetTimeout(self, Timeout, DokanFileInfo):
		return bool(self.DokanDLL.DokanResetTimeout(
			ULONG(Timeout),						# timeout in millisecond
			PDOKAN_FILE_INFO(DokanFileInfo)
		))
	
	# Get the handle to Access Token
	# This method needs be called in CreateFile, OpenDirectory or CreateDirectly callback.
	# The caller must call CloseHandle for the returned handle.
	def DokanOpenRequestorToken(self, DokanFileInfo):
		return HANDLE(self.DokanDLL.DokanOpenRequestorToken(
			PDOKAN_FILE_INFO(DokanFileInfo)
		))
		
	
	# int (DOKAN_CALLBACK *CreateFile) (LPCWSTR, DWORD, DWORD, DWORD, DWORD, HANDLE, PDOKAN_FILE_INFO);
	#def CreateFile(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, TemplateFile, DokanFileInfo):
	# int (DOKAN_CALLBACK *CreateFile) (LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO);
	def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, DokanFileInfo):
		print "********** CreateFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *OpenDirectory) (LPCWSTR,	PDOKAN_FILE_INFO);
	def OpenDirectoryFunc(self, FileName, DokanFileInfo):
		print "********** OpenDirectoryFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *CreateDirectory) (LPCWSTR, PDOKAN_FILE_INFO);
	def CreateDirectoryFunc(self, FileName, DokanFileInfo):
		print "********** CreateDirectoryFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *Cleanup) (LPCWSTR, PDOKAN_FILE_INFO);
	def CleanupFunc(self, FileName, DokanFileInfo):
		print "********** CleanupFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *CloseFile) (LPCWSTR, PDOKAN_FILE_INFO);
	def CloseFileFunc(self, FileName, DokanFileInfo):
		print "********** CloseFileFunc **********"
		return 0
		
	# int (DOKAN_CALLBACK *ReadFile) (LPCWSTR, LPVOID, DWORD,  LPDWORD, LONGLONG, PDOKAN_FILE_INFO);
	def ReadFileFunc(self, FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset, DokanFileInfo):
		print "********** ReadFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *WriteFile) (LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO);
	def WriteFileFunc(self, FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset, DokanFileInfo):
		print "********** WriteFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *FlushFileBuffers) (LPCWSTR, PDOKAN_FILE_INFO);
	def FlushFileBuffersFunc(self, FileName, DokanFileInfo):
		print "********** FlushFileBuffersFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *GetFileInformation) (LPCWSTR,  LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO);
	def GetFileInformationFunc(self, FileName, Buffer, DokanFileInfo):
		print "********** GetFileInformationFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *FindFiles) (LPCWSTR,	PFillFindData, PDOKAN_FILE_INFO);
	def FindFilesFunc(self, FileName, FillFindData, DokanFileInfo):
		print "********** FindFilesFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *FindFilesWithPattern) (LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO);
	def FindFilesWithPatternFunc(self, FileName, SearchPattern, FillFindData, DokanFileInfo):
		print "********** FindFilesWithPatternFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *SetFileAttributes) (LPCWSTR, DWORD, PDOKAN_FILE_INFO);
	def SetFileAttributesFunc(self, FileName, FileAttributes, DokanFileInfo):
		print "********** SetFileAttributesFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *SetFileTime) (LPCWSTR, CONST FILETIME*, CONST FILETIME*, CONST FILETIME*, PDOKAN_FILE_INFO);
	def SetFileTimeFunc(self, FileName, CreationTime, LastAccessTime, LastWriteTime, DokanFileInfo):
		print "********** SetFileTimeFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *DeleteFile) (LPCWSTR, PDOKAN_FILE_INFO);
	def DeleteFileFunc(self, FileName, DokanFileName):
		print "********** DeleteFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *DeleteDirectory) (LPCWSTR, PDOKAN_FILE_INFO);
	def DeleteDirectoryFunc(self, FileName, DokanFileInfo):
		print "********** DeleteDirectoryFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *MoveFile) (LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO);
	def MoveFileFunc(self, ExistingFileName, NewFileName, ReplaceExisiting, DokanFileInfo):
		print "********** MoveFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *SetEndOfFile) (LPCWSTR, LONGLONG, PDOKAN_FILE_INFO);
	def SetEndOfFileFunc(self, FileName, Length, DokanFileInfo):
		print "********** SetEndOfFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *SetAllocationSize) (LPCWSTR, LONGLONG, PDOKAN_FILE_INFO);
	def SetAllocationSizeFunc(self, FileName, Length, DokanFileInfo):
		print "********** SetAllocationSizeFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *LockFile) (LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO);
	def LockFileFunc(self, FileName, ByteOffset, Length, DokanFileInfo):
		print "********** LockFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *UnlockFile) (LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO);
	def UnlockFileFunc(self, FileName, ByteOffset, Length, DokanFileInfo):
		print "********** UnlockFileFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *GetFileSecurity) (LPCWSTR, PSECURITY_INFORMATION, PSECURITY_DESCRIPTOR, ULONG, PULONG, PDOKAN_FILE_INFO);
	def GetFileSecurityFunc(self, FileName, SecurityInformation, SecurityDescriptor, LengthSecurityDescrptorBuffer, LengthNeeded, DokanFileInfo):
		print "********** GetFileSecurityFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *SetFileSecurity) (LPCWSTR, PSECURITY_INFORMATION, PSECURITY_DESCRIPTOR, ULONG, PDOKAN_FILE_INFO);
	def SetFileSecurityFunc(self, FileName, SecurityInformation, SecurityDescriptor, LengthSecurityDescrptorBuffer, DokanFileInfo):
		print "********** SetFileSecurityFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *GetDiskFreeSpace) (PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO);
	def GetDiskFreeSpaceFunc(self, FreeBytesAvailable, TotalNumberOfBytes, TotalNumberOfFreeBytes, DokanFileInfo):
		print "********** GetDiskFreeSpaceFunc **********"
		return 0
	
	# int (DOKAN_CALLBACK *GetVolumeInformation) (LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO);
	def GetVolumeInformationFunc(self, VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, DokanFileInfo):
		print "********** GetVolumeInformationFunc **********"
		return 0
		
	# int (DOKAN_CALLBACK *Unmount) (PDOKAN_FILE_INFO);
	def UnmountFunc(self, DokanFileInfo):
		print "********** UnmountFunc **********"
		return 0
		
	def main(self):
		Operations = _DOKAN_OPERATIONS(
			CreateFileFuncType(self.CreateFileFunc),
			OpenDirectoryFuncType(self.OpenDirectoryFunc),
			CreateDirectoryFuncType(self.CreateDirectoryFunc),
			CleanupFuncType(self.CleanupFunc),
			CloseFileFuncType(self.CloseFileFunc),
			ReadFileFuncType(self.ReadFileFunc),
			WriteFileFuncType(self.WriteFileFunc),
			FlushFileBuffersFuncType(self.FlushFileBuffersFunc),
			GetFileInformationFuncType(self.GetFileInformationFunc),
			FindFilesFuncType(self.FindFilesFunc),
			FindFilesWithPatternFuncType(self.FindFilesWithPatternFunc),
			SetFileAttributesFuncType(self.SetFileAttributesFunc),
			SetFileTimeFuncType(self.SetFileTimeFunc),
			DeleteFileFuncType(self.DeleteFileFunc),
			DeleteDirectoryFuncType(self.DeleteDirectoryFunc),
			MoveFileFuncType(self.MoveFileFunc),
			SetEndOfFileFuncType(self.SetEndOfFileFunc),
			SetAllocationSizeFuncType(self.SetAllocationSizeFunc),
			LockFileFuncType(self.LockFileFunc),
			UnlockFileFuncType(self.UnlockFileFunc),
			GetFileSecurityFuncType(self.GetFileSecurityFunc),
			SetFileSecurityFuncType(self.SetFileSecurityFunc),
			GetDiskFreeSpaceFuncType(self.GetDiskFreeSpaceFunc),
			GetVolumeInformationFuncType(self.GetVolumeInformationFunc),
			UnmountFuncType(self.UnmountFunc)
		)
		Options = _DOKAN_OPTIONS(
			self.DriverLerrerOrMountPoint,			# mount point "M:\" (drive letter) or "C:\mount\dokan" (path in NTFS)
			1,										# number of threads to be used
			self.DriverOption,						# combination of DOKAN_OPTIONS_*
			0										# FileSystem can use this variable
		)
		self.DokanMain(Options, Operations)

