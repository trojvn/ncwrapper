import xml.etree.ElementTree as ET
from io import BufferedReader

from httpwrapper import BaseClient, ClientConfig

from .async_ import AsyncNextCloud


class NextCloud(BaseClient):
    def __init__(self, base_url: str, user: str, pswd: str):
        super().__init__(base_url, {"OCS-APIRequest": "true"}, auth=(user, pswd))
        self.__config = ClientConfig(3, 900, 3, 3)

    def mkdir(self, dir_path: str) -> bool:
        """
        Create a directory on the NextCloud server.

        Args:
            dir_path (str): The path to the directory to create.
            example:
                dir_path = "/path/to/directory"

        Returns:
            bool: True if the directory was created successfully, False otherwise.
        """
        if not dir_path.startswith("/"):
            dir_path = f"/{dir_path}"
        return self._request(
            "MKCOL",
            f"/remote.php/webdav{dir_path}",
            config=self.__config,
        ).status_code in (201, 405)

    def upload_file(self, file: BufferedReader, file_path: str) -> bool:
        """
        Upload a file to the NextCloud server.

        Args:
            file (BufferedReader): The file to upload.
            file_path (str): The path to the file to upload.
            example:
                file_path = "/path/to/file.txt"

        Returns:
            bool: True if the file was uploaded successfully, False otherwise.
        """
        if not file_path.startswith("/"):
            file_path = f"/{file_path}"
        return self._put(
            f"/remote.php/webdav{file_path}",
            config=self.__config,
            content=file,
        ).status_code in (201,)

    def share_file(
        self,
        file_path: str,
        share_type: int = 3,
        permissions: int = 1,
    ) -> str:
        """
        Share a file on the NextCloud server.

        Args:
            file_path (str): The path to the file to share.
            share_type (int): The type of share to create.
            permissions (int): The permissions to set on the share.
            example:
                file_path = "/path/to/file.txt"
                share_type = 3
                permissions = 1

        Returns:
            str: The URL of the shared file.
        """
        if not file_path.startswith("/"):
            file_path = f"/{file_path}"
        r = self._post(
            url="/ocs/v2.php/apps/files_sharing/api/v1/shares",
            config=self.__config,
            json_data={
                "path": file_path,
                "shareType": share_type,
                "permissions": permissions,
            },
        )
        if r.status_code not in (200, 201):
            return ""
        root = ET.fromstring(r.text)
        url_element = root.find(".//url")
        if url_element is not None:
            return url_element.text or ""
        return ""


__all__ = ["NextCloud", "AsyncNextCloud"]
