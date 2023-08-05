# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import urllib.parse

from . import bodies, shape_hash
from ..headers import ContentType

FILTERED = "[FILTERED]"


class Sanitizer(object):
    PAYLOAD_HASH_NOT_APPLICABLE = "N/A"

    def __init__(self, cfg):
        self.strip_sensitive_regex = cfg.strip_sensitive_regex
        self.strip_sensitive_keys = cfg.strip_sensitive_keys

    def _is_filtered_key(self, key):
        if self.strip_sensitive_keys and self.strip_sensitive_keys.match(key):
            return True

        return False

    def _sanitize_string(self, value):
        if self.strip_sensitive_regex:
            return self.strip_sensitive_regex.sub(FILTERED, value)
        return value

    def _sanitize_dict(self, d):
        ret = {}
        for key, value in d.items():
            if self._is_filtered_key(key):
                ret[key] = FILTERED
                continue

            ret[key] = self._sanitize_value(value)
        return ret

    def _sanitize_value(self, value):
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        elif isinstance(value, dict):
            return self._sanitize_dict(value)
        elif isinstance(value, str):
            return self._sanitize_string(value)
        return value

    def _process_body(self, body, content_type):
        payload_hash = self.PAYLOAD_HASH_NOT_APPLICABLE
        if (
            content_type == ContentType.JSON
            and body is not None
            and not isinstance(body, str)
        ):
            payload_hash = shape_hash.to_sha(body)

        body_str = bodies.to_str(self._sanitize_value(body), content_type)
        return body_str, payload_hash

    def _process_url(self, log):
        hostname = log["hostname"]
        port = log["port"]
        protocol = log["protocol"]

        include_port = (protocol == "https" and port != 443) or (
            protocol == "http" and port != 80
        )
        port_str = ":{port}".format(port=port) if include_port else ""

        path = "/".join(
            urllib.parse.quote(self._sanitize_value(urllib.parse.unquote(segment)))
            for segment in log["path"].split()
        )

        params = self._sanitize_value(log.get("params"))
        params_str = (
            "?{encoded_params}".format(encoded_params=urllib.parse.urlencode(params, doseq=True))
            if params and len(params) != 0
            else ""
        )

        url = "{protocol}://{hostname}{port_str}{path}{params_str}".format(
            protocol=protocol,
            hostname=hostname,
            port_str=port_str,
            path=path,
            params_str=params_str,
        )

        log.update({"url": url, "params": params, "path": path})

    def run(self, report):
        log = report.log
        self._process_url(log)

        request_headers = self._sanitize_value(log["requestHeaders"])
        request_body, request_body_hash = self._process_body(
            log["requestBody"], report.request_content_info.ctype
        )

        response_headers = self._sanitize_value(log["responseHeaders"])
        response_body, response_body_hash = self._process_body(
            log["responseBody"], report.response_content_info.ctype
        )

        log.update(
            {
                "requestHeaders": request_headers,
                "requestBody": request_body,
                "requestBodyPayloadSha": request_body_hash,
                "responseHeaders": response_headers,
                "responseBody": response_body,
                "responseBodyPayloadSha": response_body_hash,
            }
        )

        # This is redundant info so avoid sending it
        if "params" in log:
            del log["params"]

        return log
