# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import wrapt

from .intercept_httpcore import http2_request_wrapper, http2_close_wrapper


def intercept(module):
    wrapt.wrap_function_wrapper(
        module,
        "SyncHTTP2Connection.request",
        http2_request_wrapper,
    )
    wrapt.wrap_function_wrapper(
        module,
        "SyncHTTP2Connection.close",
        http2_close_wrapper,
    )
