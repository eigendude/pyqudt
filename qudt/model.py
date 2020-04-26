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
################################################################################

import collections
import json
import pyld.jsonld
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional


_Coerce = collections.namedtuple('_Coerce', ['iri', 'converter'])
_Link = collections.namedtuple('_Link', ['iri'])

def coerce(iri: Any, converter: Callable[[Any], Any]) -> _Coerce:
    return _Coerce(str(iri), converter)

def link(iri: Any) -> _Link:
    return _Link(str(iri) if iri else None)

def nested(iri: Any) -> _Coerce:
    return coerce(iri, lambda obj: obj.jsonld() if obj else None)


class BaseModel:
    """
    Base model for alternative representations, such as JSON-LD.

    TODO: Document schema format. It should be apparent that values are either
    JSON-LD keywords, IRIs or tuples with the second term being a coercion
    function or type.
    """
    # The model schema
    _SCHEMA: ClassVar[Dict[str, Any]] = dict()

    # The JSON-LD context
    _CONTEXT: ClassVar[Dict[str, Any]] = dict()

    def __post_init__(self) -> None:
        """
        Dataclass hook to initialize data model using a schema provided by the
        child class. Child must provide a _SCHEMA that is ignored by the
        dataclass, either by leaving it unannotated or, preferably, using the
        ClassVar type.
        """
        parent_obj: object = self
        schema: Dict[str, Any] = self._SCHEMA

        # Get list of fields defined by the parent object. The object's fields
        # must have been set before passing its 'self' to this constructor.
        schema_fields = list(parent_obj.__dict__.keys())

        # Field names mapped to JSON-LD keywords, namely @id and @type
        self._id_field: Optional[str] = None
        self._type_field: Optional[str] = None

        # JSON-LD keywords mapped to IRIs, which override fields mapped to
        # keywords
        self._id_iri: Optional[str] = None
        self._type_iri: Optional[str] = None

        # If a field is not defined in the schema, an exception will be raised
        try:
            self._schema = {
                field: schema[field] for field in schema_fields
            }
        except KeyError as e:
            raise KeyError(f'_SCHEMA in class {self.__class__.__name__} is missing the following key: {e}') from e

        # Generate table of coercions
        self._coercions = {
            field: schema[field].converter for field in schema_fields
            if self._has_coercion(schema[field])
        }

        # Generate list of links
        self._links = [
            field for field in schema_fields
            if self._has_link(schema[field])
        ]

        # Handle fields
        for field, iri in self._schema.items():
            # Skip fields set to None
            if iri is None:
                continue

            # Coercions and links are saved in member variables, so replace
            # with the IRI now
            if self._has_coercion(iri):
                iri = iri.iri
                self._schema[field] = iri
            elif self._has_link(iri):
                iri = iri.iri
                self._schema[field] = iri

            # Handle fields mapped to JSON-LD keywords
            if iri == '@id':
                self._id_field = field
            elif iri == '@type':
                self._type_field = field

        # Strip fields that map to JSON-LD keywords, they will be added in jsonld()
        if self._id_field is not None:
            del self._schema[self._id_field]
        if self._type_field is not None:
            del self._schema[self._type_field]

        # Handle type and ID overrides in the original schema
        if '@id' in schema:
            self._id_iri = schema['@id']
        if '@type' in schema:
            self._type_iri = schema['@type']

    def jsonld(self) -> Dict[str, Any]:
        # Create the document for regular fields
        result = {
            field: self._link_value(self._coerce_field(field))
            for field in self._schema.keys()
        }

        # Include JSON-LD keyword fields
        if self._id_field:
            result['@id'] = getattr(self, self._id_field)
        if self._type_field:
            result['@type'] = getattr(self, self._type_field)

        # Handle field overrides
        if self._id_iri:
            result['@id'] = self._id_iri
        if self._type_iri:
            result['@type'] = self._type_iri

        # Expand the object using the generated context
        result = pyld.jsonld.expand(
            result,
            options={
                'expandContext': [
                    self._schema,
                ]
            }
        )[0]

        result = pyld.jsonld.compact(result, ctx=self._CONTEXT)

        if '@context' in result:
            del result['@context']

        return result

    def serialize(self) -> str:
        js = self.jsonld()

        content = json.dumps(js, indent=4, sort_keys=True)

        return content

    def _coerce_field(self, field: Any) -> Any:
        value = getattr(self, str(field))

        # Coerce using converter if specified
        if field in self._coercions:
            coercion = self._coercions[field]
            return coercion(value)

        # Coerce to link if specified
        if field in self._links:
            return _Link(value)

        return value

    @classmethod
    def _link_value(cls, value: Any) -> Any:
        if cls._has_link(value):
            return cls._make_link(value.iri)

        return value

    @staticmethod
    def _has_coercion(term: Any) -> bool:
        return isinstance(term, _Coerce)

    @staticmethod
    def _has_link(term: Any) -> bool:
        return isinstance(term, _Link)

    @staticmethod
    def _make_link(term: str) -> Dict[str, str]:
        return {
            "@id": term
        }
