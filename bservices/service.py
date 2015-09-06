# coding: utf-8

from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service
from oslo_concurrency import processutils

from . import wsgi_base as wsgi
from .i18n import _

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class WSGIService(service.Service):
    """Provides ability to launch API from a 'paste' configuration."""

    def __init__(self, name, loader=None, use_ssl=False, max_url_len=None):
        """Initialize, but do not start the WSGI server.
        :param name: The name of the WSGI server given to the loader.
        :param loader: Loads the WSGI application using the given name.
        :returns: None
        """
        self.name = name
        self.loader = loader or wsgi.Loader()
        self.app = self.loader.load_app(name)

        wname = self.name
        self.host = getattr(CONF, '%s_listen' % name, "0.0.0.0")
        self.port = getattr(CONF, '%s_listen_port' % name, 0)
        self.workers = (getattr(CONF, '%s_workers' % wname, None) or
                        processutils.get_worker_count())
        if self.workers and self.workers < 1:
            worker_name = '%s_workers' % name
            msg = (_("%(worker_name)s value of %(workers)s is invalid, "
                     "must be greater than 0") %
                   {'worker_name': worker_name,
                    'workers': str(self.workers)})
            # raise exception.InvalidInput(msg)
            raise Exception(msg)
        self.use_ssl = use_ssl
        self.server = wsgi.Server(name,
                                  self.app,
                                  host=self.host,
                                  port=self.port,
                                  use_ssl=self.use_ssl,
                                  max_url_len=max_url_len)
        # Pull back actual port used
        self.port = self.server.port
        self.backdoor_port = None

    def reset(self):
        """Reset server greenpool size to default.
        :returns: None
        """
        self.server.reset()

    def start(self):
        """Start serving this service using loaded configuration.
        :returns: None
        """
        self.server.start()

    def stop(self):
        """Stop serving this API.
        :returns: None
        """
        self.server.stop()

    def wait(self):
        """Wait for the service to stop serving this API.
        :returns: None
        """
        self.server.wait()


def process_launcher():
    return service.ProcessLauncher(CONF)


# NOTE(vish): the global launcher is to maintain the existing
#             functionality of calling service.serve +
#             service.wait
_launcher = None


def serve(server, workers=None):
    global _launcher
    if _launcher:
        raise RuntimeError(_('serve() can only be called once'))

    _launcher = service.launch(CONF, server, workers=workers)


def wait():
    _launcher.wait()
