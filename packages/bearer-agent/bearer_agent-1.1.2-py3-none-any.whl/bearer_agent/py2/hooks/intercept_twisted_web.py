# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import importlib
import sys

import wrapt

from ..report import ReportLog
from ..report import CONNECT_STAGE, REQUEST_STAGE, RESPONSE_STAGE
from ..util import reraise, classname


def _decode(val):
    if isinstance(val, bytes):
        return val.decode()
    return val


def new_client_request_construct_wrapper(wrapped, _instance, args, kwargs):

    uri_cls = getattr(importlib.import_module("twisted.web.client"), "URI")

    def _parse(method, uri, _headers, _body_producer, persistent=False, parsedURI=None):

        if parsedURI is None:
            parsedURI = uri_cls.fromBytes(uri)

        d = {
            "hostname": _decode(parsedURI.host),
            "port": parsedURI.port,
            "method": _decode(method),
            "protocol": _decode(parsedURI.scheme),
            "path": _decode(parsedURI.path),
            "params": parsedURI.params,
        }
        return d

    report = ReportLog()
    report.update(_parse(*args, **kwargs), stage_type=CONNECT_STAGE)

    try:
        req = wrapped(*args, **kwargs)
        setattr(req, "_bearer_report", report)
        return req
    except Exception as exc:
        report.stage_type = CONNECT_STAGE
        report.end_report(classname(exc), "%r" % exc)
        reraise(*sys.exc_info())


def _process_headers(headers):
    headers_dict = {}
    for hdr_name, hdr_val in headers.getAllRawHeaders():
        hdr_name = _decode(hdr_name)
        hdr_val = _decode(hdr_val[0])
        if hdr_name.lower() == "content-length":
            hdr_val = int(hdr_val)

        headers_dict[hdr_name] = hdr_val
    return headers_dict


class ConsumerProxy(wrapt.ObjectProxy):

    __report__ = None
    __stage__ = None

    def __init__(self, wrapped, report, stage):
        super(ConsumerProxy, self).__init__(wrapped)
        self.__report__ = report
        self.__stage__ = stage

    def write(self, bytes):
        self.__report__.request_body.write(bytes)
        try:
            self.__wrapped__.write(bytes)
        except Exception as exc:
            self.__report__.stage_type = self.__stage__
            self.__report__.end_report(classname(exc), "%r" % exc)
            reraise(*sys.exc_info())


class ProducerProxy(wrapt.ObjectProxy):

    __report__ = None
    __stage__ = None

    def __init__(self, wrapped, report, stage):
        super(ProducerProxy, self).__init__(wrapped)
        self.__report__ = report
        self.__stage__ = stage

    def startProducing(self, consumer):
        consumer_proxy = ConsumerProxy(consumer, self.__report__, self.__stage__)
        return self.__wrapped__.startProducing(consumer_proxy)


def new_client_request_write_headers_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report")
    headers = (_process_headers, instance.headers)
    report.update({"requestHeaders": headers}, stage_type=REQUEST_STAGE)
    setattr(instance, "_bearer_report", report)
    # replace the body produce by our proxy
    setattr(
        instance,
        "bodyProducer",
        ProducerProxy(instance.bodyProducer, report, REQUEST_STAGE),
    )
    return wrapped(*args, **kwargs)


class ReadProtocolProxy(wrapt.ObjectProxy):
    __report__ = None
    __stage__ = None

    def __init__(self, wrapped, report, stage):
        super(ReadProtocolProxy, self).__init__(wrapped)
        self.__report__ = report
        self.__stage__ = stage

    def dataReceived(self, data):
        self.__report__.response_body.write(data)
        return self.__wrapped__.dataReceived(data)

    def connectionLost(self, reason):
        self.__report__.stage_type = self.__stage__
        self.__report__.end_report("%r" % reason, reason)
        ResponseDone = getattr(
            importlib.import_module("twisted.web._newclient"), "ResponseDone"
        )
        if reason.check(ResponseDone):
            self.__report__.end_report()
        else:
            self.__report__.end_report("%r" % reason.value, reason.getErrorMessage())
        return self.__wrapped__.connectionLost(reason)


def new_client_response_construct_wrapper(wrapped, instance, args, kwargs):
    def _parse(_version, code, _phrase, hdrs, _transport, request):
        return code, hdrs, getattr(request, "_bearer_report", None)

    status, headers, report = _parse(*args, **kwargs)
    if report is None:
        return wrapped(*args, **kwargs)

    report.update(
        {"statusCode": status, "responseHeaders": (_process_headers, headers)},
        stage_type=RESPONSE_STAGE,
    )

    setattr(instance, "_bearer_report", report)
    return wrapped(*args, **kwargs)


def new_client_response_deliver_body_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report")

    def _protocol(proto):
        return proto

    protocol = _protocol(*args, **kwargs)
    if report is not None:
        protocol = ReadProtocolProxy(protocol, report, RESPONSE_STAGE)

    return wrapped(protocol)


def new_client_httpclientparser_finished_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance.request, "_bearer_report")
    if report is not None:
        report.end_report()
    return wrapped(*args, **kwargs)


def intercept(module):
    wrapt.wrap_function_wrapper(
        module, "Request._construct", new_client_request_construct_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module, "Request._writeHeaders", new_client_request_write_headers_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module, "Response._construct", new_client_response_construct_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module, "Response.deliverBody", new_client_response_deliver_body_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module,
        "HTTPClientParser._finished",
        new_client_httpclientparser_finished_wrapper,
    )
