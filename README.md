# bservices

## 简介
bservices 是一个基于 oslo.service 和 eventlet 构建的服务库，提供四种类型的 Server（WSGI Server、TCP Server、Pool Server、Task Server），适用于不同业务场景，遵循 OpenStack 项目开发规范和最佳实践。

## 特性
- 基于 OpenStack oslo.service 框架，兼容 OpenStack 服务启动方式
- 四种 Server 类型满足不同业务需求：
  - WSGI Server：处理 WSGI 请求，支持 RESTful API 开发
  - TCP Server：处理原始 TCP 连接，支持自定义协议通信
  - Pool Server：基于绿色线程池的任务调度器，适合批量异步任务
  - Task Server：专注于长期运行的后台任务，支持任务数量控制
- 支持守护进程模式运行，适合生产环境部署
- 完善的日志配置和错误处理
- 遵循 OpenStack 项目目录结构和配置规范

## 目录结构
```shell
bservices/
├── bservices/
│   ├── cmd/              # 命令行入口
│   ├── config/           # 配置相关
│   │   ├── __init__.py
│   │   └── opts.py       # 配置选项定义
│   ├── contrib/          # 扩展组件
│   │   ├── server.py     # Server 实现
│   │   └── daemon.py     # 守护进程支持
│   ├── examples/         # 示例代码
│   ├── wsgi.py           # WSGI 相关实现
│   └── __init__.py
├── setup.cfg             # 项目配置
├── setup.py              # 安装脚本
└── README.md             # 项目说明
```

## 安装
```bash
git clone https://github.com/xgfone/bservices.git
cd bservices
pip install -e .
```

## 使用

```shell
# WSGI Server
bservices-wsgi --config-file /path/to/bservices.conf
# 守护进程模式
bservices-wsgi --daemonize --config-file /path/to/bservices.conf

# TCP Server
bservices-tcp

# Pool Server
bservices-pool

# Task Server
bservices-task
```