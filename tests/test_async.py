import os

import pytest
from dotenv import load_dotenv

from ncwrapper.async_ import AsyncNextCloud

load_dotenv()

L = os.getenv("L", "")
U = os.getenv("U", "")
P = os.getenv("P", "")


@pytest.mark.asyncio
async def test_rm():
    nc = AsyncNextCloud(L, U, P)
    assert await nc.rm("/test_async/")


@pytest.mark.asyncio
async def test_mkdir():
    nc = AsyncNextCloud(L, U, P)
    assert await nc.mkdir("/test_async")


@pytest.mark.asyncio
async def test_upload_file():
    nc = AsyncNextCloud(L, U, P)
    with open("poetry.lock", "rb") as f:
        assert await nc.upload_file(f, "/test_async/poetry.lock")


@pytest.mark.asyncio
async def test_share_file():
    nc = AsyncNextCloud(L, U, P)
    print(await nc.share_file("/test_async/poetry.lock"))
