# TwitchX


### Example
```python
import asyncio
from TwitchX.stream import Stream
from TwitchX.helix import Helix
from TwitchX.ext import TwitchAccount
from TwitchX.ext import GQL_CLIENT_ID

loop = asyncio.get_event_loop()

# Get Client ID
gql_code = GQL_CLIENT_ID()
client_id = loop.run_until_complete(gql_code.get_client_id())

# Login
account = TwitchAccount(
    client_id=client_id,
    username="Twitch ID",
    password="Twitch PW",
    gmail_id="Gmail ID",
    gmail_pw="Gmail PW",
    headless=False,
    driver_path="chrome driver path"
)

# Twitch API
cookie = loop.run_until_complete(account.get_cookies())
async def main():
    app = Helix(
        client_id=client_id, 
        bearer_token=cookie["auth-token"]
    )
    user = app.Users()
    code = await user.get_users(login="b4kking")
    print(code.dict())

loop.run_until_complete(main())


# Stream URL
st = Stream()
url = loop.run_until_complete(
    st.get_twitch_live_playlist_url(
        user_name="b4kking", 
        token=cookie["auth-token"]
    )
)
print(url)
```
