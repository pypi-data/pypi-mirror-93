# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import logging

from .config import DynamicConfig


class Matcher(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger("bearer")

    def run(self, report):
        filters = self.cfg.filters
        active_data_collection_rules = []
        active_rules = []
        config = {}

        def add_rule(collection, rule):
            collection.append(rule.summary)
            if hasattr(rule, "config"):
                config.update(rule.config)

        for rule in self.cfg.data_collection_rules:
            if rule.filter_hash is None:
                add_rule(active_data_collection_rules, rule)
                continue

            filter_ = filters.get(rule.filter_hash, None)
            if filter_ is None:
                self.logger.debug(
                    "ignoring rule with unknown filter hash %s", rule.filter_hash
                )
                continue

            matches = filter_.match(report, filters)
            self.logger.debug("filter %s match=%s", rule.filter_hash, matches)
            if matches:
                add_rule(active_data_collection_rules, rule)

        for rule in self.cfg.rules:
            if rule.filter_hash is None:
                add_rule(active_rules, rule)
                continue

            filter_ = filters.get(rule.filter_hash, None)
            if filter_ is None:
                self.logger.debug(
                    "ignoring rule with unknown filter hash %s", rule.filter_hash
                )
                continue

            matches = filter_.match(report, filters)
            self.logger.debug("filter %s match=%s", rule.filter_hash, matches)
            if matches:
                add_rule(active_rules, rule)

        return Result(active_rules, active_data_collection_rules, DynamicConfig(self.cfg, config))


class Result:
    def __init__(self, active_rules, active_data_collection_rules, config):
        self.active_rules = active_rules
        self.active_data_collection_rules = active_data_collection_rules
        self.config = config
