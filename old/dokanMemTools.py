from ctypes import *

debug = False

def setDwordByPoint(valueAddress, value):
	'''
	valueAddress[0] = value && 0xff
	valueAddress[1] = (value >> 8) && 0xff 
	'''
	i = 0
	while i < 4:
		#print value, i
		memset(valueAddress+i, value&0xff, 1)
		i += 1
		value >>= 8
	return valueAddress + 4


def setLongLongByPoint(valueAddress, value):
	setDwordByPoint(valueAddress, value & 0xffffffff)
	setDwordByPoint(valueAddress+4, (value>>32) & 0xffffffff)
	return valueAddress + 8


def setStringByPoint(valueAddress, value, length):
	cnt = 0
	for i in value:
		cnt += 2
		if cnt+2 > length:
			break
		#0061: u'a' -> 0x00000000: 61, 0x00000001: 00
		memset(valueAddress, ord(i)&0xff, 1)
		valueAddress += 1
		memset(valueAddress, (ord(i)>>8)&0xff, 1)
		valueAddress += 1
	memset(valueAddress, 0, 1)
	valueAddress += 1
	memset(valueAddress, 0, 1)
	return valueAddress + length

def setFileTimeByPoint(valueAddress, value):
	valueAddress = setDwordByPoint(valueAddress, value.dwLowDateTime)
	valueAddress = setDwordByPoint(valueAddress, value.dwHighDateTime)
	return valueAddress

def setByHandleFileInformationByPoint(valueAddress, value):
	valueAddress = setDwordByPoint(valueAddress, value.dwFileAttributes)
	valueAddress = setFileTimeByPoint(valueAddress, value.ftCreationTime)
	valueAddress = setFileTimeByPoint(valueAddress, value.ftLastAccessTime)
	valueAddress = setFileTimeByPoint(valueAddress, value.ftLastWriteTime)
	valueAddress = setDwordByPoint(valueAddress, value.dwVolumeSerialNumber)
	valueAddress = setDwordByPoint(valueAddress, value.nFileSizeHigh)
	valueAddress = setDwordByPoint(valueAddress, value.nFileSizeLow)
	valueAddress = setDwordByPoint(valueAddress, value.nNumberOfLinks)
	valueAddress = setDwordByPoint(valueAddress, value.nFileIndexHigh)
	valueAddress = setDwordByPoint(valueAddress, value.nFileIndexLow)
	return valueAddress
	
#def setByPoint(valueAddress, value):
	
