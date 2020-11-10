from typing import Optional, List
from app.domain.file_record import FileRecord, RegisterFileRecord
from .db.file_record_db import FileRecordDB


class FileRecordRepository:
    def get_user_files(self, user_id: int, page_num: int, paginate_by: int) -> List[FileRecord]:
        return FileRecordDB.objects.get_user_files(user_id, page_num, paginate_by)

    def get_file_record(self, pk: int, user_id: int) -> Optional[FileRecord]:
        return FileRecordDB.objects.get_file_record(user_id, pk)

    def register_file_record(self, user, register_file_record: RegisterFileRecord):
        FileRecordDB.objects.register_file_record(user, register_file_record)

    def delete_file_record(self, pk: int, user_id: int):
        FileRecordDB.objects.delete_file_record(pk, user_id)

    def is_own_file(self, pk: int, user_id: int) -> bool:
        return FileRecordDB.objects.is_own_file(pk, user_id)

    def data_count(self, user_id: int) -> int:
        return FileRecordDB.objects.data_count(user_id)
