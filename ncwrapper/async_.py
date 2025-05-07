import xml.etree.ElementTree as ET
from io import BufferedReader

from aiohttp import ClientTimeout
from httpwrapper import AsyncClientConfig, BaseAsyncClient


class AsyncNextCloud(BaseAsyncClient):
    def __init__(self, base_url: str, user: str, pswd: str):
        super().__init__(base_url, {"OCS-APIRequest": "true"}, auth=(user, pswd))
        self.__config = AsyncClientConfig(3, ClientTimeout(900), 3, 3)

    async def mkdir(self, dir_name: str) -> bool:
        return (
            await self._request(
                method="MKCOL",
                config=self.__config,
                url=f"/remote.php/webdav/{dir_name}",
            )
        ).status in (201, 405)

    async def upload_file(self, file: BufferedReader, file_name: str) -> bool:
        return (
            await self._put(
                url=f"/remote.php/webdav/{file_name}",
                config=self.__config,
                data=file,
            )
        ).status in (201,)

    async def share_file(
        self,
        file_path: str,
        share_type: int = 3,
        permissions: int = 1,
    ) -> str:
        r = await self._post(
            url="/ocs/v2.php/apps/files_sharing/api/v1/shares",
            config=self.__config,
            json_data={
                "path": file_path,
                "shareType": share_type,
                "permissions": permissions,
            },
        )
        if r.status != 200:
            return ""
        if not (_url := ET.fromstring(await r.text()).find(".//url")):
            return ""
        return _url.text or ""
