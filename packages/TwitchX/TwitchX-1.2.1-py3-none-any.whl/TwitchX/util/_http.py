import ujson
import typing
import urllib.parse

from aiohttp import ClientSession
from user_agent import generate_user_agent


def url_encode(string: str):
    return urllib.parse.quote(string)


class HTTPUtil:
    def __init__(self) -> None:
        self.method_list = ["GET", "POST"]

    @staticmethod
    def method(arg) -> int:
        if "GET" or "get" == arg:
            return 0
        elif "POST" or "post" == arg:
            return 1
        else:
            raise Exception("Invalid method")

    @staticmethod
    def get_user_agent(os: tuple = ("mac", "linux")) -> typing.Dict[str, str]:
        """Get User-Agent

        :param os: operating system ex) mac, linux
        :type os: tuple
        :return: {"User-Agent": __user_agent}
        :rtype: dict[str, str]
        """
        __user_agent = generate_user_agent(os=os)
        user_agent = {"User-Agent": __user_agent}
        return user_agent

    @staticmethod
    async def request_payload(url: str, data: dict, headers: dict):
        async with ClientSession(headers=headers) as session:
            async with session.post(url=url, json=data) as resp:
                result = await resp.json()
        return result

    async def requests(self, method: str, url: str, headers):
        """
        :param method:
        :param url:
        :param headers:
        """

        async with ClientSession(headers=headers) as session:
            _method = getattr(session, self.method_list[self.method(method)].lower())
            async with _method(url) as resp:
                content = resp.content_type
                rs = await resp.text()
                if content == "application/json":
                    rs = ujson.loads(rs)
            return rs
