from enum import Enum
from copy import copy, deepcopy

import unittest
from pynio.properties import (AttrDict, SolidDict,
                              TypedDict, TypedList, TypedEnum)

mystr = 'abcdefg'
mydict = dict(zip(mystr, range(len(mystr))))
mydict['own'] = copy(mydict)


class TestAttrDict(unittest.TestCase):
    def test_basic(self):
        attrdict = AttrDict(mydict)
        assert copy(attrdict) is not attrdict
        assert copy(attrdict) == attrdict
        assert deepcopy(attrdict) == attrdict
        assert isinstance(attrdict['own'], AttrDict)


class TestTypedDict(unittest.TestCase):
    def test_set(self):
        convert = TypedDict(mydict)
        convert.a = 8  # works
        assert convert.a == 8
        convert['b'] = 9.3  # works
        assert convert['b'] == 9
        assert convert.b == convert['b']

    def test_error(self):
        convert = TypedDict(mydict)
        self.assertRaises(ValueError, setattr, convert, 'c', 'hello')

    def test_frozen(self):
        frozen = TypedDict(mydict, frozentypes=dict)
        frozen.a = 5
        assert frozen['a'] == 5
        self.assertRaises(TypeError, setattr, frozen, 'own', TypedDict({}))
        self.assertRaises(TypeError, setattr, frozen, 'own', {})


class TestSolid(unittest.TestCase):
    def test_basic(self):
        solid = SolidDict(mydict)
        assert isinstance(solid['own'], SolidDict)
        solid.f = 8
        assert solid.f is 8
        assert solid['f'] == solid.f
        self.assertRaises(AttributeError, setattr, solid, 'dne', 'whatever')
