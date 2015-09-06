# coding: utf-8

from oslo_config import cfg
from oslo_log import log
from oslo_db import options

CONF = cfg.CONF

_DEFAULT_PROJECT = "example"
_DEFAULT_SQL_CONNECTION = 'sqlite:///tmp/%s.sqlite' % _DEFAULT_PROJECT
_DEFAULT_LOG_LEVELS = ['root=INFO', '%s=INFO' % _DEFAULT_PROJECT]
_DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def parse_args(argv, project=None, default_config_files=None,
               default_log_format=None, default_log_levels=None,
               default_sql_conn=None):
    project = project if project else _DEFAULT_PROJECT
    log_fmt = default_log_format if default_log_format else _DEFAULT_LOG_FORMAT
    log_lvl = default_log_levels if default_log_levels else _DEFAULT_LOG_LEVELS
    sql_conn = default_sql_conn if default_sql_conn else _DEFAULT_SQL_CONNECTION

    log.set_defaults(log_fmt, log_lvl)
    log.register_options(CONF)
    options.set_defaults(CONF, connection=sql_conn, sqlite_db='%s.sqlite' % project)
    CONF(argv[1:], project=project, default_config_files=default_config_files)
