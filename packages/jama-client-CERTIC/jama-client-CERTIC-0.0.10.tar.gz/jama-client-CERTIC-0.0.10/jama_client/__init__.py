"""
# Jama client library

## Installation

Use pip to install:

    pip install jama-client-CERTIC

## Quick start

    from jama_client import Client
    client = Client("https://acme.tld/rpc/", "secretapikeyhere")
    file_id = client.upload("/path/to/some/file.jpg")
    collection_id = client.add_collection("title of the collection")
    client.add_file_to_collection(file_id, collection_id)


"""
import os
import math
import hashlib
from requests import post
from typing import Any, Union, List, Dict
import base64


DEFAULT_UPLOAD_CHUNK_SIZE = 1024 * 1024


def _file_hash256(file_path: str) -> str:
    hsh = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chnk in iter(lambda: f.read(8192), b""):
            hsh.update(chnk)
    return hsh.hexdigest()


def _get_nb_of_chunks(
    file_path: str, chunk_size: int = DEFAULT_UPLOAD_CHUNK_SIZE
) -> int:
    size = os.path.getsize(file_path)
    return math.ceil(size / chunk_size)


def _get_file_slice(
    file_path: str, from_byte: int, max_size: int = DEFAULT_UPLOAD_CHUNK_SIZE
) -> bytes:
    with open(file_path, "rb") as f:
        f.seek(from_byte)
        return f.read(max_size)


class IncompleteUpload(RuntimeError):
    pass


class ServiceError(RuntimeError):
    def __init__(self, message):
        super(ServiceError, self).__init__()
        self.message = message


class _Method(object):
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "{}.{}".format(self.__name, name))

    def __call__(self, *args):
        return self.__send(self.__name, args)


class _Chunker:
    def __init__(self, file_path: str, chunk_size: int = DEFAULT_UPLOAD_CHUNK_SIZE):
        self._file_path = file_path
        self._chunk_size = chunk_size
        self.nb_of_chunks = _get_nb_of_chunks(self._file_path, self._chunk_size)
        self.file_hash = _file_hash256(self._file_path)

    def get_chunk(self, number_of_chunk) -> bytes:
        if number_of_chunk > self.nb_of_chunks or number_of_chunk < 0:
            raise ValueError("Chunk number out of range")
        return _get_file_slice(
            self._file_path, self._chunk_size * number_of_chunk, self._chunk_size
        )

    @property
    def chunks(self):
        for i in range(self.nb_of_chunks):
            yield self.get_chunk(i)


class _ChunksUploader:
    def __init__(
        self,
        file_path: str,
        endpoint: str,
        api_key: str,
        chunk_size: int = DEFAULT_UPLOAD_CHUNK_SIZE,
        file_name: str = None,
        origin_dir_name: str = None,
    ):
        self.foreign_reference = None
        self._file_path = file_path
        self._file_name = file_name
        self._origin_dir_name = origin_dir_name
        self._api_key = api_key
        self._endpoint = endpoint
        self._chunker = _Chunker(file_path, chunk_size)
        self.chunks_statuses = {}
        for i in range(self.number_of_chunks):
            self.chunks_statuses[i] = {
                "chunk_number": i,
                "tries": 0,
                "done": False,
                "message": "",
            }

    @property
    def number_of_chunks(self) -> int:
        return self._chunker.nb_of_chunks

    @property
    def is_complete(self) -> bool:
        for k in self.chunks_statuses:
            if not self.chunks_statuses[k]["done"]:
                return False
        return True

    def upload_all(self):
        for i in range(self.number_of_chunks):
            if not self.chunks_statuses[i]["done"] and self.foreign_reference is None:
                self.upload(i)

    def upload(self, chunk_number: int):
        self.chunks_statuses[chunk_number]["tries"] = (
            self.chunks_statuses[chunk_number]["tries"] + 1
        )
        try:
            headers = {
                "X-Api-Key": self._api_key,
                "X-file-chunk": "{}/{}".format(chunk_number, self.number_of_chunks),
                "X-file-hash": self._chunker.file_hash,
                "X-file-name": base64.b64encode(
                    (self._file_name or os.path.basename(self._file_path)).encode(
                        "utf-8"
                    )
                ),
            }
            if self._origin_dir_name:
                headers["X-origin-dir"] = self._origin_dir_name
            response = post(
                url=self._endpoint,
                data=self._chunker.get_chunk(chunk_number),
                headers=headers,
            )
            if response.status_code == 202:
                self.chunks_statuses[chunk_number]["done"] = True
            elif response.status_code == 200:
                for i in range(self.number_of_chunks):
                    self.chunks_statuses[i]["done"] = True
                self.foreign_reference = int(response.text)
            else:
                self.chunks_statuses[chunk_number][
                    "message"
                ] = "failed with status {} {}".format(
                    response.status_code, response.text
                )
        except Exception as e:
            self.chunks_statuses[chunk_number]["message"] = getattr(
                e, "message", repr(e)
            )


