import traceback
import logging

from django.db.models.fields.files import ImageFieldFile

logger = logging.getLogger("default")


def delete_file(image_field: ImageFieldFile):
    if not image_field:
        return
    storage = image_field.storage
    try:
        path = image_field.path
        storage.delete(path)
    except ValueError:
        logger.error(traceback.format_exc())
