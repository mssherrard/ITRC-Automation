
class BiDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        if args:
            args = args[0]
            if isinstance(args, dict):
                items = args.iteritems()
            else:
                items = iter(args)
            for key, val in items:
                self[key] = val
        if kwargs:
            for key, val in kwargs.iteritems():
                self[key] = val
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        dict.__setitem__(self, val, key)
    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

def concat(seq, sep=''):
    return sep.join(seq)

def delegate(objtype, objname, attrnames):
    
    def makemethod(attr):
        def method(self, *args, **kwargs):
            obj = getattr(self, objname)
            return attr(obj, *args, **kwargs)
        method.__name__ = attr.__name__
        method.__doc__ = attr.__doc__
        return method

    def makemember(attr):
        def fget(self):
            obj = getattr(self, objname)
            return attr.__get__(obj)
        def fset(self, value):
            obj = getattr(self, objname)
            return attr.__set__(obj, value)
        def fdel(self):
            obj = getattr(self, objname)
            return attr.__delete__(obj)
        return property(fget, fset, fdel, attr.__doc__)

    def makeattr(name):
        def fget(self):
            obj = getattr(self, objname)
            return getattr(obj, name)
        def fset(self, value):
            obj = getattr(self, objname)
            return setattr(obj, name, value)
        def fdel(self):
            obj = getattr(self, objname)
            return delattr(obj, name)
        return property(fget, fset, fdel)

    def makedelegate(cls):
        for name in attrnames:
            attr = getattr(objtype, name, None)
            if hasattr(attr, '__call__'):
                attr = makemethod(attr)
            elif hasattr(attr, '__set__'):
                attr = makemember(attr)
            else:
                attr = makeattr(name)
            setattr(cls, name, attr)
        return cls
##        for name, value in objtype.__dict__.items():
##            if not name.startswith('__') and name not in cls.__dict__:
##                if callable(value):
##                    setattr(cls, name, makemethod(name, value))
##                else:
##                    setattr(cls, name, makemember(name, value))
##        return cls
    
    return makedelegate
