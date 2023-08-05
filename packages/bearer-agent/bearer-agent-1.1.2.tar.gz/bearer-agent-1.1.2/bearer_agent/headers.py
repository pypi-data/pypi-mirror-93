from collections import namedtuple

import re


NON_BINARY_RE = re.compile("json|text|xml|x-www-form-urlencoded", re.I)
JSON_RE = re.compile("^application/json", re.I)
FORM_RE = re.compile("^application/x-www-form-urlencoded", re.I)


class ContentType(object):
    PLAIN = 0
    JSON = 1
    FORM = 2
    BINARY = 3


ContentInfo = namedtuple("ContentInfo", ["ctype", "encoding", "length"])


def get_content_info(headers):
    if headers is None:
        return ContentInfo(ctype=None, encoding=None, length=None)

    ctype = None
    encoding = None
    length = None

    for key, value in headers.items():
        canonical_key = key.upper()

        if canonical_key == "CONTENT-TYPE":
            if JSON_RE.search(value):
                ctype = ContentType.JSON
            elif FORM_RE.search(value):
                ctype = ContentType.FORM
            elif NON_BINARY_RE.search(value):
                ctype = ContentType.PLAIN
            else:
                ctype = ContentType.BINARY
        elif canonical_key == "CONTENT-ENCODING":
            encoding = value
        elif canonical_key == "CONTENT-LENGTH":
            length = int(value)

    return ContentInfo(ctype=ctype, encoding=encoding, length=length)
