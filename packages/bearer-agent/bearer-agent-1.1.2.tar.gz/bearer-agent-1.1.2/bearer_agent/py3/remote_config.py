# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import traceback
from threading import Thread, Event
import logging

from .client import Client
from .errors import ClientStopped
from .config import ConfigUpdate

UPDATE_INTERVAL = 5


class ConfigFetcher(Thread):
    def __init__(self, cfg):
        super().__init__()
        self.daemon = True
        self.finished = Event()
        self.cfg = cfg
        self.client = Client(cfg, self.finished)
        self.logger = logging.getLogger("bearer")

    def stop(self):
        self.finished.set()

    def run(self):
        self._update_config()
        while True:
            self.finished.wait(UPDATE_INTERVAL)
            if not self.finished.is_set():
                self._update_config()
                continue
            return

    def _update_config(self):
        try:
            remote_cfg = self.client.fetch_config()
        except ClientStopped:
            pass

        # do update the configuration
        with ConfigUpdate(self.cfg):
            for key, val in remote_cfg.items():
                try:
                    if key == "dataCollectionRules":
                        self.cfg.set("data_collection_rules", val)
                    elif key == "rules":
                        self.cfg.set("rules", val)
                    elif key == "filters":
                        self.cfg.set("filters", val)
                except Exception:
                    self.logger.debug(traceback.format_exc())
                    self.logger.error("error fetching configuration")
                    pass
