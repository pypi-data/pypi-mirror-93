# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

import functools
from socket import error as SocketError
import sys

from bearer_agent.six.moves.urllib.parse import urlparse, parse_qs
import bearer_agent.six.moves.http_client as _client

import wrapt

from .. import agent
from ..report import (
    ReportLog,
    CONNECT_STAGE,
    INIT_REQUEST_STAGE,
    REQUEST_STAGE,
    INIT_RESPONSE_STAGE,
    RESPONSE_STAGE,
)
from ..util import reraise, classname, ReadProxy, BufferProxy


START_STATES = [CONNECT_STAGE, INIT_REQUEST_STAGE]


def _pass_through(instance, stage_type=None):
    if agent.is_disabled():
        return True

    if getattr(instance, "_bearer_disabled", False):
        return True

    report = getattr(instance, "_bearer_report", None)
    if _report_already_in_stage(report, stage_type):
        return True

    # This shouldn't happen but if something went wrong then avoid errors for the user
    return report is None and stage_type not in START_STATES


def _report_already_in_stage(report, stage_type):
    if report is None:
        return False

    if report.stage_type != stage_type:
        return False

    # For the connect stage, the report might be one from a previous call using
    # the same connection. All previous calls should have ended in a later stage,
    # unless an error occurred
    return not (stage_type in START_STATES and report.is_error)


def httpclient_connect_wrapper(wrapped, instance, args, kwargs, protocol):
    if _pass_through(instance, CONNECT_STAGE):
        return wrapped(*args, **kwargs)

    report = getattr(instance, "_bearer_report", None) or ReportLog()

    if instance._tunnel_host:
        host = instance._tunnel_host
        port = instance._tunnel_port
    else:
        host = instance.host
        port = instance.port

    if not report.protocol:
        report.protocol = protocol

    report.update({"hostname": host, "port": port, "protocol": protocol}, stage_type=CONNECT_STAGE)
    instance._bearer_report = report

    try:
        return wrapped(*args, **kwargs)
    except Exception as exc:
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


def process_request_headers(headers):
    headers_dict = {}
    for line in headers:
        key, val = line.decode("ascii").split(":", 1)
        headers_dict[key] = val.strip()
    return headers_dict


def httpclient_putrequest_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance, INIT_REQUEST_STAGE):
        return wrapped(*args, **kwargs)

    report = ReportLog()

    old_report = getattr(instance, "_bearer_report", None)
    if old_report is not None:
        report.update(
            {
                "hostname": old_report.log["hostname"],
                "port": old_report.log["port"],
                "protocol": old_report.log["protocol"],
            }
        )

    def parse_putrequest(method, url, **_kwargs):
        o = urlparse(url)
        path = o.path
        params = parse_qs(o.query)
        return {"method": method, "path": path, "params": params}

    report.update(parse_putrequest(*args, **kwargs), stage_type=INIT_REQUEST_STAGE)
    instance._bearer_report = report

    try:
        return wrapped(*args, **kwargs)
    except Exception as exc:
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


# TODO: support body given as file object
def httpclient_endheaders_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance, REQUEST_STAGE):
        return wrapped(*args, **kwargs)

    report = instance._bearer_report

    def parse_end_headers(conn, message_body=None, **_kwargs):
        # don't process headers there, only return relevant part as a list
        # this will be processed later
        return message_body, (process_request_headers, conn._buffer[1:])

    req_body, headers = parse_end_headers(instance, *args, **kwargs)

    report.update({"requestHeaders": headers}, stage_type=REQUEST_STAGE)

    if req_body is not None:
        if isinstance(req_body, str):
            report.request_body.write(req_body.encode("utf-8"))
        elif isinstance(req_body, bytes):
            report.request_body.write(req_body)
        else:
            # try to wrap the request body so we can still read it
            largs = list(args)
            if hasattr(req_body, "read"):
                proxy = ReadProxy(req_body, report.request_body)
            else:
                try:
                    # we check if it has a buffer interface,
                    # if not we will use an iterator over the body
                    memoryview(req_body)
                except TypeError:
                    try:
                        proxy = BufferProxy(iter(req_body), report.request_body)
                    except TypeError:
                        proxy = BufferProxy(req_body, report.request_body)
                else:
                    proxy = BufferProxy(req_body, report.request_body)

            largs[0] = proxy
            args = tuple(largs)

    try:
        return wrapped(*args, **kwargs)
    except Exception as exc:
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


def process_response_headers(headers):
    if isinstance(headers, list):
        headers_dict = {}
        for key, val in headers:
            headers_dict[key] = val
        return headers_dict
    return headers


def httpclient_getresponse_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance, INIT_RESPONSE_STAGE):
        return wrapped(*args, **kwargs)

    report = instance._bearer_report
    report.stage_type = INIT_RESPONSE_STAGE

    try:
        response = wrapped(*args, **kwargs)
        # update response stage
        report.update(
            {
                "statusCode": response.status,
                "responseHeaders": (process_response_headers, response.getheaders()),
            },
            stage_type=RESPONSE_STAGE,
        )
        response._bearer_report = report

        return response
    except _client.ResponseNotReady:
        # do nothing if response is not ready, this is an app error.
        # reset the stage so we can come in here again
        report.stage_type = REQUEST_STAGE
        reraise(*sys.exc_info())
    except (_client.HTTPException, SocketError) as exc:
        if report is not None:
            report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())
    except Exception:
        # reset the stage so we can come in here again
        report.stage_type = REQUEST_STAGE
        reraise(*sys.exc_info())


def httpclient_connection_close_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    instance._bearer_report.end_report()

    return wrapped(*args, **kwargs)


def httpclient_response_close_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    instance._bearer_report.end_report()

    return wrapped(*args, **kwargs)


def httpclient_response_read_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    report = instance._bearer_report

    try:
        if report.response_proxy:
            return wrapped(*args, **kwargs)

        chunk = wrapped(*args, **kwargs)
        report.response_body.write(chunk)
        return chunk
    except (_client.HTTPException, SocketError) as exc:
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


def intercept(module):
    wrapt.wrap_function_wrapper(
        module,
        "HTTPConnection.connect",
        functools.partial(httpclient_connect_wrapper, protocol="http"),
    )

    wrapt.wrap_function_wrapper(
        module,
        "HTTPSConnection.connect",
        functools.partial(httpclient_connect_wrapper, protocol="https"),
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.putrequest", httpclient_putrequest_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.endheaders", httpclient_endheaders_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.getresponse", httpclient_getresponse_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.close", httpclient_connection_close_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPResponse.close", httpclient_response_close_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPResponse.read", httpclient_response_read_wrapper
    )
