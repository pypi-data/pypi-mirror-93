# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from .base import FilterType, Filter


class ConnectionErrorFilter(Filter):
    type_name = FilterType.ConnectionErrorFilter

    def match(self, report, filters):
        return report.log["type"] == "REQUEST_ERROR"
