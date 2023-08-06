# encodin：utf-8
"""
redis操作模块
Author:afcentry
Date:2021-01-22
"""
import sys
import redis
from CommonPart.commonvar.commonvar import CommonVar, CommonDB


class OPRedis:

    @staticmethod
    def redis_pool(**kwargs):
        """
        :param kwargs: db host port user passwd
        :return: 返回redis链接
        """
        connection_pool = None
        try:
            connection_pool = redis.ConnectionPool(**kwargs)
        except ConnectionError:
            assert ConnectionError(f"failed connect to redis:{kwargs.get(CommonDB.db)}")
            sys.exit()
        finally:
            return connection_pool

    @staticmethod
    def redis_con(connection_pool):
        """
        :param connection_pool: redis连接池
        :return: 单一redis连接
        """
        conn = redis.Redis(connection_pool=connection_pool)
        return conn
