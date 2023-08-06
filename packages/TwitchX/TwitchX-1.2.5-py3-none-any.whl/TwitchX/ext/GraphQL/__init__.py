from gql import Client
from gql import gql
from gql.transport.aiohttp import AIOHTTPTransport

from typing import Optional
from TwitchX.error import MissingClientId


class TwitchGraphQL:
    def __init__(self) -> None:
        self.url = "https://gql.twitch.tv/gql"

    async def PlaybackAccessToken(
            self,
            client_id: str,
            token: Optional[str] = None,
            login: Optional[str] = None,
            isLive: bool = True,
            isVod: bool = False,
            vodID: str = "",
            playerType: str = "site"
    ) -> dict:
        """Get Twitch API credentials.
        :param client_id: Twitch Client ID
        :param token: OAuth Token
        :param login: streamerId
        :param isLive: Live Stream Status
        :param vodID: Vod content uuid, not use TwitchX project. default: ""
        :param isVod: Is it VOD content? default: False
        :param playerType: Video playback platform type. default: site
        """

        # headers overriding
        if token is not None:
            self.headers = {
                "Authorization": f"OAuth {token}",
                "Client-ID": client_id
            }
        else:
            self.headers = {
                "Client-ID": client_id
            }

        if self.headers.get("Client-ID") is None:
            raise MissingClientId

        transport = AIOHTTPTransport(
            url=self.url, headers=self.headers
        )

        async with Client(transport=transport, fetch_schema_from_transport=True) as session:
            query = gql("""query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: 
                Boolean!, $playerType: String! ) { streamPlaybackAccessToken( channelName: $login, params: { 
                platform: "web", playerBackend: "mediaplayer", playerType: $playerType }) @include(if: $isLive) {
                value signature __typename } videoPlaybackAccessToken(id: $vodID, params: { platform: "web",
                playerBackend: "mediaplayer", playerType: $playerType }) @include(if: $isVod) {  
                value signature __typename  }}""")

            params = dict(
                login=login, isLive=isLive, vodID=vodID, isVod=isVod, playerType=playerType
            )
            result = await session.execute(document=query, variable_values=params)
        return result
