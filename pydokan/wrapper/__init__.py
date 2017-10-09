# coding=utf-8
from ..debug import force_breakpoint

class DataWrapper(object):
    pass

class FlagsWrapper(DataWrapper):
    
    flags = []
    
    by_pointer = False
    
    def __init__(self, mask=0):
        self.mask = mask if not self.by_pointer else mask[0]
    
    def debug_repr(self):
        flags = [f for f, m in self.flags if self & m]
        debug = ' | '.join(flags) if len(flags) else '0'
        return debug
    
    def raw(self):
        return self.mask
    
    def __and__(self, flag):
        return self.mask & flag
    
    def __or__(self, flag):
        return self.__class__(self.mask | flag)
    
    def __eq__(self, other):
        return self.mask == other
    
    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self.debug_repr())

class StructWrapper(DataWrapper):
    fields = []
    
    multiline = False
    
    def __init__(self, struct):
        self._struct = struct
        
    def raw(self):
        return self._struct
        
    struct = property(lambda self: self._struct[0])

    @staticmethod
    def field(x):
        return property(lambda s: getattr(s.struct, x),
                               lambda s, v: setattr(s.struct, x, v))
    @staticmethod
    def field_bool(x):
        property(lambda s: bool(getattr(s.struct, x)),
                                    lambda s, v: setattr(s.struct, x, 1 if v else 0))
        
    def debug_repr(self):
        debug = self.__class__.__name__ + '('
        if self.multiline:
            debug += '\r\n'
        
        lines = []
        for field, name in self.fields:
            attr = getattr(self, name)
            wrapper = isinstance(attr, DataWrapper)
            attr = attr.debug_repr() if wrapper else attr
            
            pad = ' ' * 3 if self.multiline else ''
            line = '%s%s = %s' % (pad, field, attr)
            lines.append(line)
        
        sep = ',\r\n' if self.multiline else ', '
        debug += sep.join(lines)
        debug += '\r\n)' if self.multiline else ')'
        return debug
    
    def __repr__(self):
        return '<%s>' % self.debug_repr()