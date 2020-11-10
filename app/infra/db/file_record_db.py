from typing import Optional, List

from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from app.domain.file_record import FileRecord, RegisterFileRecord
from app.infra.utils import delete_file


class FileRecordQuerySet(models.QuerySet):
    def get_user_files(self, user_id: int, page_num: int, paginate_by: int) -> List[FileRecord]:
        rows = self.filter(user__id=user_id).order_by("created_at").reverse()[
               (page_num - 1) * paginate_by:page_num * paginate_by]
        if not rows.exists():
            return []
        result = []
        for row in rows:
            result.append(FileRecord(
                id_=row.pk,
                file_name=row.file.name,
                file_url=row.file.url,
                file_path=row.file.path,
            ))
        return result

    def get_file_record(self, user_id: int, pk: int) -> Optional[FileRecord]:
        rows = self.filter(pk=pk, user__id=user_id)
        if not rows.exists():
            return None
        return FileRecord(
            id_=pk,
            file_name=rows[0].file.name,
            file_url=rows[0].file.url,
            file_path=rows[0].file.path,
        )

    def register_file_record(self, user, register_file_record: RegisterFileRecord):
        FileRecordDB(user=user, file=register_file_record.file).save()

    def delete_file_record(self, pk: int, user_id: int):
        self.filter(pk=pk, user__id=user_id).delete()

    def is_own_file(self, pk: int, user_id: int):
        return self.filter(pk=pk, user__id=user_id).exists()

    def data_count(self, user_id: int):
        return self.filter(user__id=user_id).count()


class FileRecordDB(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
        unique=False,
    )
    file = models.FileField(upload_to="secret", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FileRecordQuerySet.as_manager()


@receiver(models.signals.pre_save, sender=FileRecordDB)
def pre_save(sender, instance, **kwargs):
    rows = FileRecordDB.objects.filter(pk=instance.pk)
    if not rows.exists():
        return
    delete_file(rows[0].file)


@receiver(models.signals.post_delete, sender=FileRecordDB)
def post_deleted(sender, instance, **kwargs):
    delete_file(instance.file)
