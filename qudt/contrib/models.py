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
#  This file is derived from the file 'models.py' of the Senpy project
#  Copyright 2014 Grupo de Sistemas Inteligentes (GSI) DIT, UPM
#  SPDX-License-Identifier: Apache-2.0
#
################################################################################
"""
Base model

The implementation should mirror the JSON schema definition. For compatibility
with Python 3 and for easier debugging, this new version drops introspection
and adds all arguments to the models.
"""

from qudt.contrib.meta import BaseMeta
from qudt.contrib.meta import CustomDict

import json
import os
import pyld.jsonld
from six import with_metaclass  # TODO: Update for Python 3
import time

CONTEXT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'schemas',
        'context.jsonld'
    )
)

def load_context(context):
    if not context:
        return context
    elif isinstance(context, list):
        contexts = list()
        for c in context:
            contexts.append(load_context(c))
        return contexts
    elif isinstance(context, dict):
        return dict(context)
    elif isinstance(context, str):
        with open(context) as f:
            return dict(json.loads(f.read()))
    else:
        raise AttributeError('Please, provide a valid context')


base_context = load_context(CONTEXT_PATH)


class BaseModel(with_metaclass(BaseMeta, CustomDict)):
    """
    Entities of the base model are a special kind of dictionary that emulates
    a JSON-LD object. For convenience, the values can also be accessed as
    attributes, a la Javascript. e.g.:

    >>> myobject.key == myobject['key']
    True
    >>> myobject.ns__name == myobject['ns:name']
    True

    Additionally, subclasses of this class can specify default values for their
    instances. These defaults are inherited by subclasses. e.g.:

    >>> class NewModel(BaseModel):
    ...     mydefault = 5
    >>> n1 = NewModel()
    >>> n1['mydefault'] == 5
    True
    >>> n1.mydefault = 3
    >>> n1['mydefault'] == 3  # TODO: Upstream has an error using = instead of ==
    True
    >>> class SubModel(NewModel):
    >>>     pass
    >>> subn = SubModel()
    >>> subn.mydefault == 5
    True

    Lastly, every subclass that also specifies a schema will get registered, so
    it is possible to deserialize JSON and get the right type, i.e. to recover
    an instance of the original class from a plan JSON.
    """

    _context = base_context['@context']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def id(self):
        if '@id' not in self:
            self['@id'] = f'prefix:{type(self).__name__}_{time.time()}'
        return self['@id']

    @id.setter
    def id(self, value):
        self['@id'] = value

    def jsonld(self,
               with_context=False,
               context_uri=None,
               prefix=None,
               expanded=False,
               **kwargs):

        result = self.serializable(**kwargs)

        if expanded:
            result = pyld.jsonld.expand(
                result,
                options={
                    'expandContext': [
                        self._context,
                        {
                            'prefix': prefix,
                            'endpoint': prefix,
                        }
                    ]
                }
            )[0]

        if not with_context:
            try:
                del result['@context']
            except KeyError:
                pass
        elif context_uri:
            result['@context'] = context_uri
        else:
            result['@context'] = self._context

        return result

    def serialize(self,
                  prefix=None,
                  **kwargs):
        js = self.jsonld(prefix=prefix, **kwargs)

        content = json.dumps(js, indent=2, sort_keys=True)

        return content
