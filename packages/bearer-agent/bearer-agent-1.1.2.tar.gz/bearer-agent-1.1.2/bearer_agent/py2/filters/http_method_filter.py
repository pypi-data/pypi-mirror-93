# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from .base import FilterType, Filter


class HttpMethodFilter(Filter):
    type_name = FilterType.HttpMethodFilter

    def __init__(self, filter_dict):
        super(HttpMethodFilter, self).__init__(filter_dict)
        self.method = filter_dict["value"]

    def match(self, report, filters):
        return self.method == report.log.get("method", None)
