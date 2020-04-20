################################################################################
#
#  Copyright (C) 2020 Garrett Brown
#  This file is part of pyqudt - https://github.com/eigendude/pyqudt
#
#  pyqudt is derived from jQUDT
#  Copyright (C) 2012-2013  Egon Willighagen <egonw@users.sf.net>
#
#  SPDX-License-Identifier: BSD-3-Clause
#  See the file LICENSE for more information.
#
#  This file is derived from the file 'meta.py' of the Senpy project
#  Copyright 2014 Grupo de Sistemas Inteligentes (GSI) DIT, UPM
#  SPDX-License-Identifier: Apache-2.0
#
################################################################################

"""
Meta-programming for the models.
"""

from abc import ABCMeta
from collections import MutableMapping
import inspect


class BaseMeta(ABCMeta):
    """
    Metaclass for models. It extracts the default values for the fields in the
    model.

    For instance, instances of the following class wouldn't need to mark their
    version of description on initialization:

    .. code-block:: python

       class MyPlugin(Plugin):
           version=0.3
           description='A dull plugin'

    Note that these operations could be included in the __init__ of the class,
    but would be very inefficient.
    """

    def __new__(mcs, name, bases, attrs, **kwargs):
        aliases = dict()

        attrs = mcs.expand_attrs(name, attrs)

        for base in bases:
            if hasattr(base, '_aliases'):
                aliases.update(getattr(base, '_aliases'))

        info, rest = mcs.split_attrs(attrs)

        rest['_aliases'] = aliases

        cls = super().__new__(mcs, name, tuple(bases), rest)

        return cls

    @staticmethod
    def is_func(value):
        return inspect.isroutine(value) or \
            inspect.ismethod(value) or \
            inspect.ismodule(value) or \
            isinstance(value, property)

    @staticmethod
    def is_internal(key):
        return key[0] == '_'

    @staticmethod
    def get_key(key):
        if key[0] != '_':
            key = key.replace('__', ":", 1)
        return key

    @staticmethod
    def split_attrs(attrs):
        """
        Extract the attributes of the class.
        """
        is_attr = dict()
        rest = dict()

        for key, value in attrs.items():
            if not BaseMeta.is_internal(key) and not BaseMeta.is_func(value):
                is_attr[key] = value
            else:
                rest[key] = value

        return is_attr, rest

class CustomDict(MutableMapping):
    """
    A dictionary whose elements can also be accessed as attributes. Since some
    characters are not valid in the dot-notation, the attribute names also
    converted, e.g.:

    >>> d = CustomDict()
    >>> d.key = d['ns:name'] = 1
    >>> d.key == d['key']
    True
    >>> d.ns__name == d['ns:name']
    True
    """

    _aliases = {
        "id": "@id",
        "resource_iri": "@id",
        "type_iri": "@type",
    }

    def __init__(self, *args, **kwargs):
        super().__init__()

        for arg in args:
            self.update(arg)

        for key, value in kwargs.items():
            self[key] = value

        return self

    def serializable(self):
        def ser_or_down(item):
            if hasattr(item, 'serializable'):
                return item.serializable()
            elif isinstance(item, dict):
                temp = dict()

                for kp in item:
                    vp = item[kp]
                    temp[kp] = ser_or_down(vp)

                return temp
            elif isinstance(item, list) or isinstance(item, set):
                return list(ser_or_down(i) for i in item)
            else:
                return item

        return ser_or_down(self.as_dict())

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        """
        Do not insert data directly, there might be a property in that key.
        """
        key = self._key_to_attr(key)
        return setattr(self, key, value)

    def __delitem__(self, key):
        key = self._key_to_attr(key)
        del self.__dict__[key]

    def as_dict(self):
        attrs = self.__dict__.keys()

        result = {
            key: getattr(self, key) for key in attrs
            if not self._internal_key(key) and hasattr(self, key)
        }

        return result

    def update(self, other):
        for key, value in other.items():
            self[key] = value

    def _attr_to_key(self, key):
        key = self._aliases.get(key, key)
        return key

    def _key_to_attr(self, key):
        if self._internal_key(key):
            return key

        if key in self._aliases:
            key = self._aliases[key]

        return key

    def _getattr(self, key):
        # The name 'new_key' is inferred from original naming 'nkey'. This
        # assumption may be incorrect
        new_key = self._attr_to_key(key)

        if new_key in self.__dict__:
            return self.__dict__[new_key]
        elif new_key == key:
            raise AttributeError(f'Key not found: {key}')

        return getattr(self, new_key)

    def _setattr(self, key, value):
        super().__setattr__(self._attr_to_key(key), value)

    def _delattr(self, key):
        super().__delattr__(self._attr_to_key(key))

    @staticmethod
    def _internal_key(key):
        return key[0] == '_'
