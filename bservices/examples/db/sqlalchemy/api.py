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
oslo_db_options.set_defaults(CONF, connection="sqlite:///:memory:")
DB_INIT = False

LOG = logging.getLogger(__name__)


def get_backend():
    """The backend is this module itself."""
    global DB_INIT
    if not DB_INIT:
        models.TestData.metadata.create_all(get_engine(CONF.database))
        DB_INIT = True
    return sys.modules[__name__]


###########################################################
# API Interface
def get_data(_id):
    """获取指定ID的数据"""
    model = models.TestData
    session = get_session(CONF.database)
    query = sqlalchemyutils.model_query(model, session)
    obj = query.filter_by(id=_id).first()
    if obj:
        return {
            "id": obj.id,
            "data": obj.data
        }
    else:
        return None


def set_data(data):
    """新增数据"""
    model = models.TestData
    session = get_session(CONF.database)
    obj = model(data=data)
    obj.save(session)
    return {
        "id": obj.id,
    }


def update_data(_id, new_data):
    """更新指定ID的数据"""
    model = models.TestData
    session = get_session(CONF.database)
    obj = session.query(model).filter_by(id=_id).first()
    if not obj:
        return False
    obj.data = new_data
    session.flush()
    return {
        "id": obj.id,
        "data": obj.data,
        "update_time": obj.update_time.isoformat()
    }

def delete_data(_id):
    """删除指定ID的数据"""
    model = models.TestData
    session = get_session(CONF.database)
    obj = session.query(model).filter_by(id=_id).first()
    if not obj:
        return False
    session.delete(obj)
    session.flush()
    return True
