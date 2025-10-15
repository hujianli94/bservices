from oslo_config import cfg

from bservices.config.opts import register_opts

CONF = cfg.CONF
register_opts(CONF)