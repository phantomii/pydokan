# coding=utf-8

__author__  = 'Frolov Evgeniy (profisphantom@gmail.com)'
__license__ = 'GNU LGPL'
__version__ = '0.1'

from threading import local

class DecoratorChain(object):
    
    attr = '__decorators_chain__'
    
    chain_map = {}
    
    @classmethod
    def get(cls, func):
        instance = getattr(func, cls.attr, False)
        if instance:
            return instance
        
        if func not in cls.chain_map:
            instance = cls(func)
            # @todo: Сохранять и имя класса, в котором расположен метод тоже, 
            # иначе возможны коллизии
            cls.chain_map[func] = instance
        
        return cls.chain_map[func]
    
    def __init__(self, func):
        self.func = func
        self.decorators = []
        self.tls = local()
        self.tls.chain = None
        
        def decorator_chain_caller(*args, **kwargs):
            return self.call(*args, **kwargs)
        
        dcc = decorator_chain_caller
        setattr(dcc, 'decorator_chain', True)
        setattr(dcc, self.attr, self)
        setattr(dcc, '__name__', self.func.__name__)
        self.caller = dcc
    
    def get_func(self):
        return self.func
        
    def append(self, decorator):
        self.decorators.append(decorator)
        
    def insert(self, idx, decorator):
        self.decorators.insert(idx, decorator)
        
    def call(self, *args, **kwargs):
        if not hasattr(self.tls, 'chain'):
            chain = self.decorators[:]
            chain.insert(0, self.func)
            self.tls.chain = chain
            
        func = self.tls.chain.pop()
        return func(*args, **kwargs)
    
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
    
    def __repr__(self):
        return '<%s(\'%s decorator(s)\', next=%s)>' % \
               (self.__class__.__name__, len(self.decorators), 
                None if not self.tls.chain else self.tls.chain[-1])