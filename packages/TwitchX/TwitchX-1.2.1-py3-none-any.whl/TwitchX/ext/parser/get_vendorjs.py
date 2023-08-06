import re
from scrapy.selector import Selector
from TwitchX.util import HTTPUtil


class VendorJS(HTTPUtil):
    def __init__(self) -> None:
        super(VendorJS, self).__init__()
        self.url = "https://www.twitch.tv"
        self.ext = self

    async def _load_html(self) -> str:
        user_agent = self.ext.get_user_agent()
        html: str = await self.ext.requests(method="GET", url=self.url, headers=user_agent)
        return html

    async def _parse_script_tags(self) -> list:
        data = await self._load_html()
        source = Selector(text=data)
        vender_url = source.xpath("//script/@src")
        parsed = vender_url.getall()
        return parsed

    async def _parse_vendor_js(self) -> str:
        source = await self._parse_script_tags()
        for url in source:
            if bool(re.search("vendor", url)):
                return url

        raise Exception("Not Found")

    async def _load_vendor_js_code(self) -> str:
        vendor_js = await self._parse_vendor_js()
        user_agent = self.get_user_agent()
        source = await self.ext.requests(method="GET", url=vendor_js, headers=user_agent)
        return source

    @classmethod
    async def parse_client_id(cls) -> str:
        data = await cls()._load_vendor_js_code()
        client_id_regx = r'clientId="([A-Za-z0-9_-]+)"'
        client_id = re.findall(client_id_regx, data)
        return client_id[0]
