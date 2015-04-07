#coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

from common.decorator.chain import DecoratorChain
from .wrapper import DataWrapper
from .struct import FILETIME
import time

class DateTimeConvertor(object):

    def __init__(self, dt):
        self.dt = dt

    def update(self, dt):
        self.dt = dt
        return self

    def convert(self):
        value = int((time.mktime(self.dt.timetuple()) + 11644473600) * 10000000)
        return FILETIME(value >> 32, value & 0xFFFFFFFF)
    
class SizeConvert(object):

    def __init__(self, size):
        self.size = size

    def update(self, size):
        self.size = size

    def convert(self):
        return [self.size >> 32, self.size & 0xFFFFFFFF]

def wrap(*proto_args):
    '''
    Декоратор для оборачивания "сырых" параметров callback-функций, которые 
    вызывает драйвер dokan'а, в удобные для работы объекты.
    '''
    def decorator(func):
        chain = DecoratorChain.get(func)
        
        def converter(self, *call_args):
            if len(proto_args) != len(call_args):
                e = 'Number of prototypes doesn\'t match number of args'
                raise Exception(e)
            
            call_args = list(call_args)
            
            for idx, proto in enumerate(proto_args):
                if proto is not None:
                    arg = call_args[idx]
                    arg = proto(arg)
                    call_args[idx] = arg
                    
            return chain.call(self, *call_args)
        
        chain.append(converter)
        return chain.caller
    return decorator
        
def log(*arg_names):
    '''
    Декоратор для логирования вызовов callback-функций dokan'а. Рассчитан на 
    декорирование методов классов, в которых есть self.app.
    '''
    
    def decorator(func):
        chain = DecoratorChain.get(func)
        padding = 3
        
        def logger(self, *args):
            if len(arg_names) != len(args):
                e = 'Number of prototypes doesn\'t match number of args'
                raise Exception(e)
            
            log_lines = ['%s(' % func.__name__]
            last_arg_idx = len(args) - 1
            
            for idx, arg in enumerate(args):
                wrapper = isinstance(arg, DataWrapper)
                lines = arg.debug_repr() if wrapper else \
                    '\'' + str(arg) + '\'' if isinstance(arg, str) else str(arg)
                lines = lines.splitlines()
                
                log = '%s%s = %s' % (' ' * padding, arg_names[idx], lines[0])
                log_lines.append(log)
                
                for line in lines[1:]:
                    log_lines.append(' ' * padding + line)
                    
                if idx != last_arg_idx:
                    log_lines[-1] += ','
                
            log_lines.append(')')
            
            # Ставим блокировку на время записи в лог, чтобы сообщения от разных
            # потоков не перемешивались
            self.log_lock.acquire()
            try:
                log = self.app.log
                for line in log_lines:
                    log.debug(line)
            finally:
                self.log_lock.release()
            
            retval = chain.call(self, *args)
            
            self.log_lock.acquire()
            try:
                log.debug('%s(): %s ' % (func.__name__, retval))
            finally:
                self.log_lock.release()
            
            return retval
        
        chain.append(logger)
        return chain.caller
    return decorator
