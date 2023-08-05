# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import importlib
import sys
from urllib.parse import urlparse, parse_qs

import wrapt

from bearer_agent.py3.report import ReportLog
from bearer_agent.py3.report import CONNECT_STAGE, REQUEST_STAGE, RESPONSE_STAGE
from bearer_agent.py3.util import reraise, classname


def _url_to_origin(url):
    scheme, host, explicit_port = url[:3]
    default_port = {b'http': 80, b'https': 443}[scheme]
    port = default_port if explicit_port is None else explicit_port
    return scheme.decode(), host.decode(), port


class SyncByteStreamProxy(wrapt.ObjectProxy):

    __target__ = None
    __report__ = None
    __stage__ = None

    def __init__(self, wrapped, target, report, stage):
        super().__init__(wrapped)
        self.__target__ = target
        self.__report__ = report
        self.__stage__ = stage

    def __iter__(self):
        it = iter(self.__wrapped__)
        try:
            for chunk in it:
                if isinstance(chunk, str):
                    self.__target__.write(chunk.encode("utf-8"))
                else:
                    self.__target__.write(chunk)
                yield chunk
        except Exception as exc:
            self.__report__.stage_type = self.__stage__
            self.__report__.end_report(classname(exc), "%r" % exc)
            reraise(*sys.exc_info())

    def close(self):
        if self.__stage__ == RESPONSE_STAGE:
            self.__report__.end_report()
        return self.__wrapped__.close()


class AsyncByteStreamProxy(wrapt.ObjectProxy):

    __target__ = None
    __report__ = None
    __stage__ = None

    def __init__(self, wrapped, target, report, stage):
        super().__init__(wrapped)
        self.__target__ = target
        self.__report__ = report
        self.__stage__ = stage

    async def __aiter__(self):
        try:
            async for chunk in self.__wrapped__:
                if isinstance(chunk, str):
                    self.__target__.write(chunk.encode("utf-8"))
                else:
                    self.__target__.write(chunk)
                yield chunk
        except Exception as exc:
            self.__report__.stage_type = self.__stage__
            self.__report__.end_report(classname(exc), "%r" % exc)
            reraise(*sys.exc_info())

    async def aclose(self):
        if self.__stage__ == RESPONSE_STAGE:
            self.__report__.end_report()
        await self.__wrapped__.aclose()


class ResponseByteStreamProxy(wrapt.ObjectProxy):

    __target__ = None
    __report__ = None
    __stage__ = None

    def __init__(self, wrapped, target, report, stage):
        super().__init__(wrapped)
        self.__target__ = target
        self.__report__ = report
        self.__stage__ = stage

    async def __aiter__(self):
        try:
            async for chunk in self.__wrapped__:
                if isinstance(chunk, str):
                    self.__target__.write(chunk.encode("utf-8"))
                else:
                    self.__target__.write(chunk)
                yield chunk
        except Exception as exc:
            self.__report__.stage_type = self.__stage__
            self.__report__.end_report("%r" % exc, exc)
            reraise(*sys.exc_info())

    async def aclose(self):
        if self.__stage__ == RESPONSE_STAGE:
            self.__report__.end_report()
        ret = await self.__wrapped__.aclose()
        return ret


def _process_headers(headers):
    headers_dict = {}
    for name, value in headers:
        headers_dict[name.decode("ascii")] = value.decode("ascii")
        return headers_dict


def sync_synchttpconnection_request_wrapper(wrapped, instance, args, kwargs):
    report = ReportLog()
    syncbytestream_class = getattr(importlib.import_module("httpcore._sync.base"), "SyncByteStream")

    def _parse_request(method, url, headers=None, stream=None, ext=None, **restkw):
        scheme, host, explicit_port = url[:3]
        default_port = {b'http': 80, b'https': 443}[scheme]
        port = default_port if explicit_port is None else explicit_port
        path = url[3].decode()
        parsed_url = urlparse(path)

        request_dict = {
            "hostname": host.decode(),
            "port": port,
            "protocol": scheme.decode(),
            "method": method.decode(),
            "path": path,
            "params": parse_qs(parsed_url.query)
        }
        stream = syncbytestream_class() if stream is None else stream
        return request_dict, stream

    request_dict, req_stream = _parse_request(*args, **kwargs)
    report.update(request_dict, stage_type=CONNECT_STAGE)

    req_stream = SyncByteStreamProxy(req_stream, report.request_body, report, REQUEST_STAGE)
    kwargs["stream"] = req_stream

    try:
        result = wrapped(*args, **kwargs)
        httpcore_legacy = len(result) == 5  # httpcore<0.11

        if httpcore_legacy:
            version, status, reason, resp_headers, resp_stream = result
        else:
            status, resp_headers, resp_stream, ext = result

        report.update(
            {
                "statusCode": status,
                "responseHeaders": (_process_headers, resp_headers)
            },
            stage_type=RESPONSE_STAGE
        )
        resp_stream = SyncByteStreamProxy(resp_stream, report.response_body, report, RESPONSE_STAGE)

        if httpcore_legacy:
            return version, status, reason, resp_headers, resp_stream
        return status, resp_headers, resp_stream, ext
    except Exception as exc:
        report.stage_type = REQUEST_STAGE
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


