import logging
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .form.user_profile_form import UserProfileForm
from ..infra.user_repository import UserRepository
from ..domain.user_info import RegisterUserProfile

logger = logging.getLogger("default")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        user_profile = UserRepository().get_user_profile(user_id=user_id)
        form = UserProfileForm(user_profile.to_dict())
        context = {
            "form": form,
            "user_profile": user_profile,
        }
        return render(request, "user_profile.html", context)

    def post(self, request):
        user = request.user
        form = UserProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            return self._error_response(request, form)

        intro = form.cleaned_data["intro"]
        thumbnail_file = form.cleaned_data["thumbnail"]
        is_thumbnail_delete = form.cleaned_data["is_thumbnail_delete"]
        user_profile = UserRepository().save_user_profile(
            user,
            RegisterUserProfile(
                intro=intro,
                thumbnail_file=thumbnail_file,
                is_thumbnail_delete=is_thumbnail_delete,
            ),
        )
        context = {
            "form": form,
            "user_profile": user_profile,
            "is_save_succeed": True,
        }
        return render(request, "user_profile.html", context)

    def _error_response(self, request, form):
        user_profile = UserRepository().get_user_profile(user_id=request.user.id)
        return render(
            request,
            "user_profile.html",
            {
                "form": form,
                "user_profile": user_profile,
            },
        )
