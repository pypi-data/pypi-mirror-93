# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import FilterType, KeyValueFilterBase


class RequestBodyFilter(KeyValueFilterBase):
    type_name = FilterType.RequestBodyFilter

    def match(self, report, filters):
        if "requestBody" not in report.log:
            return False
        return self._match(report.log["requestBody"])
