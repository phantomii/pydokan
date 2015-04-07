#coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

import sys
from common.decorator.chain import DecoratorChain

try:
    import pydevd
except ImportError:
    pydevd = None

module = sys.modules[__name__]
mode = True
catch_funcs = {}

def debug(func):
    chain = DecoratorChain.get(func)
    func = chain.get_func()
    
    def debugger(*args, **kwargs):
        # Если включен режим принудительной отладки
        if module.mode == True:
            # Если функция в списке функций, для которых отладка задействована
            if module.catch_funcs[func.__name__]:
                # Останавливаем выполнение кода
                force_breakpoint()
        
        return chain.call(*args, **kwargs)
    
    # Если функции ещё нет в списке перехватываемых функций
    if func.__name__ not in module.catch_funcs:
        # то вносим в список и включаем перехват
        enable(func.__name__)
    
    #chain.append(wrapper)
    # Вставляем наш декоратор первым в цепочку, в таком случае он будет 
    # декорировать саму функцию и будет вызван последним изо всех декораторов
    chain.insert(0, debugger)
    return chain.caller

def force_breakpoint():
    if pydevd: pydevd.settrace()

def enable(func_name):
    '''
    Задействует перехват вызовов указанной функции.
    '''
    module.catch_funcs[func_name] = True

def disable(func_name):
    '''
    Выключает перехват вызовов указанной функции.
    '''
    module.catch_funcs[func_name] = False
