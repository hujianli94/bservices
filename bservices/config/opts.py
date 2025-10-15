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
from oslo_config import cfg

wsgi_group = cfg.OptGroup(
    name='wsgi',
    title='WSGI Server Options',
    help='Configuration options for WSGI Server')

wsgi_opts = [
    cfg.StrOpt(
        'listen_ip',
        default='0.0.0.0',
        help='IP address on which the WSGI server will listen.'),
    cfg.PortOpt(
        'listen_port',
        default=10000,
        help='Port on which the WSGI server will listen.'),
    cfg.IntOpt(
        'workers',
        min=1,
        help='Number of workers for WSGI server. Default is CPU count.'),
    cfg.BoolOpt(
        'use_ssl',
        default=False,
        help='Enable SSL for WSGI server.')
]

tcp_group = cfg.OptGroup(
    name='tcp',
    title='TCP Server Options',
    help='Configuration options for TCP Server')

tcp_opts = [
    cfg.StrOpt(
        'listen_ip',
        default='0.0.0.0',
        help='IP address on which the TCP server will listen.'),
    cfg.PortOpt(
        'listen_port',
        default=10001,
        help='Port on which the TCP server will listen.'),
    cfg.IntOpt(
        'pool_size',
        default=1024,
        min=1,
        help='Connection pool size for TCP server.')
]

pool_group = cfg.OptGroup(
    name='pool',
    title='Pool Server Options',
    help='Configuration options for Pool Server')

pool_opts = [
    cfg.IntOpt(
        'size',
        default=100,
        min=1,
        help='Worker pool size for Pool server.'),
    cfg.IntOpt(
        'interval',
        default=10,
        min=1,
        help='Task scheduling interval in seconds.')
]

task_group = cfg.OptGroup(
    name='task',
    title='Task Server Options',
    help='Configuration options for Task Server')

task_opts = [
    cfg.IntOpt(
        'num',
        default=10,
        min=1,
        help='Number of persistent tasks.'),
    cfg.IntOpt(
        'interval',
        default=10,
        min=1,
        help='Task execution interval in seconds.'),
    cfg.IntOpt(
        'spare',
        default=3,
        min=0,
        help='Number of spare task workers for burst handling.')
]

ALL_OPTS = (wsgi_opts + tcp_opts + pool_opts + task_opts)
ALL_GROUPS = (wsgi_group, tcp_group, pool_group, task_group)


def register_opts(conf):
    for group in ALL_GROUPS:
        conf.register_group(group)
        conf.register_opts(_get_opts_for_group(group.name), group=group)


def _get_opts_for_group(group_name):
    return {
        'wsgi': wsgi_opts,
        'tcp': tcp_opts,
        'pool': pool_opts,
        'task': task_opts
    }[group_name]


def list_opts():
    return [(group.name, _get_opts_for_group(group.name))
            for group in ALL_GROUPS]
