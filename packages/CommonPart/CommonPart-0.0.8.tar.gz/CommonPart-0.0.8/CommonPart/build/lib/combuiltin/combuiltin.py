# coding:utf-8
"""
系统通用内建模块
提供通用功能块
"""

import time
import datetime
import requests
import random
# from aiohttp import ClientSession
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from CommonPart.commonvar.commonvar import CommonVar, ProxyUnit

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ComBuiltin:

    @staticmethod
    def get_current_time():
        """
        获取系统当前日期时间
        :return: 2020-02-02 08:00:00
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def get_current_date():
        """
        获取系统当前日期
        :return: 2020-02-02
        """
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_timestamp13():
        """获取13位时间戳"""
        return int(round(time.time() * 1000))

    @staticmethod
    def get(url, **kwargs):
        """
        模拟发送GET请求
        url headers verify proxy timeout
        ifproxy: 是否使用代理访问  默认 False
        trytimes: 是否做请求失败尝试 默认不重试
        :return:
        """
        trytimes = kwargs.pop(CommonVar.trytimes) if CommonVar.trytimes in kwargs.keys() else 1
        if_proxy = kwargs.pop(CommonVar.ifproxy) if CommonVar.ifproxy in kwargs.keys() else False
        if if_proxy:  # 使用代理访问
            proxy_info = ComBuiltin.get(ProxyUnit.URL, verify=False, trytimes=1, timeout=3).json()
            if not proxy_info[CommonVar.status]:
                kwargs[CommonVar.proxies] = proxy_info[CommonVar.proxy]
        current_time, response = 1, None
        while current_time <= trytimes:
            try:
                response = requests.get(url, **kwargs)
                break
            except:
                current_time += 1
                continue
            finally:
                time.sleep(random.randint(1, 3) / 10)
        return response

    """
    @staticmethod
    async def async_get(url, **kwargs):
        模拟发送GET请求 异步实现
        url headers verify proxy timeout
        ifproxy: 是否使用代理访问  默认 False
        trytimes: 是否做请求失败尝试 默认不重试
        :return:
        
        trytimes = kwargs.pop(CommonVar.trytimes) if CommonVar.trytimes in kwargs.keys() else 1
        if_proxy = kwargs.pop(CommonVar.ifproxy) if CommonVar.ifproxy in kwargs.keys() else False
        if if_proxy:  # 使用代理访问
            proxy = {}
            kwargs[CommonVar.proxy] = proxy
        current_time, response = 1, None
        while current_time <= trytimes:
            try:
                async with ClientSession() as session:
                    async with session.get(url, **kwargs) as resp:
                        response = await resp
            except Exception as e:
                current_time += 1
                continue
            finally:
                time.sleep(random.randint(1, 3) / 10)

        return response
    """

    @staticmethod
    def post(url, **kwargs):
        """
        模拟发送POST请求
        url headers verify proxy
        :return:
        """
        pass
