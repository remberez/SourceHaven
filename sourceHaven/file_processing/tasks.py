from celery import shared_task
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import File, Project, FileExtensions, Folder
from .utils import get_or_none, get_tasks
import uuid


@shared_task
def file_created(file_data):

    """Не лучшее использование задач celery.
    При вызове функции get_tasks из utils.py этого приложения
    происходит небольшая задержка 2-4 секунды из-за части кода,
    где нужно получить активные и зарезервированные задачи.
    """

    user_id = file_data['user_id']
    project_name = file_data['project_name']
    file_size = file_data['size']
    file_content = file_data['content']
    file_name = file_data['file_name']
    file_extension = file_data['file_extension']
    parent_folder_id = file_data['parent_folder']

    user = User.objects.get(id=user_id)
    project = Project.objects.get(name=project_name, owner=user)
    extension_id = get_or_none(FileExtensions, extension=file_extension)
    parent_folder = get_or_none(Folder, id=parent_folder_id)

    if extension_id:

        new_file = File(
            project_id=project,
            name=file_name,
            file_size=file_size,
            extension=file_extension,
            extension_id=extension_id,
            parent_folder=parent_folder,
        )

        new_file.filling_the_file.save(str(uuid.uuid4()) + file_extension, ContentFile(file_content))
        new_file.save()
        return True

    return False
