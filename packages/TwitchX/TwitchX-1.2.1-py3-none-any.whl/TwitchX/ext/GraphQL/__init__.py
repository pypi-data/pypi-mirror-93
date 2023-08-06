from typing import Optional
from aiographql.client import GraphQLClient
from aiographql.client.response import GraphQLResponse
from aiographql.client.request import GraphQLRequest


class GraphQL:

    @staticmethod
    async def PlaybackAccessTokenTemplate(
            streamerId: str,
            client_id: str,
            isLive: bool,
            token: Optional[str] = None,
            vodID: str = "",
            isVod: bool = False,
            playerType: str = "site"
    ) -> GraphQLResponse:
        """Twitch GraphQL

        Play back Access Token

        :param streamerId: Twitch Streamer ID
        :type streamerId: str
        :param client_id: Client ID
        :type client_id: str
        :param isLive: Live
        :type isLive: bool
        :param token: OAuth Token
        :type token: Optional[str]
        :param vodID: ""
        :type vodID: str
        :param isVod: False
        :type isVod: bool
        :param playerType: site
        :type playerType: str
        :return:
        :rtype: dict
        """
        if token:
            headers = {
                "Authorization": f"OAuth {token}",
                "Client-ID": client_id
            }
        else:
            headers = {
                "Client-ID": client_id
            }

        _client = GraphQLClient(
            endpoint="https://gql.twitch.tv/gql",
            headers=headers,
            session=None
        )
        _query = GraphQLRequest(
            query="""
                query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {
                    streamPlaybackAccessToken(
                        channelName: $login,
                        params: {
                            platform: "web",
                            playerBackend: "mediaplayer",
                            playerType: $playerType
                        }
                    )
                    @include(if: $isLive) {
                        value
                        signature
                        __typename
                    }
                    videoPlaybackAccessToken(id: $vodID, params: {
                        platform: "web",
                        playerBackend: "mediaplayer",
                        playerType: $playerType
                    })
                    @include(if: $isVod) {
                        value
                        signature
                        __typename  
                    }
                }
            """,
            variables={
                "login": streamerId,
                "isLive": isLive,
                "vodID": vodID,
                "isVod": isVod,
                "playerType": playerType
            },
        )
        return await _client.query(request=_query)

