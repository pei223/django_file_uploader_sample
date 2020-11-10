import logging

from django.dispatch import receiver
from django.core.validators import MaxLengthValidator
from django.db import models

from django.contrib.auth.models import User

from app.domain.user_info import UserProfile, RegisterUserProfile
from app.infra.utils import delete_file

logger = logging.getLogger("default")


class UserProfileQuerySet(models.QuerySet):
    def get_user_profile(self, user_id: int) -> UserProfile:
        rows = self.filter(user__id=user_id)
        if not rows.exists():
            return UserProfile.default()
        row = rows[0]
        return UserProfile(
            intro=row.intro,
            thumbnail_name=row.thumbnail.name,
            thumbnail_url=row.thumbnail.url if row.thumbnail else None,
        )

    def register(self, user, register_user_prof: RegisterUserProfile):
        if register_user_prof.is_thumbnail_set():
            self.update_or_create(
                user=user,
                defaults={
                    "intro": register_user_prof.intro,
                    "thumbnail": register_user_prof.thumbnail_file,
                },
            )
        elif register_user_prof.is_thumbnail_delete:
            self.update_or_create(
                user=user,
                defaults={"intro": register_user_prof.intro, "thumbnail": None},
            )
        else:
            self.update_or_create(user=user, defaults={"intro": register_user_prof.intro})


class UserProfileDB(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True,
    )
    intro = models.TextField(validators=[MaxLengthValidator(500)])
    thumbnail = models.ImageField(upload_to="src/thumbnail/")

    objects = UserProfileQuerySet.as_manager()


@receiver(models.signals.pre_save, sender=UserProfileDB)
def pre_save(sender, instance, **kwargs):
    user_id = instance.user.id
    rows = UserProfileDB.objects.filter(user__id=user_id)
    if not rows.exists():
        return
    delete_file(rows[0].thumbnail)


@receiver(models.signals.post_delete, sender=UserProfileDB)
def post_deleted(sender, instance, **kwargs):
    delete_file(instance.thumbnail)
