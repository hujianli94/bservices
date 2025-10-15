#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2025 bservices Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import eventlet

eventlet.monkey_patch(all=True)

import logging
import time

from oslo_log import log
from oslo_service import service

from bservices.config import CONF
from bservices.contrib.server import PoolServer

LOG = logging.getLogger(__name__)


def pool_task(i):
    LOG.info(f"Processing task {i}")
    time.sleep(1)


def pool_handler(pool, interval):
    while True:
        for i in range(100):
            pool.spawn_n(pool_task, i)
        time.sleep(interval)


def main():
    log.register_options(CONF)
    CONF(project='bservices', prog='bservices-pool')
    log.setup(CONF, 'bservices')

    server = PoolServer(
        pool_handler,
        interval=CONF.pool_interval,
        pool_size=CONF.pool_size
    )
    launcher = service.launch(CONF, server)
    launcher.wait()
