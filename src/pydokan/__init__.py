# coding=utf8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

"""Пакетный модуль для связи питона с Dokan драйвером.

"""

__version__ = "0.1.0"
__author__  = "Eugene Frolov"
__mail__    = "profisphantom@gmail.com"



from sys import platform, stderr
from ctypes import *
from types import MethodType

from .errors import *
from .struct import *
from .debug import debug

if platform == 'win32':
    DOKAN_DLL = windll.dokan
else:
    print(platform, "platform not supported!!!", stderr)


# Dokan Class
class Dokan():
    """ Основной класс для работы с драйвером.
    
    При возникновении ошибки, необходимо вернуть отрицательное значение.
    Как правило, вы должны вернуться GetLastError () * -1.
    
    """
    
    def __init__(self, mount_point, options, threads_count, version=600):
        """Инициализация класса Dokan
        
        mount_point   - путь, куда будет примонтирован драйвер
        options       - см файл struct секцию Dokan Options 
        threads_count - кол-во потоков в драйвере.
        version       - Версия используемого драйвера. Пока поддерживается
                        только 0.6 версия.
        
        """
        
        self.mount_point = mount_point
        self.options = options
        self.threads_count = threads_count
        self.version = version
    
    def main(self):
        """Вызов этой функции приводик к запуску драйвера.
        
        options    - Структура которая описывает опции драйвера
        operations - Структура которая описывает call-back функции
        
        Результат 0 если все успешно или код ошибки.
        
        """
        
        # Перечисляем пары (сишный_тип_функции, функция)
        op_funcs = [
            (CreateFileFuncType,           self.create_file),
            (OpenDirectoryFuncType,        self.open_directory),
            (CreateDirectoryFuncType,      self.create_directory),
            (CleanupFuncType,              self.cleanup),
            (CloseFileFuncType,            self.close),
            (ReadFileFuncType,             self.read),
            (WriteFileFuncType,            self.write),
            (FlushFileBuffersFuncType,     self.flush),
            (GetFileInformationFuncType,   self.get_info),
            (FindFilesFuncType,            self.find_files),
            (FindFilesWithPatternFuncType, self.find_files_with_pattern),
            (SetFileAttributesFuncType,    self.set_attributes),
            (SetFileTimeFuncType,          self.set_time),
            (DeleteFileFuncType,           self.delete_file),
            (DeleteDirectoryFuncType,      self.delete_directory),
            (MoveFileFuncType,             self.move),
            (SetEndOfFileFuncType,         self.set_end_of_file),
            (SetAllocationSizeFuncType,    self.set_allocation_size),
            (LockFileFuncType,             self.lock_file),
            (UnlockFileFuncType,           self.unlock_file),
            (GetDiskFreeSpaceFuncType,     self.get_free_space),
            (GetVolumeInformationFuncType, self.get_volume_info),
            (UnmountFuncType,              self.preunmount),
            (GetFileSecurityFuncType,      self.get_security_info),
            (SetFileSecurityFuncType,      self.set_security_info)
        ]
        
        operations = []
        for func_type, func in op_funcs:
            # Декорируем функцию отладчиком
            new_func = debug(func)
            
            if getattr(func, 'decorator_chain', False):
                # Делаем из обёртки метод объекта, чтобы в него передавался self
                new_func = MethodType(new_func, self)
            
            # Добавляем указатель на функцию в список
            operations.append(func_type(new_func))
        
        operations = DOKAN_OPERATIONS(*operations)
        options = DOKAN_OPTIONS(
            self.version,
            self.threads_count,            # number of threads to be used
            self.options,                  # combination of DOKAN_OPTIONS_*
            0,                             # FileSystem can use this variable
            self.mount_point               # mount point "M:\" (drive letter)
                                           # or "C:\mount\dokan" (path in NTFS)
        )
        
        return int(DOKAN_DLL.DokanMain(
            PDOKAN_OPTIONS(options), 
            PDOKAN_OPERATIONS(operations)
        ))
        
    def umount(self):
        """Отмонтирование драйвера
        
        Результат True если все успешно. False в противном случае
        
        """
        return bool(DOKAN_DLL.DokanRemoveMountPoint(
            self.mount_point
        ))
    
    def name_in_expression(self, expression, name, ic=True):
        """ Проверяет подходит ли имя под шаблон
        
        expression - Выражение с которым производится сравнение. Выражение может
                     включать в себя спецзнаки ?(один любой символ) и *(множество
                     любых символов)
        name       - Имя которое сравнивается
        ic         - Игнорировать ли регистр букв?
        
        Результат True если имя попадает под шаблон, False в противном случае
        
        """
        return bool(DOKAN_DLL.DokanIsNameInExpression(
            LPCWSTR(expression), # matching pattern
            LPCWSTR(name),       # file name
            BOOL(ic)             # Ignore case?
        ))
    
    def version(self):
        """Версия библиотеки драйвера
        
        Результатом является число, которое означает версию библиотеки драйвера
        
        """
        return int(DOKAN_DLL.DokanVersion())
        
    def driver_version(self):
        """Версия драйвера
        
        Результатом является число, которое означает версию драйвера
        
        """
        return int(DOKAN_DLL.DokanDriverVersion())
    
    def reset_timeout(self, timeout, dokan_file_info):
        """Допустимая задержка для операций драйвера
        
        Результат True если все упешно. False в противном случае
        
        """
        return bool(DOKAN_DLL.DokanResetTimeout(
            ULONG(timeout),                        # timeout in millisecond
            PDOKAN_FILE_INFO(dokan_file_info)
        ))
    
    def open_requestor_token(self, dokan_file_info):
        """Получить дискриптор доступа
        
        Этот метод должен быть вызван в таких функциях как create_file, 
        open_directory или create_directoty. Если Вы воспользывались данным
        методом, вы должны будите вызвать CloseHandle после этого.
        
        Результат HANDLE открываемого, создаваемого файла.
        """
        return HANDLE(DOKAN_DLL.DokanOpenRequestorToken(
            PDOKAN_FILE_INFO(dokan_file_info)
        ))
    
    # int (DOKAN_CALLBACK *CreateFile) (LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO);
    def create_file(self, path, access, share_mode, disposition, flags, file_info):
        """ Создание или открытие файла
        
        path            - Путь к файлу относительно точки монтирвания драйвера
        
        access          - Запрошеный доступ к файлу. Например чтение GENERIC_READ,
                          запись GENERIC_WRITE или оба (GENERIC_READ | GENERIC_WRITE)
                          Если этот параметр равен 0, то приложение может запросить
                          определенные метаданные, такие как тип файла или атрибуты 
                          доступа к файлу, даже если доступ с флагом GENERIC_READ
                          запрещен. Вы не должны разрешать доступ к файлу если 
                          доступ протеворечит share_mode ранее открытым файлам и
                          вернуть ERROR_SHARING_VIOLATION
        
        share_mode      - Возможные права доступа к файлу, пока открыт этот дискриптор.
                          Эсли этот параметр равен 0, и открытие произошло успешно
                          файл больше не может быть успешно открыт, пока этот дескриптор
                          не будет закрыт. Вы не должны позволять устанавливать
                          значения этого параметра при последующих открытиях файла,
                          которые протеворечат установленным разрешениям. В этом случае
                          вы должны будите вернуть ERROR_SHARING_VIOLATION. Возможные
                          значения или их комбинации:
                          0 - запрещает любой доступ к файлу, кроме чтения метаданных.
                          FILE_SHARE_DELETE - Разрешает удалять, а так же переименовывать
                              файл. Если это флаг не установлен, то любое открытие файла,
                              для его удаления потерпит неудачу.
                          FILE_SHARE_READ - Позволяет при последующем открытии просить
                              доступ на чтение. если флаг не установлен, последующие
                              функции на открытие файла для чтения потерпят неудачу.
                          FILE_SHARE_WRITE - Позволяет при последующем открытии просить
                              доступ на запись. если флаг не установлен, последующие
                              функции на открытие файла для запись потерпят неудачу.
                          Влаги можно комбинировать между собой с помощью |
        
        disposition     - Меры которые следует предпринять при условии что файл 
                          существует или несуществует. Этот параметр может быть 
                          один из следующих параметров:
                          CREATE_ALWAYS - Если файл существует и доступен для 
                              записи функция перезапишет файл изавершится успешно
                              и код возврата доджен быть установлен в ERROR_ALREADY_EXISTS
                              Если указанный файл не существует, что является 
                              правильным, будет создан новый файл и результатом 
                              выполнения функции будет 0 
                          CREATE_NEW - Создает новый файл, только если он не 
                              существует. Если указанный файл существует функция
                              потерпит неудачу и результатом выполнения должен 
                              стать ERROR_FILE_EXISTS. сли файл не существует, и
                              это правильно, то функция создает файл и результатом
                              выполнения является 0
                          OPEN_ALWAYS - Открывает файл всегда, если файл существует
                              то файл открывается успешно и результат выполнения 
                              функции ERROR_ALREADY_EXISTS. Если файл не существует
                              и это правильно, функция создает файл и результат 
                              выполнения функции равен 0
                          OPEN_EXISTING - Открывает файл только если он существует
                              Если указанный файл не существует, то функция терпит
                              неудачу, а результатом выполнения ERROR_FILE_NOT_FOUND
                          TRUNCATE_EXISTING - Открывает файл и обрезает его так,
                              что его размер становится равен 0. Если указанный файл
                              не существует, функция терпит неудачу и результатом
                              выполнения будет ERROR_FILE_NOT_FOUND.
        
        flags           - Флаги для созаваемого файла, обычно это FILE_ATTRIBUTE_NORMAL
                          но могут быть и другие FILE_ATTRIBUTE_ * см msdn
        
        Если файл является каталогом вы должны вернуть 0 если католог может быть 
        открыт и file_info.IsDirectory установить в True. Ели disposition
        является CREATE_ALWAYS или OPEN_ALWAYS и файл существует необходимо вернуть
        ERROR_ALREADY_EXISTS не отрицательным значением.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *OpenDirectory) (LPCWSTR, PDOKAN_FILE_INFO);
    def open_directory(self, path, file_info):
        """Открытие каталога
        
        Данная функция вызывается если система пытается открыть каталог
        
        Параметры:
            path -  Путь к открываемому каталогу относительно точки монтирвания 
                    драйвера
        
        Необходимо вернуть 0 если открыть каталог возможно в противном случае 
        код ошибки
        
        """
        return -1

    # int (DOKAN_CALLBACK *CreateDirectory) (LPCWSTR, PDOKAN_FILE_INFO);
    def create_directory(self, path, file_info):
        """Создание директории
        
        Данная функция вызывается, когда необходимо создать директорию.
        
        Параметры:
            path -  Путь к создаваемому каталогу относительно точки монтирвания 
                    драйвера
        
        Необходимо создать каталог и вернуть 0 если это возможно иначе код ошибки
        
        """
        return -1

    # int (DOKAN_CALLBACK *Cleanup) (LPCWSTR, PDOKAN_FILE_INFO);
    def cleanup(self, path, file_info):
        """Очистка перед закрытием файла
        
        Данная функция вызывается перед закрытием файла
        
        Параметры:
            path -  Путь к файлу или директории относительно точки монтирвания 
                    драйвера
        
        Если file_info.DeleteOnClose является True, вы должны удалить этот
        файл непосредственно в этой функции. Если очистка произошла удачно вернуть
        0 иначе код ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *CloseFile) (LPCWSTR, PDOKAN_FILE_INFO);
    def close(self, path, file_info):
        """Закрытие открытых файлов и директорий
        
        Данная функция вызывается если дескриптор файла закрывается
        
        Параметры:
            path -  Путь к файлу или директории относительно точки монтирвания 
                    драйвера
        
        Если закрытие произшло удачно, результатом выполнения функции 0 иначе
        код ошибки.
        """
        return -1
    
    # int (DOKAN_CALLBACK *ReadFile) (LPCWSTR, LPVOID, DWORD,  LPDWORD, LONGLONG, PDOKAN_FILE_INFO);
    def read(self, path, buffer, length, buff_length, offset, file_info):
        """Чтение открытого файла
        
        Данная функция вызывается когда программа пытается считать какую-то часть 
        файла
        
        Параметры:
            path   - Путь к файлу относительно точки монтирвания драйвера
            
            buffer - Буфер в который будет записана запрашиваемая информация
            
            length - Кол-во запрашиваемых байт на чтение
            
            buff_length - Кол-во записанных байт в буфер
            
            offset - Смещение от начала файла
        
        Если чтение возможно, в буфер записываются данные, в переменную buff_length
        записывается кол-во байт записанных в buffer. И результатом выполнения 
        функции 0. В противном случае код ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *WriteFile) (LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO);
    def write(self, path, buffer, length, writen_length, offset, file_info):
        """Запись открытого файла
        
        Данная функция вызывается когда программа пытается записать какую-то часть 
        файла
        
        Параметры:
            path   - Путь к файлу относительно точки монтирвания драйвера
            
            buffer - Буфер с информацией.
            
            length - Кол-во записываемых байт
            
            buff_length - Кол-во записанных байт
            
            offset - Смещение от начала файла
        
        Если запись возможна, в файл записываются данные, в переменную writen_length
        записывается кол-во байт записанных в файл. И результатом выполнения 
        функции 0. В противном случае код ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *FlushFileBuffers) (LPCWSTR, PDOKAN_FILE_INFO);
    def flush(self, path, file_info):
        """Сброс буфера данных файла на диск
        
        Данная функция вызывается если программа хочет сбросить данные файла на 
        диск
        
        Параметры:
            path   - Путь к файлу относительно точки монтирвания драйвера
        
        Если сброс данных с буфера возможен, результат 0. В противном случае код
        ошибки
        """
        return 0
    
    # int (DOKAN_CALLBACK *GetFileInformation) (LPCWSTR,  LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO);
    def get_info(self, path, buffer, file_info):
        """Информация об открытом файле или папке 
        
        Данная функция вызывается если программа пытается получить информацию о 
        файле или папке.
        
        Параметры:
            path   - Путь к файлу относительно точки монтирвания драйвера
            
            buffer - Буфер, куда будет записана информация о файле
        
        Если возможно вернуть информацию о файле или папке, то в буфер должна 
        быть записана информация о файле или папке и результатом выполнения 
        функции 0, в противном случае код ошибки. 
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *FindFiles) (LPCWSTR,    PFillFindData, PDOKAN_FILE_INFO);
    def find_files(self, path, func, dokan_file_info):
        """Поиск файлов.
        
        Эта функция не используется
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *FindFilesWithPattern) (LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO);
    def find_files_with_pattern(self, path, pattern, func, file_info):
        """Поиск файлов по шаблону
        
        Эта функция вызывается когда программа пытается получить список файлов
        подходящий под определенный шаблон
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            pattern - Шаблон, которому должны удовлетворять файлы.
            
            func    - Функция обратного вызова. Если поиск успешен и есть 
                      результаты, то эта функция должна быть вызвана с результатом
                      в качестве параметра.
        
        Если успешно все прошло успешно, результатом выполнения 0, иначе код 
        ошибки 
        Если вы используете эту функцию для поиска информации, то функция 
        find_files будет отключена.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *SetFileAttributes) (LPCWSTR, DWORD, PDOKAN_FILE_INFO);
    def set_attributes(self, path, attr, file_info):
        """Установка атрибутов файлов
        
        Эта функция вызывается, когда программа желает поменять атрибуты файла
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            attr    - Новые атрибуты файла
        
        Если установку атрибутов возможно применить, то они применяются в этой 
        функции и результатом выполнения функции 0, иначе код ошибки.
        """
        return 0
    
    # int (DOKAN_CALLBACK *SetFileTime) (LPCWSTR, CONST FILETIME*, CONST FILETIME*, CONST FILETIME*, PDOKAN_FILE_INFO);
    def set_time(self, path, c_time, a_time, w_time, file_info):
        """Установка новых дат для файла или директории
        
        Это функция вызывается если программа пытается обновить даты файла
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            c_time  - Новое время создания файла
            
            a_time  - Новое время последнего доступа к файлу
            
            w_time  - Новое время последней подификации файла.
        
        Если изменить даты возможно, то результатом выполнения функции 0 иначе 
        код ошибки.
        
        """
        return 0
    
    # int (DOKAN_CALLBACK *DeleteFile) (LPCWSTR, PDOKAN_FILE_INFO);
    def delete_file(self, path, file_info):
        """Удаление файла
        
        Это функция вызывается если программа пытается удалить файл
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
        
        Вы не должны удалять файл в нутри этой функции. Вы должны проверить 
        возможно ли удалить файл в этой функции и если возможно вернуть 0, иначе 
        код ошибки таких как -ERROR_SHARING_VIOLATION и т.д. Удаление необходимо
        будет произвести в функции очиски, когда file_info.DeleteOnClose будет
        установлено в True
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *DeleteDirectory) (LPCWSTR, PDOKAN_FILE_INFO);
    def delete_directory(self, path, file_info):
        """Удаление директории
        
        Это функция вызывается если программа пытается удалить директорию
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
        
        Вы не должны удалять директорию в нутри этой функции. Вы должны проверить 
        возможно ли удалить файл в этой функции и если возможно вернуть 0, иначе 
        код ошибки таких как --ERROR_DIR_NOT_EMPTY и т.д. Удаление необходимо
        будет произвести в функции очиски, когда file_info.DeleteOnClose будет
        установлено в True
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *MoveFile) (LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO);
    def move(self, src, dst, replace, file_info):
        """Перемещение файла или директории
        
        Это функция вызывается если программа пытается переместить файл или 
        директорию
        
        Параметры:
            src    - Путь к перемещаемому файлу.
        
            dst    - Путь куда перемещается файл
        
        Эта функция так жк может быть использована в качестве переименования 
        файлов
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *SetEndOfFile) (LPCWSTR, LONGLONG, PDOKAN_FILE_INFO);
    def set_end_of_file(self, path, offset, file_info):
        """Устанавливает физический конец файла
        
        Эта функция вызываетсякогда программа делает установить физический конец
        файла. Она используется для того, чтобы сократить или удлинить файл. Если 
        файл удлиняется, содержание файла между старой позицией EOF и новой 
        позицией не определяется.
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            offset  - Смещение в позицию в которой необходимо установить 
                      физический конец файла.
        
        Если функция выполняется успешно, то результатом функции 0, иначе код 
        ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *SetAllocationSize) (LPCWSTR, LONGLONG, PDOKAN_FILE_INFO);
    def set_allocation_size(self, path, offset, file_info):
        """Устанавливает логический конец файла
        
        Функция устанавливает правильную длину данных заданного файла. Эта функция 
        устанавливает логический конец файла.
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            offset  - Смещение в позицию в которой необходимо установить 
                      логический конец файла.
        
        Если функция выполняется успешно, то результатом функции 0, иначе код 
        ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *LockFile) (LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO);
    def lock_file(self, path, offset, length, file_info):
        """Блокировка файла
        
        Функция блокирует заданный файл для единоличного доступа вызывающего 
        процесса.
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            offset  - Смещение от начала файла
            
            length  - Кол-во байт которые будут заблокированны начиная от offset
        
        Если функция выполняется успешно, то результатом функции 0, иначе код 
        ошибки. Байты, которые находятся за пределами конца текущего файла тоже
        могут быть заблокированны. Это полезно для координации добавляемых 
        записей в конец файла.
        
        Блокировки не могут накладываться на существующую блокированную область 
        файла.
        
        """
        return 0
    
    # int (DOKAN_CALLBACK *UnlockFile) (LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO);
    def unlock_file(self, path, offset, length, file_info):
        """Снятие блокировки с области файла
        
        Функция вызывается когда программа деблокирует область в открытом файле. 
        Разблокирование области дает возможность другим процессам обращаться к 
        ней.
        
        Параметры:
            path    - Путь к файлу относительно точки монтирвания драйвера
            
            offset  - Смещение от начала файла
            
            length  - Кол-во байт которые будут деблокированны начиная от offset
        
        Если функция выполняется успешно, то результатом функции 0, иначе код 
        ошибки. Разблокирование области файла снимает перед этим полученную 
        блокировку файла. Область снятия блокировки должна точно соответствовать
        существующей блокированной области. Две смежных области файла не могут 
        быть заблокированы отдельно, а затем разблокированы, как использующаяся 
        единая область, которая охватывает обе блокированных области.
        
        """
        return 0
    
    # int (DOKAN_CALLBACK *GetDiskFreeSpace) (PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO);
    def get_free_space(self, free_bytes, total_bytes, total_free_bytes, file_info):
        """Сообщает о свободном месте на диске
        
        Эта функция вызываетя кода процесс запрашивает свободное место на диске.
        
        Параметры:
            free_byte        - кол-во свободных байт для текущего пользователя.
            
            total_bytes      - Всего байт на диске
            
            total_free_bytes - Всего свободно байт на диске.
            
            В случае успеха функция записывает в переменные free_bytes, 
            total_bytes и total_free_b корректные значения и результатом 
            выполнения функции является 0. Иначе код ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *GetVolumeInformation) (LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO);
    def get_volume_info(self, name_buff, name_size, sn, max_comonent_len, fs_flags, \
                         fs_name_buff, fs_name_size, file_info):
        """Сообщает информацию о разделе диска
        
        Эта функция вызывается, когда процесс хочет получить информацию о диске.
        
        Параметры:
            name_buff         - Буфер для имени диска. В эту переменную 
                                необходимо записать имя устройства.
            
            name_size         - Размер буфера, куда было записано имя устройства
            
            sn                - Серийный номер устройства
            
            max_component_len - Максимальная длинна имени компонента
            
            fs_flags          - флаги файловой системы
            
            fs_name_buff      - Буфер для имени файловой системы.
            
            fs_name_size      - Размер буфера имени файловой системы.
        
        Если функция завершается упешно, результат выполнения функции должен быть
        0 иначе код ошибки.
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *Unmount) (PDOKAN_FILE_INFO);
    def preunmount(self, file_info):
        """Отключение диска
        
        Это функция вызывается, когда процесс пытается отключить диск, отмонтировать
        В случае успеха результатом выполнения должен быть 0 иначе код ошибки.
        """
        return -1
        
    # int (DOKAN_CALLBACK *GetFileSecurity) (LPCWSTR, PSECURITY_INFORMATION, PSECURITY_DESCRIPTOR, ULONG, PULONG, PDOKAN_FILE_INFO);
    def get_security_info(self, path, inf, desc, desc_length, length_needed, file_info):
        """Сообщает информацию безопасности для файла или директории.
        
        Данная функция вызывается, когда процесс пытается запросить информацию
        о безопасности файла или каталога
        
        Параметры:
            path          - Путь к файлу относительно точки монтирвания драйвера
            
            inf           - Сообщает о том, какая информация запрашивается. 
            
            desc          - Дескриптор собранной информации о запрашиваемом файле.
            
            desc_length   - размер буфера дескриптора
            
            length_needed - Если выделенный размер буфера для дискриптора мал,
                            то в этот параметр устанавливается значение о том,
                            какой объем нужен для буфера дескриптора.
            
            В случае успеха, результат выполнения функции 0, в противном случае
            код ошибки. Если буфер desc мал, для записи дискриптора, то в
            параметр length_needed записывается размер необходимого объема для
            дескриптора и результатом выполнения функции -ERROR_INSUFFICIENT_BUFFER
        
        """
        return -1
    
    # int (DOKAN_CALLBACK *SetFileSecurity) (LPCWSTR, PSECURITY_INFORMATION, PSECURITY_DESCRIPTOR, ULONG, PDOKAN_FILE_INFO);
    def set_security_info(self, path, inf, desc, desc_length, file_info):
        """Устанавливает информацию безопасности для файла или директории.
        
        Данная функция вызывается, когда процесс пытается установить информацию
        о безопасности файла или каталога
        
        Параметры:
            path        - Путь к файлу относительно точки монтирвания драйвера
            
            inf         - Сообщает о том, какая информация устанавливается. 
            
            desc        - Дескриптор описывающий информацию безопасности файла 
                          или директории.
            
            desc_length - размер буфера дескриптора
            
            В случае успеха, результат выполнения функции 0, в противном случае
            код ошибки.
        
        """
        return -1