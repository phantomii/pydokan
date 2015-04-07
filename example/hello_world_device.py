# coding=utf-8
# Hello World File System.

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU GPL'
__version__ = '0.1'


from sys import path
path.append('..')

from pydokan import Dokan
from pydokan.struct import DOKAN_OPTION_KEEP_ALIVE, DOKAN_OPTION_REMOVABLE,\
    LPWSTR, WIN32_FIND_DATAW, PWIN32_FIND_DATAW, LPSTR
from pydokan.wrapper.file import AccessMode, ShareMode, CreationDisposition, FlagsAndAttributes
from pydokan.wrapper.dokan import DokanFileInfo
from pydokan.wrapper.security import SecurityInfo
from pydokan.win32con import ERROR_FILE_NOT_FOUND, FILE_ATTRIBUTE_DIRECTORY,\
    ERROR_INVALID_HANDLE, FILE_CASE_SENSITIVE_SEARCH, FILE_UNICODE_ON_DISK,\
    FILE_SUPPORTS_ENCRYPTION, FILE_SUPPORTS_REMOTE_STORAGE, FILE_ATTRIBUTE_NORMAL
from pydokan.utils import wrap, log, DateTimeConvertor, SizeConvert
from pydokan.debug import disable as disable_debug, force_breakpoint

from datetime import datetime
from threading import Thread, Lock
import traceback, logging, logging.handlers
from ctypes import memmove, string_at



