#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dokanClass import *
from dokanHeader import *
import dokanMemTools
from dokanWin32Constants import *

class HelloFS(DokanAPI):
	
	HelloWorldText = 'Hello World!!!'
	HelloWorldName = '\\Hello_World.txt'
	first = True
	
	def __init__(self, DriverMountPoint, DriverOption, DriverSerialNumber):
		self.DriverSerialNumber = DriverSerialNumber
		DokanAPI.__init__(self, DriverMountPoint, DriverOption)
		
	def GetDiskFreeSpaceFunc(self, FreeBytesAvailable, TotalNumberOfBytes, TotalNumberOfFreeBytes, DokanFileInfo):
		_FreeByteAvailable = 0x100000000L - len(self.HelloWorldText)
		_TotalNumberOfBytes = 0x100000000L
		_TotalNumberOfFreeBytes = 0x100000000L - len(self.HelloWorldText)
		dokanMemTools.setLongLongByPoint(FreeBytesAvailable, _FreeByteAvailable)
		dokanMemTools.setLongLongByPoint(TotalNumberOfBytes, _TotalNumberOfBytes)
		dokanMemTools.setLongLongByPoint(TotalNumberOfFreeBytes, _TotalNumberOfFreeBytes)
		return 0
	
	def GetVolumeInformationFunc(self, VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, DokanFileInfo):
		_VolumeNameBuffer = u'Hello World Disk'
		VolumeNameSize = 2 * (len(_VolumeNameBuffer) + 1)
		dokanMemTools.setStringByPoint(VolumeNameBuffer, _VolumeNameBuffer, VolumeNameSize)
		VolumeSerialNumber = self.DriverSerialNumber
		MaximumComponentLength = 256 
		FileSystemFlags = FILE_CASE_SENSITIVE_SEARCH | \
			FILE_SUPPORTS_ENCRYPTION | FILE_UNICODE_ON_DISK | \
			FILE_CASE_PRESERVED_NAMES | FILE_SUPPORTS_REMOTE_STORAGE | \
			FILE_UNICODE_ON_DISK
			# FILE_SEQUENTIAL_WRITE_ONCE
		_FileSystemNameBuffer = u'Hello World File System'
		FileSystemNameSize = 2 * (len(_FileSystemNameBuffer) + 1)
		dokanMemTools.setStringByPoint(FileSystemNameBuffer, _FileSystemNameBuffer, FileSystemNameSize)
		return 0
		
	def GetFileAttributes(self, FileName):
		if FileName == "\\":
			return FILE_ATTRIBUTE_DEVICE
		elif FileName == self.HelloWorldName:
			return FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_READONLY
		else:
			return FILE_ATTRIBUTE_NORMAL
	
	def GetFileInformationFunc(self, FileName, Buffer, DokanFileInfo):
		FileName = FileName.replace('/', '\\')
		if FileName == "\\":
			dwFileAttributes = self.GetFileAttributes(FileName)
			_Buffer = _BY_HANDLE_FILE_INFORMATION(dwFileAttributes, FILETIME(0, 0),
				FILETIME(0, 0), FILETIME(0, 0), self.DriverSerialNumber, 0, 0, 0, 
				0, 0)
			print _Buffer, _Buffer.dwFileAttributes
			dokanMemTools.setByHandleFileInformationByPoint(Buffer, _Buffer)
			return 0
		elif FileName == self.HelloWorldName:
			dwFileAttributes = self.GetFileAttributes(FileName)
			_Buffer = BY_HANDLE_FILE_INFORMATION(dwFileAttributes, FILETIME(0, 0),
				FILETIME(0, 0), FILETIME(0, 0), self.DriverSerialNumber, 0, len(self.HelloWorldText), 0,
				0, 0)
			print _Buffer, _Buffer.dwFileAttributes
			dokanMemTools.setByHandleFileInformationByPoint(Buffer, _Buffer)
			return 0
		else:
			return -ERROR_FILE_NOT_FOUND
		
	def FindFilesFunc(self, FileName, FillFindData, DokanFileInfo):
		return 0
	
	def FindFilesWithPatternFunc(self, FileName, SearchPattern, FillFindData, DokanFileInfo):
		print FileName, SearchPattern, FillFindData
		if FileName == '\\':
			File = WIN32_FIND_DATAW(FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_READONLY, FILETIME(1, 1),
				FILETIME(1, 1), FILETIME(1, 1), 0, len(self.HelloWorldText), 0, 0, 'Hello_World.txt',
				'Hello_~1.txt')
			pFile = PWIN32_FIND_DATAW(File)
			FillFindData(pFile, DokanFileInfo)
			return 0
		else:
			return -ERROR_FILE_NOT_FOUND
	
	# Its no ready
	#def ReadFileFunc(self, FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset, DokanFileInfo):
		#print "FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset", FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset
		#if self.first:
			#lenBuff = (len(self.HelloWorldText) + 1) * 2
			#self.first = False
		#else:
			#lenBuff = 0
		#dokanMemTools.setStringByPoint(Buffer, self.HelloWorldText, lenBuff)
		#dokanMemTools.setDwordByPoint(NumberOfBytesWritten, lenBuff)
		#return 0
	
	#def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, DokanFileInfo):
		#print "FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes", FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes
		#if FileName == '\\':
			#pass
			#return 0
		#elif FileName == self.HelloWorldName:
			#self.first = True
			#return 0x00000001
		#else:
			#return INVALID_HANDLE_VALUE
		
	
DriveOption = DOKAN_OPTION_DEBUG |DOKAN_OPTION_STDERR | DOKAN_OPTION_KEEP_ALIVE
helloFS = HelloFS("Y:\\", DriveOption, 0x19831116L)
helloFS.main()
