# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from .base import FilterType, Filter


class FilterSetOperator(object):
    ANY = "ANY"
    ALL = "ALL"


FilterSetOperators = {"ANY": FilterSetOperator.ANY, "ALL": FilterSetOperator.ALL}


class FilterSet(Filter):
    type_name = FilterType.FilterSet

    def __init__(self, filter_dict):
        super(FilterSet, self).__init__(filter_dict)

        self.operator = FilterSetOperators[filter_dict.get("operator", "ALL")]
        self.child_hashes = filter_dict.get("childHashes", [])

    def _match_all(self, report, filters):
        for h in self.child_hashes:
            if h in filters:
                if not filters[h].match(report, filters):
                    return False
        return True

    def _match_any(self, report, filters):
        for h in self.child_hashes:
            if h in filters:
                if filters[h].match(report, filters):
                    return True
        return False

    def match(self, report, filters):
        if self.operator == FilterSetOperator.ANY:
            return self._match_any(report, filters)
        return self._match_all(report, filters)
