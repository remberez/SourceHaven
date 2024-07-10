import os
from typing import Union, Optional

from celery.result import AsyncResult
from django.contrib.auth.models import User
from sourceHaven.celery_config import app


def get_folder_hierarchy(instance: Union['Folder', 'File']) -> Optional[list[str]]:
    folder_hierarchy = []

    if instance.parent_folder:
        folder_hierarchy += get_folder_hierarchy(instance.parent_folder) + [instance.name]
    else:
        folder_hierarchy = [instance.name] + folder_hierarchy
    return folder_hierarchy or None


def project_directory_path(instance, filename) -> str:
    directory_path = f'projects/{instance.project_id.owner.id}/' \
                     f'{instance.project_id.name}/' \
                     f'{"/".join(get_folder_hierarchy(instance)[:-1])}/' \
                     f'{filename}'
    return directory_path


def get_or_none(class_model, **kwargs):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        return class_model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def get_tasks(method: str):
    if method == 'active':
        tasks = app.control.inspect().active()
    elif method == 'reserved':
        tasks = app.control.inspect().reserved()
    elif method == 'scheduled':
        tasks = app.control.inspect().scheduled()
    else:
        return 'Несуществующий метод'
    return tasks


def get_user_tasks(user: User, folder: 'Folder' = None) -> [str]:
    scheduled_tasks = get_tasks('scheduled')
    tasks_to_display = []

    for _, tasks in scheduled_tasks.items():
        for task in tasks:
            task_id = task['request']['id']
            task_args = task['request']['args'][0]
            task_result = AsyncResult(task_id)

            if task_result.state == 'PENDING':
                user_id = task_args['user_id']
                parent_folder = task_args['parent_folder']
                if parent_folder:
                    parent_folder = int(parent_folder)

                if user.id == user_id:
                    if (folder and parent_folder == folder.id) or (not folder and not parent_folder):
                        tasks_to_display.append(task_args['file_name'])

    return tasks_to_display


def get_all_folders(project: 'Project') -> list[(str, int)]:
    directories = []
    for folder in project.folder.all():
        path = '\\'.join(get_folder_hierarchy(folder)) + '\\'
        folder_id = folder.id
        directories.append((path, folder_id))

    return directories
