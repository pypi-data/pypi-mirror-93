import pytest


name = "saddummy"


@pytest.mark.asyncio
async def test_get_twitch_access_token():
    from TwitchX.stream import Stream

    app = Stream()
    res = await app.get_twitch_access_token(name)
    if not res:
        raise Exception
    assert isinstance(res, dict)
    return res


@pytest.mark.asyncio
async def test_get_twitch_live_playlist_url():
    from TwitchX.stream import Stream

    app = Stream()
    res = await app.get_twitch_live_playlist_url(name)
    if not res:
        raise Exception
    assert isinstance(res, str)
    return res


@pytest.mark.asyncio
async def test_get_twitch_live_playlist():
    from TwitchX.stream import Stream

    app = Stream()
    try:
        res = await app.get_twitch_live_playlist(name)
    except Warning as e:
        print(e)
        return None

    if not res:
        raise Exception
    assert isinstance(res, str)
    return res
