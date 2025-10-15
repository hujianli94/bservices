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
import multiprocessing

from oslo_log import log
from oslo_service import service

from bservices.config import CONF
from bservices.contrib.server import WSGIServer
from bservices.examples.wsgi_server_example import API

LOG = logging.getLogger(__name__)


def main():
    log.register_options(CONF)
    CONF(project='bservices', prog='bservices-wsgi')
    log.setup(CONF, 'bservices')

    server = WSGIServer(
        CONF,
        'bservices-wsgi',
        API(),
        host=CONF.wsgi_listen_ip,
        port=CONF.wsgi_listen_port,
        use_ssl=False
    )
    launcher = service.launch(
        CONF,
        server,
        workers=CONF.wsgi_workers or multiprocessing.cpu_count()
    )
    launcher.wait()
