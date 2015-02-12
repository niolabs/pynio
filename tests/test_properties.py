from pprint import pprint
from enum import Enum
from copy import copy, deepcopy

import unittest

from .example_data import (SimulatorFastTemplate, SimulatorFastConfig)

from pynio.properties import (AttrDict, SolidDict,
                              TypedDict, TypedList, TypedEnum,
                              load_block)

mystr = 'abcdefg'
mydict = dict(zip(mystr, range(len(mystr))))
mydict['own'] = copy(mydict)


class abc(Enum):
    a = 0
    b = 1
    c = 2


class TestAttrDict(unittest.TestCase):
    def test_basic(self):
        attrdict = AttrDict(mydict)
        assert copy(attrdict) is not attrdict
        assert copy(attrdict) == attrdict
        assert deepcopy(attrdict) == attrdict
        assert isinstance(attrdict['own'], AttrDict)


class TestSolid(unittest.TestCase):
    def test_basic(self):
        solid = SolidDict(mydict)
        assert isinstance(solid['own'], SolidDict)
        solid.f = 8
        assert solid.f is 8
        assert solid['f'] == solid.f
        self.assertRaises(AttributeError, setattr, solid, 'dne', 'whatever')


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


class TestTypedList(unittest.TestCase):
    def test_append(self):
        mylist = list(range(10))
        l = TypedList(int, mylist)
        assert l == mylist
        l.append(10)
        l.append(13.4)
        l.append('67')
        assert l[-3:] == [10, 13, 67]

    def test_type_error(self):
        mylist = list(range(10))
        l = TypedList(int, mylist)
        self.assertRaises(ValueError, l.append, 'hello')
        self.assertRaises(ValueError, l.__setitem__, 5, 'hello')

    def test_setitem(self):
        mylist = list(range(10))
        l = TypedList(int, mylist)
        l[0] = 100
        assert l[0] == 100
        l[1] = 3.23423
        assert l[1] == 3


class TestTypedEnum(unittest.TestCase):
    def test_basic(self):
        venum = TypedEnum(abc)
        venum.value = 'a'
        venum.value = 1
        venum.value = abc.a
        with self.assertRaises(ValueError):
            venum.value = 6


class TestLoadProperties(unittest.TestCase):
    def test_load_simulator_template(self):
        blk = load_block(SimulatorFastTemplate)
        print()
        pprint(blk)

    def test_set_simulator(self):
        blk = load_block(SimulatorFastTemplate)
        blk.attribute.name = 'newsim'
        blk.attribute.value.end = 5.8
        blk.interval.days = 100
        pprint(blk)

    def test_typecheck_simulator(self):
        blk = load_block(SimulatorFastTemplate)
        self.assertRaises(TypeError, setattr, blk.attribute.value.end, 'bad')
        self.assertRaises(TypeError, setattr, blk.interval.days, 'bad')
