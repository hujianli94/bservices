# coding: utf-8

import sys

import routes
import eventlet
from oslo_config import cfg
from oslo_log import log as logging

from bservices import config
from bservices import service
from bservices import wsgi

LOG = logging.getLogger()
CONF = cfg.CONF

PROJECT = "example"

cli_opts = [
    cfg.StrOpt("%s_listen" % PROJECT, default='0.0.0.0'),
    cfg.IntOpt("%s_listen_port" % PROJECT, default=10000)
]
CONF.register_cli_opts(cli_opts)


class HelloController(wsgi.Controller):
    def hello(self, req):
        return "Hello"

    def data(self, req, body):
        LOG.info(body)


class API(wsgi.Router):
    def __init__(self):
        mapper = routes.Mapper()
        mapper.redirect("", "/")

        resource = wsgi.Resource(HelloController())
        mapper.connect("/hello",
                       controller=resource,
                       action="hello",
                       conditions={"method": ['GET']})
        mapper.connect("/data",
                       controller=resource,
                       action="data",
                       conditions={"method": ["POST"]})

        super(API, self).__init__(mapper)


class Loader(object):
    def load_app(self, name):
        return API()


def main():
    config.parse_args(sys.argv, PROJECT)
    logging.setup(CONF, PROJECT)
    eventlet.monkey_patch(all=True)

    server = service.WSGIService(PROJECT, Loader(), use_ssl=False, max_url_len=16384)
    service.serve(server, workers=server.workers)
    service.wait()


if __name__ == '__main__':
    main()
