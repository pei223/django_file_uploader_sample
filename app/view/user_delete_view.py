import logging
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..infra.user_repository import UserRepository

logger = logging.getLogger("default")


class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        UserRepository().delete_user(user_id)
        return redirect("/accounts/login")
