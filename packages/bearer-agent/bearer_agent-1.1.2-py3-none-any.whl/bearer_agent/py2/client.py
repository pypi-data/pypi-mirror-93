# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from __future__ import absolute_import

from bearer_agent import six

import logging
import json
import socket

import bearer_agent.six.moves.urllib.parse as urllib_parse

from .backoff import ExponentialBackoff
from .errors import ClientStopped
from .util import agent_env, encode_environment, runtime_env, json_loads

if six.PY2:
    import httplib as client
else:
    import http.client as client


class Client(object):
    CONFIG_PATH = "/config"
    REPORT_PATH = "/logs"

    def __init__(self, cfg, stop_ev):
        self.cfg = cfg
        self.stop_ev = stop_ev
        # we sleep max 5 secs, min 200ms and step by 200ms
        self.backoff = ExponentialBackoff(0.2, 5, 0.2)
        self.logger = logging.getLogger("bearer")
        self.active = True
        self.create_config_connection = create_connection_factory(cfg.config_host)
        self.create_report_connection = create_connection_factory(cfg.report_host)

    def fetch_config(self):
        headers = {
            "Authorization": self.cfg.secret_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        body = json.dumps(
            {
                "agent": agent_env(),
                "application": {
                    "environment": encode_environment(self.cfg.environment)
                },
                "runtime": runtime_env(),
            }
        )

        h = self.create_config_connection()
        h._bearer_disabled = True
        attempts = 1
        while True:
            if self.stop_ev.is_set():
                raise ClientStopped()

            try:
                h.request("POST", self.CONFIG_PATH, body=body, headers=headers)
                resp = h.getresponse()
                json_body = resp.read().decode()
                self.logger.debug("remote config received: %s", json_body)
                return json_loads(json_body)
            except (client.HTTPException, socket.error) as exc:
                self.logger.error("retrying fetching config: %s", str(exc))
                if self.stop_ev.wait(self.backoff.next(attempts)):
                    raise ClientStopped()
                attempts += 1
            finally:
                h.close()

    def send_report(self, report):
        headers = {
            "Authorization": self.cfg.secret_key,
            "Content-Type": "application/json",
        }
        attempts = 1
        while True:
            if self.stop_ev.is_set():
                break

            h = self.create_report_connection()
            h._bearer_disabled = True
            body = json.dumps(report)
            self.logger.debug("sending report: %s", body)

            try:
                h.request("POST", self.REPORT_PATH, body=body, headers=headers)
                resp = h.getresponse()
                json_body = resp.read().decode()
                return json_loads(json_body)
            except (client.HTTPException, socket.error) as exc:
                self.logger.error("retrying sending report: %s", str(exc))
                if self.stop_ev.wait(self.backoff.next(attempts)):
                    raise ClientStopped()
                attempts += 1
            finally:
                h.close()


def create_connection_factory(base_url):
    parsed_url = urllib_parse.urlparse(base_url)
    klass = client.HTTPSConnection if parsed_url.scheme.lower() == "https" else client.HTTPConnection
    host = parsed_url.hostname
    port = parsed_url.port

    def f():
        return klass(host, port=port)

    return f