class HelloWorldFS(Dokan, Thread):
    
    files = {'\\hello_world.txt': b'Hello World',
             '\\ReadMe.txt': b'To unmount the disk, enter the path H:\\exit'}
    
    def __init__(self, app, mount_point, options, threads_count, version=600):
        self.app = app
        Dokan.__init__(self, mount_point, options, threads_count, version)
        Thread.__init__(self)
        self.mount_code = 0
        self.serial_number = 0x19831116
        # Lock for decorator @log. Callback`s loging...
        self.log_lock = Lock()
        self.counter = 1
    
    def run(self):
        self.mount_code = 0
        self.mount_code = self.main()
    
    def log_exception(self):
        lines = traceback.format_exc().splitlines()
        self.log_lock.acquire()
        try:
            log = self.app.log
            for line in lines:
                log.error(line)
        finally:
            self.log_lock.release()
    
    @wrap(None, AccessMode, ShareMode, CreationDisposition, FlagsAndAttributes, DokanFileInfo)
    @log('path', 'access', 'share_mode', 'disposition', 'flags', 'info')
    def create_file(self, path, access, share_mode, disposition, flags, file_info):
        # Unmount disk if enter h:\exit path
        if path == '\\exit':
            self.umount()
        elif path == '\\':
            file_info.is_directory = True
        elif path in self.files.keys():
            file_info.context = self.counter
            self.counter += 1
        else:
            return -ERROR_FILE_NOT_FOUND 
        return 0           
    disable_debug('create_file')
    
    @wrap(None, DokanFileInfo)
    @log('path', 'info')
    def open_directory(self, path, file_info):
        if path == '\\':
            file_info.context = self.counter
            self.counter += 1
            return 0
        else:
            return -ERROR_FILE_NOT_FOUND
    disable_debug('open_directory')
    
    @wrap(None, None, DokanFileInfo)
    @log('path', 'buf', 'info')
    def get_info(self, path, buffer, file_info):
        if file_info.context:
            if path in self.files.keys():
                buffer[0].dwFileAttributes = FILE_ATTRIBUTE_NORMAL
                win_size = SizeConvert(len(self.files[path])).convert()
                buffer[0].nFileSizeHigh = win_size[0]
                buffer[0].nFileSizeLow = win_size[1]
                buffer[0].nNumberOfLinks = 1
                win_index = SizeConvert(2).convert()
                buffer[0].nFileIndexHigh = win_index[0]
                buffer[0].nFileIndexLow = win_index[1]
            elif path == '\\':
                buffer[0].dwFileAttributes = FILE_ATTRIBUTE_DIRECTORY
                buffer[0].nFileSizeHigh = 0
                buffer[0].nFileSizeLow = 0
                buffer[0].nNumberOfLinks = 1
                win_index = SizeConvert(1).convert()
                buffer[0].nFileIndexHigh = win_index[0]
                buffer[0].nFileIndexLow = win_index[1] 
            dt_converter = DateTimeConvertor(datetime.today())
            dc = dt_converter.convert()
            buffer[0].ftCreationTime = dc
            buffer[0].ftLastAccessTime = dc
            buffer[0].ftLastWriteTime = dc
            buffer[0].dwVolumeSerialNumber = self.serial_number
            return 0    
        else:
            return -ERROR_INVALID_HANDLE
    disable_debug('get_info')
    
    @wrap(None, DokanFileInfo)
    @log('path', 'info')
    def cleanup(self, path, file_info):
        if file_info.context:
            if file_info.delete_on_close:
                return -1
            file_info.context = 0
            return 0
        else:
            return -ERROR_INVALID_HANDLE
    disable_debug('cleanup')  
    
    @wrap(None, DokanFileInfo)
    @log('path', 'info')
    def close(self, path, file_info):
        if file_info.context:
            print("ERROR: File not cleanupped?")
            file_info.context = 0
            return 0
        else:
            return 0
    disable_debug('close')
    
    @wrap(None, None, None, None, None, None, None, DokanFileInfo)
    @log('name', 'name_size', 'serial', 'max_component_len', \
         'fs_flags', 'fs_name', 'fs_name_size', 'info')
    def get_volume_info(self, name_buff, name_size, sn, max_comonent_len, \
                        fs_flags, fs_name_buff, fs_name_size, file_info):
        name = 'Hello World Device'
        fname = 'HelloWorldFS'
        memmove(name_buff, LPWSTR(name), (len(name) + 1) * 2)
        memmove(fs_name_buff, LPWSTR(fname), (len(fname) + 1) * 2)
        sn[0] = self.serial_number
        max_comonent_len[0] = 255
        
        flags = FILE_SUPPORTS_ENCRYPTION | FILE_UNICODE_ON_DISK | \
            FILE_SUPPORTS_REMOTE_STORAGE | FILE_CASE_SENSITIVE_SEARCH
        
        fs_flags[0] = flags
        return 0
    disable_debug('get_volume_info')
    
    @wrap(None, None, None, DokanFileInfo)
    @log('avail', 'total', 'free', 'info')
    def get_free_space(self, free_bytes, total_bytes, total_free_bytes, file_info):
        free_bytes[0] = 1048576 - len(self.files['\\hello_world.txt'])
        total_bytes[0] = 1048576
        total_free_bytes[0] = 1048576
        return 0
    disable_debug('get_free_space')
    
    @wrap(None, None, None, DokanFileInfo)
    @log('path', 'pattern', 'func', 'info')
    def find_files_with_pattern(self, path, pattern, func, file_info):
        file_info_raw = file_info.raw()
        if file_info.context:
            if path == '\\':
                dc = DateTimeConvertor(datetime.today()).convert()
                for i in self.files.keys():
                    if self.name_in_expression(pattern, i, False):
                        win_size = SizeConvert(len(self.files[i])).convert()
                        info = WIN32_FIND_DATAW(
                            FILE_ATTRIBUTE_NORMAL, dc, dc, dc, win_size[0],
                            win_size[1], 0, 0, i[1:], ''
                        )
                        func(PWIN32_FIND_DATAW(info), file_info_raw)
            return 0
        else:
            return -ERROR_INVALID_HANDLE
    disable_debug('find_files_with_pattern')
    
    @wrap(None, None, None, None, None, DokanFileInfo)
    @log('path', 'buf', 'length', 'read', 'offset', 'info')
    def read(self, path, buffer, length, buff_length, offset, file_info):
        if file_info.context:
            buff = self.files[path][offset:offset+length]
            memmove(buffer, LPSTR(buff), len(buff))
            buff_length[0] = len(buff)
            return 0
        else:
            return -ERROR_INVALID_HANDLE
        
    disable_debug('read')
    
    @wrap(None, None, None, None, None, DokanFileInfo)
    @log('path', 'buf', 'length', 'written', 'offset', 'info')
    def write(self, path, buffer, length, writen_length, offset, file_info):
        if file_info.context:
            buffer = string_at(buffer, length)
            self.files[path] = self.files[path][:offset] + buffer + self.files[path][offset+length:]
            return 0
        else:
            return -ERROR_INVALID_HANDLE
            
    disable_debug('write')


class App():
    
    def __init__(self):
        self.log = self.get_logger()
    
    def get_logger(self):
        logger = logging.getLogger('vdisk')
        
        level = logging.DEBUG
        logger.setLevel(level)
        
        format = '[%(asctime)s] [%(thread)d] %(levelname)s: %(message)s'
        formatter = logging.Formatter(format)
        
        log_path = './logs/vdisk.log'
        Handler = logging.handlers.TimedRotatingFileHandler
        handler = Handler(log_path, when='D', interval=1, backupCount=5)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger


def main():
    app = App()
    app.hwfs = HelloWorldFS(app, 'H', DOKAN_OPTION_KEEP_ALIVE | DOKAN_OPTION_REMOVABLE, 5)
    app.hwfs.start()

if __name__ == '__main__':
    main()