# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from bearer_agent import six
from ..util import flag

import re
import operator

KNOWN_FILTERS = []


class FilterType(object):
    # Structural
    FilterSet = "FilterSet"
    NotFilter = "NotFilter"

    # Connection
    DomainFilter = "DomainFilter"

    # Request
    PathFilter = "PathFilter"
    HttpMethodFilter = "HttpMethodFilter"
    ParamFilter = "ParamFilter"
    RequestHeaderFilter = "RequestHeaderFilter"

    # Response
    ResponseHeaderFilter = "ResponseHeaderFilter"
    StatusCodeFilter = "StatusCodeFilter"

    # Bodies
    RequestBodyFilter = "RequestBodyFilter"
    RequestBodySizeFilter = "RequestBodySizeFilter"
    ResponseBodyFilter = "ResponseBodyFilter"
    ResponseBodySizeFilter = "ResponseBodySizeFilter"

    # Error
    ConnectionErrorFilter = "ConnectionErrorFilter"

    # Bodies/Error
    DurationFilter = "DurationFilter"


class FilterMeta(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(FilterMeta, cls).__new__
        parents = [b for b in bases if isinstance(b, FilterMeta)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        new_class = super_new(cls, name, bases, attrs)
        KNOWN_FILTERS.append(new_class)
        return new_class


class Filter(object):
    type_name = None

    def __init__(self, filter_dict):
        self.filter_dict = filter_dict

    def match(self, log, filters):
        raise NotImplementedError


Filter = FilterMeta("Filter", (Filter,), {})


class RegularExpression(object):
    def __init__(self, value, flags=None):
        self.value = (value,)
        self.flags = flags
        self._regexp = re.compile(value, flag(flags))

    def match(self, string):
        if self._regexp.search(string):
            return True

        return False


class RangeFilterBase(Filter):
    def __init__(self, filter_dict):
        super(RangeFilterBase, self).__init__(filter_dict)

        range_dict = filter_dict["range"]
        from_value = range_dict.get("from")
        from_exclusive = range_dict.get("fromExclusive", False)
        to_value = range_dict.get("to")
        to_exclusive = range_dict.get("toExclusive", False)

        self.from_ = float(from_value) if from_value is not None else None
        self.from_op = operator.gt if from_exclusive else operator.ge
        self.to = float(to_value) if to_value is not None else None
        self.to_op = operator.lt if to_exclusive else operator.le

    def _match(self, value):
        if value is None:
            return False

        return (
            (self.from_ is None or self.from_op(value, self.from_))
            and (self.to is None or self.to_op(value, self.to))
        )


class KeyValueFilterBase(Filter):
    def __init__(self, filter_dict):
        super(KeyValueFilterBase, self).__init__(filter_dict)

        value_pattern_dict = filter_dict.get("valuePattern")
        key_pattern_dict = filter_dict.get("keyPattern")
        self.value_pattern = (
            RegularExpression(**value_pattern_dict) if value_pattern_dict else None
        )
        self.key_pattern = (
            RegularExpression(**key_pattern_dict) if key_pattern_dict else None
        )

    def _match(self, value):
        if value is None:
            return False

        if not self.key_pattern and not self.value_pattern:
            return True

        return self._match_value(value)

    def _match_value(self, value):
        if isinstance(value, six.string_types):
            return not self.key_pattern and self.value_pattern.match(value)
        elif isinstance(value, list):
            return any(self._match_value(element) for element in value)
        elif isinstance(value, dict):
            return any(self._match_key_value(key, sub_value) for key, sub_value in value.viewitems())

        return False

    def _match_key_value(self, key, value):
        key_matched = not self.key_pattern or self.key_pattern.match(key)
        if isinstance(value, six.string_types):
            return key_matched and (not self.value_pattern or self.value_pattern.match(value))
        else:
            return (key_matched and not self.value_pattern) or self._match_value(value)
