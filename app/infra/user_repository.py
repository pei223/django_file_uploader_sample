from django.contrib.auth.models import User
from app.infra.db.user_profile_db import UserProfileDB
from ..domain.user_info import UserProfile, RegisterUserProfile


class UserRepository:
    def delete_user(self, user_id: int):
        User.objects.filter(id=user_id).delete()

    def get_user_profile(self, user_id: int) -> UserProfile:
        return UserProfileDB.objects.get_user_profile(user_id)

    def save_user_profile(self, user, register_user_prof: RegisterUserProfile) -> UserProfile:
        UserProfileDB.objects.register(user, register_user_prof)
        return self.get_user_profile(user.id)
