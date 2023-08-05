# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import pkg_resources


__version__ = pkg_resources.get_distribution("bearer-agent").version
version_info = tuple(int(v) for v in __version__.split("."))
