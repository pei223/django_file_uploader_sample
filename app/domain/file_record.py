from django.core.files.uploadedfile import UploadedFile


class FileRecord:
    def __init__(self, id_: int, file_name: str, file_path: str, file_url: str):
        self._id = id_
        self._file_name = file_name
        self._file_url = file_url
        self._file_path = file_path

    @property
    def id_(self):
        return self._id

    @property
    def file_name(self) -> str:
        return self._file_name[self._file_name.find("/") + 1:]

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def file_url(self) -> str:
        return self._file_url


class RegisterFileRecord:
    def __init__(self, file_: UploadedFile):
        self._file = file_

    @property
    def file(self) -> UploadedFile:
        return self._file
