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
from collections import namedtuple
import copy
import inspect
import json


_Alias = namedtuple('Alias', ['indict', 'default'])


def alias(key, default=None):
    return _Alias(key, default)


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
        defaults = dict()
        aliases = dict()

        for base in bases:
            if hasattr(base, '_defaults'):
                defaults.update(getattr(base, '_defaults'))
            if hasattr(base, '_aliases'):
                aliases.update(getattr(base, '_aliases'))

        info, rest = mcs.split_attrs(attrs)

        for i in list(info.keys()):
            if isinstance(info[i], _Alias):
                aliases[i] = info[i].indict
                if info[i].default is not None:
                    defaults[i] = info[i].default
            else:
                defaults[i] = info[i]

        rest['_defaults'] = defaults
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

        This allows adding default values in the class definition.
        e.g.:
        """
        is_attr = dict()
        rest = dict()

        for key, value in attrs.items():
            if not BaseMeta.is_internal(key) and not BaseMeta.is_func(value):
                is_attr[key] = value
            else:
                rest[key] = value

        return is_attr, rest

    @staticmethod
    def get_defaults(schema):
        temp = dict()

        for obj in [
            schema,
        ] + schema.get('allOf', list()):
            for key, value in obj.get('properties', dict()).items():
                if 'default' in value and key not in temp:
                    temp[key] = value['default']

        return temp

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

    _defaults = dict()
    _aliases = {
        "id": "@id",
        "resource_iri": "@id",
    }

    def __init__(self, *args, **kwargs):
        super().__init__()

        for key, value in self._defaults.items():
            self[key] = copy.copy(value)

        for arg in args:
            self.update(arg)

        for key, value in kwargs.items():
            self[key] = value

        return self

    def serializable(self, **kwargs):
        def ser_or_down(item):
            if hasattr(item, 'serializable'):
                return item.serializable(**kwargs)
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

        return ser_or_down(self.as_dict(**kwargs))

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

    def as_dict(self, verbose=True, aliases=False):
        attrs = self.__dict__.keys()

        if not verbose and hasattr(self, '_terse_keys'):
            attrs = self._terse_keys + ['@type', '@id']

        result = {
            key: getattr(self, key) for key in attrs
            if not self._internal_key(key) and hasattr(self, key)
        }

        if not aliases:
            return result

        # The name 'old_key' is inferred from original naming 'ok'. This
        # assumption may be incorrect
        for key, old_key in self._aliases.items():
            if old_key in result:
                result[key] = getattr(result, old_key)
                del result[old_key]

        return result

    def __iter__(self):
        return (key for key in self.__dict__ if not self._internal_key(key))

    def __len__(self):
        return len(self.__dict__)

    def update(self, other):
        for key, value in other.items():
            self[key] = value

    def _attr_to_key(self, key):
        key = key.replace('__', ':', 1)
        key = self._aliases.get(key, key)
        return key

    def _key_to_attr(self, key):
        if self._internal_key(key):
            return key

        if key in self._aliases:
            key = self._aliases[key]
        else:
            key = key.replace(':', '__', 1)

        return key

    def __getattr__(self, key):
        # The name 'new_key' is inferred from original naming 'nkey'. This
        # assumption may be incorrect
        new_key = self._attr_to_key(key)

        if new_key in self.__dict__:
            return self.__dict__[new_key]
        elif new_key == key:
            raise AttributeError(f'Key not found: {key}')

        return getattr(self, new_key)

    def __setattr__(self, key, value):
        super().__setattr__(self._attr_to_key(key), value)

    def __delattr__(self, key):
        super().__delattr__(self._attr_to_key(key))

    @staticmethod
    def _internal_key(key):
        return key[0] == '_'

    def __str__(self):
        return json.dumps(self.serializable(), sort_keys=True, indent=4)

    def __repr__(self):
        return json.dumps(self.serializable(), sort_keys=True, indent=4)
