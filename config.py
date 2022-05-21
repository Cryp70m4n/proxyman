#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class ProxymanConfig():
    def __init__(self):
        self.source_timeout = 2
        self.proxy_timeout = 5
        self.threads = 500
        self.db_path = "proxys.db"
        self.port = 4334

    @staticmethod
    def ParseConfig(config_path):
        f = open(config_path, "rb")
        s = json.load(f)

        pd = vars(ProxymanConfig())
        pd = pd | s

        p = ProxymanConfig()
        p.__dict__ = json.loads(json.dumps(pd))

        return p
