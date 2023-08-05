# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from bearer_agent import six

import binascii
import hashlib
import json
import numbers
from collections import OrderedDict


class PrimitiveTypes:
    OBJECT = 0
    ARRAY = 1
    STRING = 2
    NUMBER = 3
    BOOLEAN = 4
    NULL = 5


def to_shape(value):
    if isinstance(value, list):
        return Shape(PrimitiveTypes.ARRAY, items=[to_shape(item) for item in value])
    elif isinstance(value, dict):
        return Shape(
            PrimitiveTypes.OBJECT,
            fields=[
                OrderedDict([("hash", to_shape(value[key])), ("key", key)])
                for key in sorted(value.keys())
            ],
        )
    elif isinstance(value, str):
        return Shape(PrimitiveTypes.STRING)
    # booleans inherit from Number so this must come before that
    elif isinstance(value, bool):
        return Shape(PrimitiveTypes.BOOLEAN)
    elif isinstance(value, numbers.Number):
        return Shape(PrimitiveTypes.NUMBER)
    elif value is None:
        return Shape(PrimitiveTypes.NULL)


def to_hash(value):
    return binascii.b2a_hex(to_shape(value).to_bytes()).decode()


def to_sha(value):
    return hashlib.sha256(to_shape(value).to_bytes()).hexdigest()


class Shape(object):
    def __init__(self, type, fields=[], items=[], rules=[]):
        self.type = type
        self.fields = fields
        self.items = items
        self.rules = rules

    def __repr__(self):
        return "<{cls}:type={type}, fields={fields}>".format(
            cls=self.__class__, type=self.type, fields=self.fields
        )

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.fields == other.fields
            and self.items == other.items
            and self.rules == other.rules
        )

    def to_bytes(self):
        return six.ensure_binary(json.dumps(self.as_json(), separators=(",", ":")))

    def as_json(self):
        fields = []
        for field in self.fields:
            field["hash"] = field["hash"].as_json()
            fields.append(field)

        return OrderedDict(
            [("fields", fields),
             ("items", [item.as_json() for item in self.items]),
             ("rules", self.rules),
             ("type", self.type)]
        )
