################################################################################
#
#  Copyright (C) 2019 Garrett Brown
#  This file is part of pyqudt - https://github.com/eigendude/pyqudt
#
#  pyqudt is derived from jQUDT
#  Copyright (C) 2012-2013  Egon Willighagen <egonw@users.sf.net>
#
#  SPDX-License-Identifier: BSD-3-Clause
#  See the file LICENSE for more information.
#
################################################################################


class OntologyUtils(object):
    """
    Utility functions for working with ontologies.
    """

    # Registered namespaces
    _namespaces = {}

    @classmethod
    def register_namespace(cls, shorthand, namespace):
        """
        Register shorthand for a namespace.

        :param shorthand: The shorthand, e.g. 'xsd'
        :param namespace The namespace, e.g. 'http://www.w3.org/2001/XMLSchema#'
        """
        cls._namespaces[shorthand] = namespace

    @classmethod
    def get_namespace(cls, shorthand: str) -> str:
        """
        Get the namespace for the given shorthand.

        :param shorthand: The shorthand, e.g. 'xsd'
        :return: The namespace, e.g. 'http://www.w3.org/2001/XMLSchema#'
        """
        return cls._namespaces[shorthand]

    @classmethod
    def get_uri(cls, shorthand: str, local_part: str) -> str:
        """
        Get the full URI given the namespace shorthand and the local part

        :param shorthand: The namespace shorthand, e.g. 'xsd'
        :param local_path: The local part of the URI
        :return: The full URI containing the namespace and local part
        """
        return cls.get_namespace(shorthand) + local_part
