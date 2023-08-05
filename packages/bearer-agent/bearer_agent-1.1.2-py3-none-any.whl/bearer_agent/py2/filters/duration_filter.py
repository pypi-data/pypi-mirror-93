# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import FilterType, RangeFilterBase


class DurationFilter(RangeFilterBase):
    type_name = FilterType.DurationFilter

    def match(self, report, filters):
        return self._match(report.duration)
