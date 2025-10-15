# coding: utf-8

"""
# 以守护进程模式启动
python -m bservices.examples.wsgi_server_daemon --daemonize

# 查看进程（确认后台运行）
ps -ef | grep wsgi_server_daemon


注意事项:
- 日志配置：必须在 daemon() 调用前初始化日志(如 log.setup)，否则日志会被重定向到 /dev/null。
- 文件描述符：若需保留日志文件描述符，可设置 keep_fds_open=True 并手动管理文件句柄。
- 进程管理：守护进程模式下，建议配合 systemd 等工具管理启停，避免直接 kill 导致资源泄漏。
"""
import logging
import multiprocessing

import eventlet
from oslo_config import cfg
from oslo_log import log
from oslo_service import service

from bservices import wsgi, exception
from bservices.contrib.server import WSGIServer
from bservices.contrib.daemon import daemon  # 导入daemon函数
from bservices.examples.db import api

LOG = logging.getLogger()
CONF = cfg.CONF

cli_opts = [
    cfg.StrOpt("listen_ip", default='0.0.0.0'),
    cfg.IntOpt("listen_port", default=10000),
    cfg.BoolOpt("daemonize", default=False, help="是否以守护进程运行")
]
CONF.register_cli_opts(cli_opts)


class DataController(wsgi.Controller):
    @wsgi.serializers(json=wsgi.JSONDictSerializer)
    @wsgi.deserializers(json=wsgi.JSONDeserializer)
    @wsgi.response(200)
    @wsgi.action("index")
    def get_data(self, req):
        try:
            id = int(req.GET["id"])
        except (KeyError, TypeError, ValueError):
            raise exception.BadRequest()

        ret = api.get_data(id)
        if not ret:
            raise exception.NotFound()
        return ret

    def set_data(self, req, body):
        try:
            data = body["data"]
        except (KeyError, TypeError, ValueError):
            raise exception.BadRequest()

        return api.set_data(data)

    @wsgi.serializers(json=wsgi.JSONDictSerializer)
    @wsgi.deserializers(json=wsgi.JSONDeserializer)
    @wsgi.response(200)
    def update_data(self, req, body):
        """更新数据(PUT /update_data)"""
        try:
            data_id = int(body["id"])
            new_data = body["data"]
        except (KeyError, TypeError, ValueError):
            raise exception.BadRequest()

        ret = api.update_data(data_id, new_data)
        if not ret:
            raise exception.NotFound()
        return ret

    @wsgi.response(204)  # 204表示成功无返回体
    def delete_data(self, req):
        """删除数据(DELETE /delete_data)"""
        try:
            data_id = int(req.GET["id"])
        except (KeyError, TypeError, ValueError):
            raise exception.BadRequest()

        if not api.delete_data(data_id):
            raise exception.NotFound()
        return None


class API(Router):
    def __init__(self):
        mapper = routes.Mapper()
        mapper.redirect("", "/")

        resource = wsgi.Resource(DataController())
        mapper.connect("/get_data",
                       controller=resource,
                       action="get_data",
                       conditions={"method": ['GET']})
        mapper.connect("/set_data",
                       controller=resource,
                       action="set_data",
                       conditions={"method": ["POST"]})
        mapper.connect("/update_data",
                       controller=resource,
                       action="update_data",
                       conditions={"method": ["PUT"]})
        mapper.connect("/delete_data",
                       controller=resource,
                       action="delete_data",
                       conditions={"method": ["DELETE"]})

        super(API, self).__init__(mapper)


def main(project="wsgi_server_daemon"):
    log.register_options(CONF)
    CONF(project=project)  # 解析命令行参数
    log.setup(CONF, project)  # 初始化日志（需在daemon前，否则日志可能被重定向）

    eventlet.monkey_patch(all=True)

    # 如果启用守护进程模式，调用daemon()
    if CONF.daemonize:
        daemon(
            umask=0o07,          # 文件权限掩码（默认0o07）
            workdir="/",         # 工作目录（默认/）
            keep_fds_open=False, # 不保留额外文件描述符
            stdio=False          # 重定向标准IO到/dev/null
        )

    # 启动WSGI服务
    server = WSGIServer(
        CONF, project, API(),
        host=CONF.listen_ip,
        port=CONF.listen_port,
        use_ssl=False
    )
    launcher = service.launch(
        CONF, server,
        workers=multiprocessing.cpu_count()  # 按CPU核心数启动工作进程
    )
    launcher.wait()


if __name__ == '__main__':
    main()
