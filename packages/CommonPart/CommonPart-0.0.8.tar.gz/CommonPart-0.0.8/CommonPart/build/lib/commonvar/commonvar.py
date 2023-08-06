# coding:utf8

"""
常量名定义
"""


class CommonDB:
    """数据库配置文件定义"""
    db = "db"
    host = "host"
    port = "port"
    dbname = "dbname"
    user = "user"
    password = "password"
    charset = "charset"
    decode_responses = "decode_responses"
    max_connections = "max_connections"
    con = "con"

    """数据库操作信息定义"""
    table_name = "tablename"


class CommonVar:
    trytimes = "trytimes"  # 发送请求失败重试次数
    ifproxy = "ifproxy"  # 代理状态
    proxy = "proxy"  # 代理参数
    proxies = "proxies"
    m_h5_tk = "_m_h5_tk"
    m_h5_tk_enc = "_m_h5_tk_enc"
    ok = "ok"
    data = "data"
    text = "text"
    reply_text = "reply_text"
    card_type = "card_type"
    created_at = "created_at"
    comments_count = "comments_count"
    cards = "cards"
    tcn = "t.cn"
    origin_url = "http://t.cn/{}"
    status = "status"
    join_groups = "join_groups"
    group_id = "id"
    name = "name"
    result = "result"


class ProxyUnit:
    URL = "https://proxypool.io.mlj162.com/proxy/getitem/wbgroupdata"