def _parse_conn_request(method, url, headers=None, stream=None, ext=None, **restkw):
    return headers, stream


def http11_request_wrapper(wrapped, instance, args, kwargs):
    req_headers, req_stream = _parse_conn_request(*args, **kwargs)
    report = getattr(req_stream, "__report__")
    report.update(
        {
            "requestHeaders": (_process_headers, req_headers)
        },
        stage_type=REQUEST_STAGE
    )
    setattr(req_stream, "__report__", report)
    setattr(instance, "_bearer_report", report)
    return wrapped(*args, **kwargs)


def http2_request_wrapper(wrapped, instance, args, kwargs):
    req_headers, req_stream = _parse_conn_request(*args, **kwargs)
    report = getattr(req_stream, "__report__")
    report.update(
        {
            "requestHeaders": (_process_headers, req_headers)
        },
        stage_type=REQUEST_STAGE
    )
    setattr(req_stream, "__report__", report)
    setattr(instance, "_bearer_report", report)
    return wrapped(*args, **kwargs)


def http11_close_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report", None)
    if report is not None:
        report.end_report()
    return wrapped(*args, **kwargs)


def http2_close_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report", None)
    if report is not None:
        report.end_report()
    return wrapped(*args, **kwargs)


def async_asynchttpconnection_request_wrapper(wrapped, instance, args, kwargs):
    report = ReportLog()
    asyncbytestream_class = getattr(importlib.import_module("httpcore._async.base"), "AsyncByteStream")

    def _parse_request(method, url, headers=None, stream=None, ext=None, **restkw):
        scheme, host, explicit_port = url[:3]
        default_port = {b'http': 80, b'https': 443}[scheme]
        port = default_port if explicit_port is None else explicit_port
        path = url[3].decode()
        parsed_url = urlparse(path)

        request_dict = {
            "hostname": host.decode(),
            "port": port,
            "protocol": scheme.decode(),
            "method": method.decode(),
            "path": path,
            "params": parse_qs(parsed_url.query)
        }
        stream = asyncbytestream_class() if stream is None else stream
        return request_dict, stream

    request_dict, req_stream = _parse_request(*args, **kwargs)
    report.update(request_dict, stage_type=CONNECT_STAGE)

    req_stream = AsyncByteStreamProxy(req_stream, report.request_body, report, REQUEST_STAGE)
    kwargs["stream"] = req_stream

    async def _request():
        result = await wrapped(*args, **kwargs)
        httpcore_legacy = len(result) == 5  # httpcore<0.11

        if httpcore_legacy:
            version, status, reason, resp_headers, resp_stream = result
        else:
            status, resp_headers, resp_stream, ext = result

        report.update(
            {
                "statusCode": status,
                "responseHeaders": (_process_headers, resp_headers)
            },
            stage_type=RESPONSE_STAGE
        )
        resp_stream = ResponseByteStreamProxy(resp_stream, report.response_body, report, RESPONSE_STAGE)

        if httpcore_legacy:
            return version, status, reason, resp_headers, resp_stream
        return status, resp_headers, resp_stream, ext

    try:
        return _request()
    except Exception as exc:
        report.stage_type = REQUEST_STAGE
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


def intercept(module):
    wrapt.wrap_function_wrapper(
        module,
        "_sync.connection.SyncHTTPConnection.request",
        sync_synchttpconnection_request_wrapper,
    )
    wrapt.wrap_function_wrapper(
        module,
        "_sync.http11.SyncHTTP11Connection.request",
        http11_request_wrapper,
    )
    wrapt.wrap_function_wrapper(
        module,
        "_sync.http11.SyncHTTP11Connection.close",
        http11_close_wrapper,
    )
    wrapt.wrap_function_wrapper(
        module,
        "_async.http11.AsyncHTTP11Connection.aclose",
        http11_close_wrapper,
    )

    # Newer versions of the library use `arequest`
    if has_attribute(module, "_async.connection.AsyncHTTPConnection.arequest"):
        wrapt.wrap_function_wrapper(
            module,
            "_async.connection.AsyncHTTPConnection.arequest",
            async_asynchttpconnection_request_wrapper,
        )
        wrapt.wrap_function_wrapper(
            module,
            "_async.http11.AsyncHTTP11Connection.arequest",
            http11_request_wrapper,
        )
    else:
        wrapt.wrap_function_wrapper(
            module,
            "_async.connection.AsyncHTTPConnection.request",
            async_asynchttpconnection_request_wrapper,
        )
        wrapt.wrap_function_wrapper(
            module,
            "_async.http11.AsyncHTTP11Connection.request",
            http11_request_wrapper,
        )


def has_attribute(module, name):
    try:
        wrapt.resolve_path(module, name)
        return True
    except AttributeError:
        return False
