import xml.etree.ElementTree as ET
from io import BufferedReader

from httpwrapper import BaseClient, ClientConfig

from .async_ import AsyncNextCloud


class NextCloud(BaseClient):
    def __init__(self, base_url: str, user: str, pswd: str):
        super().__init__(base_url, {"OCS-APIRequest": "true"}, auth=(user, pswd))
        self.__config = ClientConfig(3, 900, 3, 3)

    def mkdir(self, dir_name: str) -> bool:
        return self._request(
            "MKCOL",
            f"/remote.php/webdav/{dir_name}",
            config=self.__config,
        ).status_code in (201, 405)

    def upload_file(self, file: BufferedReader, file_name: str) -> bool:
        return self._put(
            f"/remote.php/webdav/{file_name}",
            config=self.__config,
            content=file,
        ).status_code in (201,)

    def share_file(
        self,
        file_path: str,
        share_type: int = 3,
        permissions: int = 1,
    ) -> str:
        r = self._post(
            url="/ocs/v2.php/apps/files_sharing/api/v1/shares",
            config=self.__config,
            json_data={
                "path": file_path,
                "shareType": share_type,
                "permissions": permissions,
            },
        )
        if r.status_code != 200:
            return ""
        if not (_url := ET.fromstring(r.text).find(".//url")):
            return ""
        return _url.text or ""


__all__ = ["NextCloud", "AsyncNextCloud"]
