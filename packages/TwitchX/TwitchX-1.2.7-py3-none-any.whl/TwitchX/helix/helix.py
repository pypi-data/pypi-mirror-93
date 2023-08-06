from typing import Optional
from datetime import timedelta

from TwitchX.api import API
from TwitchX.helix.resource import Streams as _Streams
from TwitchX.helix.resource import Search as _Search
from TwitchX.helix.resource import Users as _Users


class Helix:
    BASE_URL: str = 'https://api.twitch.tv/helix/'

    def __init__(self,
                 client_id: str,
                 use_cache: bool = False,
                 cache_duration: Optional[timedelta] = None,
                 bearer_token: Optional[str] = None) -> None:
        """
        Helix API (New Twitch API)
        https://dev.twitch.tv/docs/api/

        :param client_id: Twitch client ID
        :param use_cache: Cache API requests (recommended)
        :param cache_duration: Cache duration
        :param bearer_token: API bearer token
        """
        self.client_id = client_id
        self.use_cache = use_cache
        self.cache_duration = cache_duration
        self.bearer_token = bearer_token

        self.source = API(
            base_url=self.BASE_URL,
            client_id=self.client_id,
            use_cache=self.use_cache,
            cache_duration=self.cache_duration,
            bearer_token=self.bearer_token
        )

    def Users(self):
        return _Users(source=self.source)

    def Streams(self):
        return _Streams(source=self.source)

    def Search(self):
        return _Search(source=self.source)
