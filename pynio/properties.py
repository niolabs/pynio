from copy import deepcopy


def isiter(obj):
    return (False if isinstance(obj, (str, bytes))
            else True if
            (hasattr(obj, '__iter__') or hasattr(obj, '__next__'))
            else False)


class AttrDict(dict):
    '''Dictionary that allows item access via getattr'''
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.update(self)

    def update(self, value):
        '''updates self to convert all values to own class type
        '''
        if isinstance(value, dict):
            value = value.items()
        for key, value in value:
            self[key] = value

    def __getattr__(self, attr):
        if attr in self.__dict__:  # prevents recursion from parent classes
            return object.__getattr__(self, attr)
        else:
            return self[attr]

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            object.__setattr__(self, attr, value)
        else:
            self[attr] = value

    def __setitem__(self, key, value):
        '''overloaded to automatically convert dictionaries to
        self'''
        if isinstance(value, dict):
            value = self.__class__(value)
        dict.__setitem__(self, key, value)

    def __copy__(self, *args, **kwargs):
        return AttrDict(self)

    def __deepcopy__(self, *args, **kwargs):
        return AttrDict({key: deepcopy(value) for (key, value) in self.items()})


class SolidDict(AttrDict):
    '''Dictionary like object that doesn't allow it's shape to change
    (cannot add or remove keys)
    Does the same for all items inside of it'''
    def __setitem__(self, item, value):
        if item not in self:
            raise KeyError(item)
        AttrDict.__setitem__(self, item, value)

    def __setattr__(self, attr, value):
        if attr not in self and attr not in self.__dict__:
            raise AttributeError(attr)
        AttrDict.__setattr__(self, attr, value)


class TypedDict(AttrDict):
    '''Dictionary like object that keeps track of types. Choose whether
        to attempt to convert types (default) or not allow different types.
        Also specify types that cannot be changed
    Arguments:
        convert: whether to attempt to convert values that don't match
        frozentypes: list/tupple of types to not allow change
    Special Cases:
        If an item is an Enum Class, then it will only allow values that are in
            the Enum Class.
        '''
    def __init__(self, *args, convert=True, frozentypes=tuple(), **kwargs):
        object.__setattr__(self, '_frozentypes', tuple())
        object.__setattr__(self, '_convert', convert)
        super().__init__(*args, **kwargs)
        object.__setattr__(self, '_frozentypes', frozentypes)  # freeze types after init
        assert hasattr(self, '_frozentypes')

    def _convert_value(self, value, curval):
        '''Convert value to type(curvalue). Also do associated error checking'''
        if isinstance(curval, self._frozentypes):
            raise TypeError("{} is a frozen type".format(type(curval)))
        curtype = type(curval)
        if not isinstance(value, curtype):
            if self._convert:
                value = curtype(value)
            else:
                raise TypeError("{} is not type {}".format(value, curtype))
        return value

    def __setitem__(self, item, value):
        if item not in self:
            raise KeyError(item)
        curval = self[item]
        value = self._convert_value(value, curval)
        dict.__setitem__(self, item, value)

    def __setattr__(self, attr, value):
        if not hasattr(self, attr):
            raise AttributeError(attr)
        curval = getattr(self, attr)
        value = self._convert_value(value, curval)
        AttrDict.__setattr__(self, attr, value)


class TypedList(list):
    '''A list that preserves types
        type: the type of list elements to preserve
        convert: whether to attempt automatic conversion to type
        noset: don't allow setting of existing elements
    '''
    def __init__(self, type, *args, convert=True, noset=False, **kwargs):
        self._type = type
        self._convert = convert
        self._noset = noset
        list.__init__(self)  # make self an empty list
        convert = self._convert
        self.extend(tuple(*args, **kwargs))

    def _convert_value(self, value):
        if not isinstance(value, type):
            return self._type(value)
            raise TypeError(value)
        return value

    def append(self, value):
        value = self._convert_value(value)
        list.append(self, value)

    def extend(self, iterator):
        for i in iterator:
            self.append(i)

    def __setitem__(self, item, value):
        if self._noset:
            raise IndexError("items cannot be set with noset=True")
        value = self._convert_value(value)
        list.__setitem__(self, item, value)


class TypedEnum:
    '''Class to make setting of enum types valid and error checked'''
    def __init__(self, enum):
        self._enum = enum
        self._enum_by_value = {e.value: e for e in enum}
        self._enum_by_name = {e.name: e for e in enum}
        self._value = next(iter(enum))

    @property
    def value(self):
        return self._value.value

    @value.setter
    def value(self, value):
        if value in self._enum_by_name:
            value = self._enum_by_name[value]
        elif value in self._enum_by_value:
            value = self._enum_by_value[value]
        else:
            raise ValueError("Value does not exist in enum: {}".format(value))
        self._value = value

    @property
    def name(self):
        return self._value.name

    def __repr__(self):
        return repr(self.value)
