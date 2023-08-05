from . import six
from .headers import get_content_info

if six.PY3:
    from .py3 import bodies
else:
    from .py2 import bodies


def process(report):
    log = report.log

    req_headers, req_content_info = _process_headers(log.get("requestHeaders"))
    req_body, req_body_size = bodies.parse(log.get("requestBody"), req_content_info)

    res_headers, res_content_info = _process_headers(log.get("responseHeaders"))
    res_body, res_body_size = bodies.parse(log.get("responseBody"), res_content_info)

    report.request_body_size = req_body_size
    report.request_content_info = req_content_info
    report.response_body_size = res_body_size
    report.response_content_info = res_content_info

    log.update(
        {
            "requestHeaders": req_headers,
            "requestBody": req_body,
            "responseHeaders": res_headers,
            "responseBody": res_body,
            "instrumentation": {
                "requestBenchmark": float(report.ended_at - report.start_at),
                "responseContentLength": res_content_info.length,
                "processingBeforeThreadBenchmark": -1.0,
            },
        }
    )

    return report


def _process_headers(headers):
    if headers is None:
        return None, get_content_info(None)

    if isinstance(headers, tuple):
        fun, data = headers
        headers = fun(data)

    return headers, get_content_info(headers)
