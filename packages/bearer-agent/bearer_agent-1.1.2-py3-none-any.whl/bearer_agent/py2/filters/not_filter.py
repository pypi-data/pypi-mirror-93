# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from .base import FilterType, Filter


class NotFilter(Filter):
    type_name = FilterType.NotFilter

    def __init__(self, filter_dict):
        super(NotFilter, self).__init__(filter_dict)

        if "childHash" not in filter_dict:
            raise TypeError("Invalid NotFilter")

        self.child_hash = filter_dict["childHash"]

    def match(self, report, filters):
        if self.child_hash not in filters:
            return False

        filter_ = filters[self.child_hash]
        return not filter_.match(report, filters)
