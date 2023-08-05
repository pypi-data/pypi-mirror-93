# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from io import BytesIO

from .agent import enqueue_report
from .util import current_time


CONNECT_STAGE = "ConnectStage"
INIT_REQUEST_STAGE = "InitRequestStage"
REQUEST_STAGE = "RequestStage"
INIT_RESPONSE_STAGE = "InitResponseStage"  # Internal Python-only stage
RESPONSE_STAGE = "ResponseStage"
BODIES_STAGE = "BodiesStage"


REQUEST_END = "REQUEST_END"
REQUEST_ERROR = "REQUEST_ERROR"

_STATE_ACTIVE = 0
_STATE_ENQUEUED = 1


LOG_TEMPLATE = {
    "port": 0,
    "protocol": None,
    "hostname": "",
    "path": "",
    "method": "",
    "url": "",
    "requestHeaders": {},
    "responseHeaders": {},
    "statusCode": None,
    "requestBody": None,
    "responseBody": None,
    "errorCode": None,
    "errorFullMessage": None,
}


class ReportLog(object):
    def __init__(self):
        self.log = LOG_TEMPLATE.copy()
        self.duration = None
        self.request_content_type = None
        self.request_content_encoding = None
        self.request_body = BytesIO()
        self.request_body_size = None
        self.response_content_type = None
        self.response_content_encoding = None
        self.response_body = BytesIO()
        self.response_body_size = None
        self.start_at = current_time()
        self.ended_at = self.start_at
        self.disabled = False
        self.stage_type = CONNECT_STAGE
        self.state = _STATE_ACTIVE
        self.response_proxy = False

    @property
    def protocol(self):
        return self.log["protocol"]

    @protocol.setter
    def protocol(self, value):
        self.log["protocol"] = value

    def update(self, attrs, stage_type=None):
        self.log.update(attrs)
        if stage_type is not None:
            self.stage_type = stage_type

    @property
    def is_error(self):
        return self.log.get("type") == REQUEST_ERROR

    def end_report(self, error_code=None, error_msg=None):
        if self.state == _STATE_ENQUEUED:
            return

        report_type = REQUEST_END
        self.ended_at = current_time()
        self.duration = self.ended_at - self.start_at

        # This stage is only used internally to avoid double calls due to
        # response handling needing to come after the wrapped call
        if self.stage_type == INIT_RESPONSE_STAGE:
            self.stage_type = REQUEST_STAGE

        if error_code:
            report_type = REQUEST_ERROR
            self.log.update({"errorCode": error_code, "errorFullMessage": error_msg})
        else:
            self.stage_type = BODIES_STAGE

        self.log.update(
            {
                "stageType": self.stage_type,
                "startedAt": self.start_at,
                "endedAt": self.ended_at,
                "requestBody": self.request_body,
                "responseBody": self.response_body,
                "type": report_type
            }
        )

        self.state = _STATE_ENQUEUED
        enqueue_report(self)
