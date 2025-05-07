import os

from dotenv import load_dotenv

from ncwrapper import NextCloud

load_dotenv()


U = os.getenv("U", "")
P = os.getenv("P", "")
L = os.getenv("L", "")


def test_mkdir():
    nc = NextCloud(L, U, P)
    assert nc.mkdir("/test")


def test_upload_file():
    nc = NextCloud(L, U, P)
    with open("poetry.lock", "rb") as f:
        assert nc.upload_file(f, "/test/poetry.lock")


def test_share_file():
    nc = NextCloud(L, U, P)
    print(nc.share_file("/test/poetry.lock"))
