from django.urls import path

from .view.files_view import file_download_view, FilesView, file_delete_view
from .view.index_view import IndexView
from .view.signup_view import SignUpView
from .view.user_delete_view import UserDeleteView
from .view.user_profile_view import UserProfileView

urlpatterns = [
    path("", IndexView.as_view()),
    path("accounts/signup", SignUpView.as_view()),
    path("accounts/delete", UserDeleteView.as_view()),
    path("accounts/profile", UserProfileView.as_view()),
    path("files", FilesView.as_view()),
    path("files/delete", file_delete_view),
    path("files/download", file_download_view),
]
