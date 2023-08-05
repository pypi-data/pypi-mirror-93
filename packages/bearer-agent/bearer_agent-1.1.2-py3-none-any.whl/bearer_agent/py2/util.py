# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from bearer_agent import six

import io
import time
import re
import base64
import platform
import json

import wrapt

from ..version import __version__


def reraise(tp, value, tb=None):
    six.reraise(tp, value, tb)


def classname(obj):
    return type(obj).__name__


def current_time():
    return int(round(time.time() * 1000))


def flag(flag_str):
    flags = 0

    if not flag_str:
        return flags

    for flag in flag_str:
        attr_name = flag.upper()
        if not hasattr(re, attr_name):
            raise ValueError("invalid flag %s" % flag)
        flags = flags | getattr(re, attr_name)

    return flags


def _is_text_io(stream):
    """Test whether a file-like object is a text or a binary stream.
    """
    return isinstance(stream, io.TextIOBase)


def encode_environment(environment):
    if environment is None:
        return None
    return six.ensure_text(base64.b64encode(six.ensure_binary(environment)))


def runtime_env():
    return {
        "arch": platform.machine(),
        "hostname": platform.node() or "unknown",
        "type": platform.system(),
        "platform": platform.platform(),
        "version": platform.python_version(),
    }


def agent_env():
    return {"type": "python", "version": __version__}


class ReadProxy(wrapt.ObjectProxy):

    __target__ = None

    def __init__(self, wrapped, target):
        super(ReadProxy, self).__init__(wrapped)
        self.__encode = _is_text_io(wrapped)
        self.__target__ = target

    def read(self, amt=None):
        data = self.__wrapped__.read(amt)
        if self.__encode:
            self.__target__.write(data.encode("utf-8"))
        else:
            six.ensure_binary(data)
        return data


class BufferProxy(wrapt.ObjectProxy):

    __target__ = None

    def __init__(self, wrapped, target):
        super(BufferProxy, self).__init__(wrapped)
        self.__target__ = target

    def __iter__(self):
        it = iter(self.__wrapped__)
        for chunk in it:
            self.__target__.write(six.ensure_binary(chunk))
            yield chunk


def _byteify(data):
    # if this is a unicode string, return its string representation
    if isinstance(data, six.string_types):
        return str(data.encode("utf-8").decode())

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item) for item in data]

    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict):
        return {_byteify(key): _byteify(value) for key, value in six.iteritems(data)}
    # if it's anything else, return it in its original form
    return data


def json_loads(jsonval):
    return json.loads(jsonval, object_hook=_byteify)
