# coding: utf-8
import logging
import multiprocessing

import routes
import eventlet
from oslo_config import cfg
from oslo_log import log
from oslo_service import service
from oslo_service.wsgi import Router, Server

from bservices import wsgi

LOG = logging.getLogger()
CONF = cfg.CONF

cli_opts = [
    cfg.StrOpt("listen_ip", default='0.0.0.0'),
    cfg.IntOpt("listen_port", default=10000)
]
CONF.register_cli_opts(cli_opts)


class HelloController(wsgi.Controller):
    def hello(self, req):
        return "Hello"

    def data(self, req, body):
        LOG.info(body)


class API(Router):
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


class WSGIServer(Server, service.ServiceBase):
    pass


def main(project="example"):
    log.register_options(CONF)
    CONF(project=project)
    # log.set_defaults(default_log_levels=None)

    log.setup(CONF, project)
    eventlet.monkey_patch(all=True)

    server = WSGIServer(CONF, project, API(), host=CONF.listen_ip, port=CONF.listen_port,
                        use_ssl=False, max_url_len=1024)
    launcher = service.launch(CONF, server, workers=multiprocessing.cpu_count())
    launcher.wait()


if __name__ == '__main__':
    main()
