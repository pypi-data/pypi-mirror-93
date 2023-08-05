import zlib
import json
import urllib.parse

from urllib3.response import MultiDecoder

from ..headers import ContentType
from .util import json_loads


MAX_BODY_SIZE = 1024 * 1024  # 1mb

DECODER_ERROR_CLASSES = (IOError, zlib.error)


def parse(raw_body, content_info):
    if raw_body is None and content_info.ctype is None:
        return None, None

    body_bytes = _decode(raw_body, content_info.encoding)

    size = len(body_bytes)
    if size == 0:
        return "(no body)", 0
    elif size > MAX_BODY_SIZE:
        return "(omitted due to size)", size

    try:
        decoded_body = body_bytes.decode()
    except UnicodeDecodeError:
        return "(could not decode body)", size

    body = _parse_decoded(decoded_body, content_info.ctype)

    return body, size


def to_str(body, content_type):
    if isinstance(body, str):
        return body
    elif content_type == ContentType.JSON:
        return json.dumps(body)
    elif content_type == ContentType.FORM:
        return urllib.parse.urlencode(body, doseq=True)

    return body


def _decode(raw_body, content_encoding):
    if raw_body is None:
        return b""

    if content_encoding is None:
        return raw_body.getvalue()

    decoder = MultiDecoder(content_encoding)

    try:
        return decoder.decompress(raw_body.getvalue())
    except DECODER_ERROR_CLASSES:
        return raw_body.getvalue()


def _parse_decoded(decoded_body, content_type):
    if content_type == ContentType.JSON:
        try:
            return json_loads(decoded_body)
        except json.JSONDecodeError:
            pass
    elif content_type == ContentType.FORM:
        try:
            return urllib.parse.parse_qs(decoded_body)
        except (ValueError, TypeError):
            pass
    elif content_type == ContentType.BINARY:
        return "(not showing binary data)"

    return decoded_body
