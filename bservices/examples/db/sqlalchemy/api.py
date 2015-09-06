# coding: utf-8
import sys

from oslo_config import cfg
from oslo_db import options as oslo_db_options
from oslo_db.sqlalchemy import utils as sqlalchemyutils
from oslo_log import log as logging

from bservices.db.sqlalchemy import get_engine, get_session

from . import models

CONF = cfg.CONF
CONF.register_opts(oslo_db_options.database_opts, 'database')
CONF.register_opts(oslo_db_options.database_opts, 'api_database')

LOG = logging.getLogger(__name__)


def get_backend():
    """The backend is this module itself."""
    # return APIInterface()
    return sys.modules[__name__]


###########################################################
# API Interface
def get_user_info(username):
    model = models.UserInfo
    session = get_session(CONF.database)
    #api_session = get_session(CONF.api_database)
    query = sqlalchemyutils.model_query(model, session)
    return query.filter_by(username=username)


class APIInterface(object):
    def __init__(self):
        self._engine = get_engine()
        self._session = get_session()
        self._api_engine = get_api_engine(CONF.api_database)
        self._api_session = get_api_session(CONF.api_database)

    def get_user_info(self, username):
            model = models.UserInfo
            query = sqlalchemyutils.model_query(model, self._session)
            return query.filter_by(username=username)
