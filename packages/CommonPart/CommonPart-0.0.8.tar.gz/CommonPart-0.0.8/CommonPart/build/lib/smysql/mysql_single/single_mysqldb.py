# coding:utf8
"""
MySQL单线程数据库操作模板
"""
import pymysql

from CommonPart.smysql.config import databases
from CommonPart.combuiltin import ComBuiltin


class DBCon:
    """
    数据库连接操作
    获取
    检查
    重连
    """

    def __init__(self):
        self.dbcon = None

    @staticmethod
    def get_con(host, port, dbname, user, password, charset='utf8mb4'):
        dbcon = None
        try:
            dbcon = pymysql.connect(host=host,
                                    port=port,
                                    db=dbname,
                                    user=user,
                                    password=password,
                                    charset=charset,
                                    autocommit=True
                                    )  # 自动提交更改
            return True, dbcon
        except Exception as e:
            print("[{}]数据库{}连接失败-{}.".format(ComBuiltin.get_current_time(),
                                             databases["db"]["host"], str(e)))
            return False, dbcon

    def check_con(self):
        pass


class DBOperate:
    """
    数据库表数据操作接口提供
    """

    @staticmethod
    def insert_one(con=None, table_name=None, **kwargs):
        """
        数据库单条数据插入
        :param kwargs: con 数据库连接  table_name 操作表名 kwargs 存储键值
        :return: 数据插入状态 True False
        """
        insert_sql = "insert into {} set ".format(table_name)
        area_sql = ""
        for key, value in kwargs.items():
            if isinstance(value, int) or isinstance(value, float):
                if area_sql:
                    area_sql += "," + key + "={}".format(value)
                else:
                    area_sql += key + "={}".format(value)
            else:
                if area_sql:
                    area_sql += "," + key + "='{}'".format(value)
                else:
                    area_sql += key + "='{}'".format(value)
        insert_sql += area_sql
        print(insert_sql)
        cur = con.cursor()
        try:
            cur.execute(insert_sql)
        except Exception as e:
            print("[{}]数据插入失败.{}".format(ComBuiltin.get_current_time(), e))
        finally:
            cur.close()

    @staticmethod
    def select_all(con=None, table_name=None):
        select_sql = "select * from {}".format(table_name)
        cur = con.cursor()
        data = None
        try:
            cur.execute(select_sql)
            data = cur.fetchall()
        except Exception as e:
            pass
        finally:
            cur.close()
            return list(data)

    @staticmethod
    def selectWithCondition(con=None, table_name=None, queryField=None, **kwargs):
        fieldinfo = ""
        if queryField:
            for field in queryField:
                if fieldinfo:
                    fieldinfo += "," + field
                else:
                    fieldinfo = field
        else:
            fieldinfo = "*"

        area_sql = ""
        for key, value in kwargs.items():
            if isinstance(value, int) or isinstance(value, float):
                if area_sql:
                    area_sql += "and" + key + "={}".format(value)
                else:
                    area_sql += key + "={}".format(value)
            else:
                if area_sql:
                    area_sql += "and" + key + "='{}'".format(value)
                else:
                    area_sql += key + "='{}'".format(value)
        select_sql = "select {} from {} where {}".format(fieldinfo, table_name, area_sql)
        cur = con.cursor()
        try:
            cur.execute(select_sql)
        except Exception as e:
            print("[{}]数据查询失败.{}".format(ComBuiltin.get_current_time(), e))
        finally:
            cur.close()
