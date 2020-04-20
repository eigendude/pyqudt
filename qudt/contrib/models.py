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

import json
import pyld.jsonld
from typing import Any
from typing import Dict
from typing import Optional


class BaseModel:
    """
    Base model for alternative representations, such as JSON-LD.
    """
    def __init__(self, context: Dict[str, str]):
        schema_fields = list(self.__dict__.keys())

        self._id_field: Optional[str] = None
        self._type_field: Optional[str] = None
        self._id_iri: Optional[str] = None
        self._type_iri: Optional[str] = None

        self._context = {
            field: context[field] for field in schema_fields
        }

        # Handle coercions
        self._coercions = {
            field: context[field][1] for field in schema_fields
            if isinstance(context[field], list)
        }

        # Handle type and ID overrides
        if '@id' in context:
            self._id_iri = context['@id']
        if '@type' in context:
            self._type_iri = context['@type']

        # Handle fields
        for field, iri in self._context.items():
            # Dereference fields with coercions
            if isinstance(iri, list):
                iri = iri[0]
                self._context[field] = iri

            # Handle fields mapped to JSON-LD keywords
            if iri == '@id':
                self._id_field = field
            elif iri == '@type':
                self._type_field = field

        # Strip fields that map to JSON-LD keywords, they will be added in jsonld()
        if self._id_field is not None:
            del self._context[self._id_field]
        if self._type_field is not None:
            del self._context[self._type_field]

    def jsonld(self, flatten=True):
        result = {
            field: self._coerce(field) for field in self._context.keys()
        }

        # Handle field overrides
        if self._id_iri:
            result['@id'] = self._id_iri
        if self._type_iri:
            result['@type'] = self._type_iri

        # Include JSON-LD keyword fields
        if self._id_field:
            result['@id'] = getattr(self, self._id_field)
        if self._type_field:
            result['@type'] = getattr(self, self._type_field)

        result = pyld.jsonld.expand(
            result,
            options={
                'expandContext': [
                    self._context,
                ]
            }
        )[0]

        if flatten:
            result = pyld.jsonld.compact(result, ctx={"@context": dict()})

        return result

    def serialize(self, **kwargs):
        js = self.jsonld(**kwargs)

        content = json.dumps(js, indent=2, sort_keys=True)

        return content

    def _coerce(self, field: str) -> Any:
        value = getattr(self, field)

        if field in self._coercions:
            coercion = self._coercions[field]
            return coercion(value)

        return value

    """
    @classmethod
    def from_jsonld(cls, jsonld_document):
        result = pyld.jsonld.compact(jsonld_document, ctx={
            "http:/qudt...": ""
        })
    """
