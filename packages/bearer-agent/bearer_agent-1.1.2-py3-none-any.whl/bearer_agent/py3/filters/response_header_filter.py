# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import FilterType, KeyValueFilterBase


class ResponseHeaderFilter(KeyValueFilterBase):
    type_name = FilterType.ResponseHeaderFilter

    def match(self, report, filters):
        if "responseHeaders" not in report.log:
            return False
        return self._match(report.log["responseHeaders"])
