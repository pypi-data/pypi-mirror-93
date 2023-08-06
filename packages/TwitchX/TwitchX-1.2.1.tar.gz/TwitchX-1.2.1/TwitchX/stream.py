from typing import Optional
from user_agent import generate_user_agent
from .ext.GraphQL import GraphQL
from .ext.parser import VendorJS
from .util import HTTPUtil, url_encode


class Stream(HTTPUtil):
    def __init__(self):
        super(Stream, self).__init__()

        self.ext = self
        self.user_agent = generate_user_agent(os=("mac", "linux"))
        self.twitch_api_channel = "https://api.twitch.tv/api/channels/"

    @staticmethod
    async def get_twitch_access_token(user_name: str, token: Optional[str] = None) -> dict:
        """스트리밍용으로 playlist m3u8 파일을 발급받기 위한
        `access_token` 을 발급 받습니다.

        :param token: Oauth Token
        :param user_name: 사용자
        :return: `TwitchAccessTokenInterface` 형식의 토큰 정보로 리턴
        """
        # if not client_id_raw:
        #    client_id = await self.get_stream_only_client_id()
        # else:
        #    client_id = client_id_raw

        client_id = await VendorJS.parse_client_id()
        source = await GraphQL.PlaybackAccessTokenTemplate(streamerId=user_name, isLive=True, token=token, client_id=client_id)
        _data = source.json
        data = _data.get("data")

        if data is None:
            raise Exception("Response not found")

        r = data.get("streamPlaybackAccessToken")
        res = {
            "sig": r.get("signature"),
            "token": r.get("value")
        }
        return res

    @classmethod
    async def get_twitch_live_playlist_url(
            cls, user_name: str, access_token: Optional[dict] = None, token: Optional[str] = None
    ) -> str:
        """트위치 라이브 플레이 리스트의 주소를 가져옵니다

        :param user_name: 사용자
        :param access_token: `TwitchAccessTokenInterface` 형식의 access_token (Default. `get_twitch_access_token` 으로 자동 생성함)
        :param token: Oauth Token
        :return: live playlist url
        """
        if not access_token:
            access_token = await cls().get_twitch_access_token(user_name=user_name, token=token)

        _url = [
            "https://usher.ttvnw.net/",
            "api/channel/hls/",
            f"{user_name}.m3u8",
            "?allow_source=true",
            "&playlist_include_framerate=true",
            "&player_backend=mediaplayer",
            "&fast_bread=true",
            "&reassignments_supported=true",
            f"&sig={access_token['sig']}",
            "&supported_codecs=avc1",
            f"&token={url_encode(access_token['token'])}",
            "&cdm=wv",
            "&player_version=0.9.5"
        ]
        url = "".join(_url)
        return url

    @classmethod
    async def get_twitch_live_playlist(
        cls, user_name: str, access_token: Optional[dict] = None, token: Optional[str] = None
    ) -> str:
        """트위치 라이브 플레이 리스트의 내용을 가져옵니다

        :param token: Twitch OAuth Token
        :type token: str
        :param user_name: 사용자
        :param access_token: `TwitchAccessTokenInterface` 형식의 access_token (Default. `get_twitch_access_token` 으로 자동 생성함)
        :return: live playlist
        """
        url = await cls.get_twitch_live_playlist_url(
            user_name=user_name, access_token=access_token, token=token
        )
        headers = {"User-Agent": cls().user_agent}
        resp = await cls().ext.requests("GET", url, headers)
        if type(resp) == list:
            raise Warning(f"{resp[0]['error']}")
        return resp
