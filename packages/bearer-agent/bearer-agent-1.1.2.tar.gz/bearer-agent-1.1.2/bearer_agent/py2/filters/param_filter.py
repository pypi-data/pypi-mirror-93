# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from .base import FilterType, KeyValueFilterBase


class ParamFilter(KeyValueFilterBase):
    type_name = FilterType.ParamFilter

    def match(self, report, filters):
        if "params" not in report.log:
            return False
        return self._match(report.log["params"])