class Client:
    def __init__(self, endpoint: str, api_key: str):
        self._endpoint = endpoint
        self._api_key = api_key
        self.requests_count = 0
        self.upload_status = {}

    def __getattr__(self, name):
        return _Method(self.__call, name)

    def __call(self, method: str, params: List = None) -> Any:
        self.requests_count = self.requests_count + 1
        payload = {"method": method, "params": params or [], "id": self.requests_count}
        try:
            response = post(
                url=self._endpoint, json=payload, headers={"X-Api-Key": self._api_key}
            )
        except Exception:
            raise ServiceError("Could not contact service")
        if response.status_code == 200:
            message = response.json()
            if message["error"] is None:
                return message["result"]
            else:
                raise ServiceError(message["error"])
        else:
            raise ServiceError(
                "Response ended with status code {}".format(response.status_code)
            )

    def upload(
        self,
        file_path: str,
        chunk_size: int = DEFAULT_UPLOAD_CHUNK_SIZE,
        file_name: str = None,
        origin_dir_name: str = None,
    ) -> int:
        """
        This methods uploads a file in multiple chunks, allowing
        resumable uploads.

        ```file_path``` is the local path to the file.

        ```chunk_size``` is the number of bytes uploaded with each chunk of the file.

        ```file_name``` overides the name of the file, should you want a different name in Jama than
        the local name.

        ```origin_dir_name``` is a directory path (```dirA/dirB/dirC```). This path triggers
        the creation of the corresponding collections and sub-collections in Jama.
        """
        chunked_upload = _ChunksUploader(
            file_path,
            self._endpoint + "upload/partial/",
            self._api_key,
            chunk_size,
            file_name,
            origin_dir_name,
        )
        chunked_upload.upload_all()
        if not chunked_upload.is_complete:
            self.upload_status[file_path] = chunked_upload.chunks_statuses
            raise IncompleteUpload()
        return chunked_upload.foreign_reference

    def add_collection(self, title: str, parent_id: int = None) -> Union[Dict, None]:
        return self.__call("add_collection", [title, parent_id])

    def add_collection_from_path(self, path: str) -> List[Dict]:
        return self.__call("add_collection_from_path", [path])

    def add_file_to_collection(self, file_id: int, collection_id: int) -> bool:
        return self.__call("add_file_to_collection", [file_id, collection_id])

    def add_meta_to_collection(
        self, collection_id: int, meta_id: int, meta_value: str
    ) -> Union[int, bool]:
        return self.__call(
            "add_meta_to_collection", [collection_id, meta_id, meta_value]
        )

    def add_meta_to_file(
        self, file_id: int, meta_id: int, meta_value: str
    ) -> Union[int, bool]:
        return self.__call("add_meta_to_file", [file_id, meta_id, meta_value])

    def add_meta_to_resource(
        self, resource_id: int, meta_id: int, meta_value: str
    ) -> Union[int, bool]:
        return self.__call("add_meta_to_resource", [resource_id, meta_id, meta_value])

    def add_metadata(
        self, title: str, metas_set_id: int, metadata_type_id: int = None
    ) -> Union[int, bool]:
        return self.__call("add_metadata", [title, metas_set_id, metadata_type_id])

    def add_metadataset(self, title: str) -> int:
        return self.__call("add_metadataset", [title])

    def add_resource_to_collection(self, resource_id: int, collection_id: int) -> bool:
        return self.__call("add_resource_to_collection", [resource_id, collection_id])

    def advanced_search(self, search_terms: List[Dict]) -> Dict[str, List]:
        return self.__call("advanced_search", [search_terms])

    def advanced_search_terms(self) -> List[str]:
        return self.__call("advanced_search_terms", [])

    def ancestors_from_collection(
        self, collection_id: int, include_self: bool = False
    ) -> List[dict]:
        return self.__call("ancestors_from_collection", [collection_id, include_self])

    def ancestors_from_resource(self, resource_id: int) -> List[List[dict]]:
        return self.__call("ancestors_from_resource", [resource_id])

    def collection(self, collection_id: int) -> Union[Dict, None]:
        return self.__call("collection", [collection_id])

    def collections(self, parent_id: int = None) -> List[Dict]:
        return self.__call("collections", [parent_id])

    def delete_collection(self, collection_id: int) -> bool:
        return self.__call("delete_collection", [collection_id])

    def delete_file(self, file_id: int) -> bool:
        return self.__call("delete_file", [file_id])

    def delete_resource(self, resource_id: int) -> bool:
        return self.__call("delete_resource", [resource_id])

    def file(self, file_id: int) -> Union[Dict, None]:
        return self.__call("file", [file_id])

    def files(self, collection_id: int, include_metas: bool = True) -> List[Dict]:
        return self.__call("files", [collection_id, include_metas])

    def metadata(self, metadata_id: int) -> Union[Dict, None]:
        return self.__call("metadata", [metadata_id])

    def metadatas(self, metadata_set_id: int) -> List[Dict]:
        return self.__call("metadatas", [metadata_set_id])

    def metadatasets(self) -> List[Dict]:
        return self.__call("metadatasets", [])

    def metadatatypes(self) -> List[dict]:
        return self.__call("metadatatypes", [])

    def ping(self) -> str:
        return self.__call("ping", [])

    def remove_file_from_collection(self, file_id: int, collection_id: int) -> bool:
        return self.__call("remove_file_from_collection", [file_id, collection_id])

    def remove_meta_from_collection(
        self, collection_id: int, meta_value_id: int
    ) -> bool:
        return self.__call(
            "remove_meta_from_collection", [collection_id, meta_value_id]
        )

    def remove_meta_from_file(self, file_id: int, meta_value_id: int) -> bool:
        return self.__call("remove_meta_from_file", [file_id, meta_value_id])

    def remove_meta_from_resource(self, resource_id: int, meta_value_id: int) -> bool:
        return self.__call("remove_meta_from_resource", [resource_id, meta_value_id])

    def remove_resource_from_collection(
        self, resource_id: int, collection_id: int
    ) -> bool:
        return self.__call(
            "remove_resource_from_collection", [resource_id, collection_id]
        )

    def rename_collection(self, collection_id: int, title: str) -> bool:
        return self.__call("rename_collection", [collection_id, title])

    def rename_file(self, file_id: int, title: str) -> bool:
        return self.__call("rename_file", [file_id, title])

    def rename_meta(self, meta_id: int, title: str) -> bool:
        return self.__call("rename_meta", [meta_id, title])

    def rename_resource(self, resource_id: int, title: str) -> bool:
        return self.__call("rename_resource", [resource_id, title])

    def resource(self, resource_id: int) -> Union[Dict, None]:
        return self.__call("resource", [resource_id])

    def resources(self, collection_id: int, include_metas: bool = True) -> List[Dict]:
        return self.__call("resources", [collection_id, include_metas])

    def simple_search(self, query: str) -> Dict[str, List]:
        return self.__call("simple_search", [query])

    def supported_file_types(self) -> List[Dict]:
        return self.__call("supported_file_types", [])

    def upload_infos(self, sha256_hash: str) -> Dict:
        return self.__call("upload_infos", [sha256_hash])
