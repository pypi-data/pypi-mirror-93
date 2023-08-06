import pytest


@pytest.mark.asyncio
async def test_load_html():
    from TwitchX.ext.parser import VendorJS

    core = VendorJS()
    res = await core._load_html()
    if not res:
        raise Exception

    assert isinstance(res, str)
    return res


@pytest.mark.asyncio
async def test_parse_script_tags():
    from TwitchX.ext.parser import VendorJS

    core = VendorJS()
    res = await core._parse_script_tags()
    if res is []:
        raise Exception

    assert isinstance(res, list)
    return res


@pytest.mark.asyncio
async def test_parse_vendor_js():
    from TwitchX.ext.parser import VendorJS

    core = VendorJS()
    res = await core._parse_vendor_js()
    if not res:
        raise Exception

    assert isinstance(res, str)
    return res


@pytest.mark.asyncio
async def test_load_vendor_js_code():
    from TwitchX.ext.parser import VendorJS

    core = VendorJS()
    res = await core._load_vendor_js_code()
    if not res:
        raise Exception
    assert isinstance(res, str)
    return res


@pytest.mark.asyncio
async def test_parse_client_id():
    from TwitchX.ext.parser import VendorJS

    core = VendorJS()
    res = await core.parse_client_id()
    if not res:
        raise Exception
    assert isinstance(res, str)
