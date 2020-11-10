from typing import Optional, Dict

from django.core.files.uploadedfile import UploadedFile
from django.conf import settings


class RegisterUserProfile:
    def __init__(
        self,
        intro: str,
        thumbnail_file: Optional[UploadedFile],
        is_thumbnail_delete: bool,
    ):
        self._intro = intro
        self._thumbnail_file = thumbnail_file
        self._is_thumbnail_delete = is_thumbnail_delete

    @property
    def intro(self) -> str:
        return self._intro

    def is_thumbnail_set(self) -> bool:
        return self._thumbnail_file is not None

    @property
    def thumbnail_file(self) -> UploadedFile:
        return self._thumbnail_file

    @property
    def is_thumbnail_delete(self) -> bool:
        return self._is_thumbnail_delete


class UserProfile:
    def __init__(self, intro: str, thumbnail_name: Optional[str] = None, thumbnail_url: Optional[str] = None):
        self._intro = intro
        self._thumbnail_name = thumbnail_name
        self._thumbnail_url = thumbnail_url

    @property
    def intro(self) -> str:
        return self._intro

    @property
    def thumbnail_url(self) -> str:
        return self._thumbnail_url if self._thumbnail_url else settings.NOIMAGE_URL

    @property
    def thumbnail_path(self) -> str:
        return self._thumbnail_name

    @staticmethod
    def default() -> "UserProfile":
        return UserProfile(intro="")

    def to_dict(self) -> Dict:
        return {
            "intro": self._intro,
        }
