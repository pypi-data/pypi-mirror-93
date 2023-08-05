# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import wrapt

from .intercept_httpcore import has_attribute, http2_request_wrapper, http2_close_wrapper


def intercept(module):
    if has_attribute(module, "AsyncHTTP2Connection.arequest"):
        wrapt.wrap_function_wrapper(
            module,
            "AsyncHTTP2Connection.arequest",
            http2_request_wrapper,
        )
    else:
        wrapt.wrap_function_wrapper(
            module,
            "AsyncHTTP2Connection.request",
            http2_request_wrapper,
        )
    wrapt.wrap_function_wrapper(
        module,
        "AsyncHTTP2Connection.aclose",
        http2_close_wrapper,
    )
