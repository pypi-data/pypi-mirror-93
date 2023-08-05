# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from bearer_agent import six
from bearer_agent.version import version_info, __version__

if six.PY3:
    from bearer_agent.py3.agent import init
else:
    from bearer_agent.py2.agent import init


__ALL__ = [init, version_info, __version__]
