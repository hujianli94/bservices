# coding: utf-8

from oslo_config import cfg
from oslo_db import concurrency
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
_BACKEND_MAPPING = {'sqlalchemy': "bservices.examples.db.sqlalchemy.api"}

IMPL = concurrency.TpoolDbapiWrapper(CONF, backend_mapping=_BACKEND_MAPPING)


####################################
# API Interface
def get_data(id):
    """获取指定ID的数据"""
    return IMPL.get_data(id)


def set_data(data):
    """新增数据"""
    return IMPL.set_data(data)


def update_data(id, new_data):
    """更新指定ID的数据"""
    return IMPL.update_data(id, new_data)

def delete_data(id):
    """删除指定ID的数据"""
    return IMPL.delete_data(id)
