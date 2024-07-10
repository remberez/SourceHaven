from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, File, Folder, FileExtensions
from account.models import Profile
from django.views.decorators.http import require_POST
from django.conf import settings
from .forms import UploadProjectForm
import os
from .utils import get_or_none, get_tasks, get_user_tasks, project_directory_path, get_folder_hierarchy, get_all_folders
from .tasks import file_created


def create_project(request):
    if request.method == 'POST':
        _, name, description, publicity = request.POST.values()
        project = Project.objects.create(name=name,
                                         description=description,
                                         is_public=publicity,
                                         owner=request.user)
        return render(
            request,
            'file_processing/project_created.html',
            {
                'project': project,
            }
        )
    else:
        return render(
            request,
            'file_processing/create_project.html',
        )


def project_detail(request, user_slug, project_slug, directory_path=None):
    user = get_object_or_404(Profile, slug=user_slug)
    project = get_object_or_404(Project, slug=project_slug, owner=user.user)
    upload_project_form = UploadProjectForm()

    if request.user.profile.slug == user_slug or project.is_public:
        folder = None
        parent_folder = None
        if directory_path:
            folder_name = directory_path.split('/')[-1]
            folder = Folder.objects.get(name=folder_name, project_id=project)

            if folder.parent_folder:
                parent_folder = folder.parent_folder
            else:
                parent_folder = project

        files = File.objects.filter(parent_folder=folder, project_id=project)
        folders = Folder.objects.filter(parent_folder=folder, project_id=project)
        tasks_to_display = get_user_tasks(user, folder)

        # Нужно создать функционал обновления состояния задач с помощью fetch api

        return render(
            request,
            'file_processing/project_detail.html',
            {
                'project': project,
                'files': files,
                'folders': folders,
                'parent_folder': parent_folder,
                'upload_project_form': upload_project_form,
                'tasks': tasks_to_display,
            }
        )
    else:
        return HttpResponse('Private project')


def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(
        request,
        'file_processing/project_list.html',
        {
            'projects': projects,
        }
    )


def file_detail(request, user_slug, project_slug, file_path, extension):
    user = get_object_or_404(Profile, slug=user_slug)
    project = get_object_or_404(Project, slug=project_slug, owner=user.user)
    file = get_object_or_404(File, project_id=project, name=file_path.split('/')[-1])

    with file.filling_the_file.open('rb') as file:
        filling_the_file = file.read().decode('utf-8')

    if project.is_public or project.owner == request.user:
        return render(
            request,
            'file_processing/file_detail.html',
            {
                'project': project,
                'file': file,
                'filling_the_file': filling_the_file,
            }
        )
    return HttpResponse('Private project')


@require_POST
def file_processing(request):
    uploaded_files = request.FILES.getlist('files')
    project_id = request.POST.get('project_id')
    user_id = request.user.id
    project = Project.objects.get(id=project_id)

    for uploaded_file in uploaded_files:
        if uploaded_file:
            file_name, file_extension = os.path.splitext(uploaded_file.name)
            parent_folder = request.POST.get('folders')
            if parent_folder == 'None':
                parent_folder = None
            else:
                parent_folder = int(parent_folder)

            extension = get_or_none(FileExtensions, extension=file_extension)

            if not extension:
                return HttpResponse('Неподходящее расширение файла (что бы добавить файл нужно добавить расширение в базу данных). ')
            file_data = {
                'size': uploaded_file.size,
                'content': uploaded_file.read(),
                'project_name': project.name,
                'user_id': user_id,
                'file_name': file_name,
                'file_extension': file_extension,
                'parent_folder': parent_folder,
            }

            file_created.apply_async((file_data,), countdown=4)  # Искусственная задержка что-бы имитировать загрузки файла
        else:
            return JsonResponse({'status': 'no file uploaded'})

    return redirect('file_processing:project_detail', request.user.profile.slug, project.slug)


def upload_file(request, user_slug, project_slug):
    project = Project.objects.get(slug=project_slug, owner=request.user)
    directories = get_all_folders(project)

    return render(
        request,
        'file_processing/upload_files.html',
        {
            'project': project,
            'directories': directories,
        }
    )


@require_POST
def delete_file(request):
    file_id = request.POST.get('file_id')
    user = request.user
    file = File.objects.get(id=file_id)
    file_owner = file.project_id.owner

    if file_owner == user:
        file.delete()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})


def create_folder(request, user_slug, project_slug):
    user = get_object_or_404(Profile, slug=user_slug)
    project = get_object_or_404(Project, slug=project_slug, owner=user.user)

    if request.method == 'POST':
        parent_folder_id = request.POST.get('folders')
        folder_name = request.POST.get('folder_name')

        parent_folder = None

        if parent_folder_id != 'None':
            parent_folder = get_or_none(Folder, id=parent_folder_id, project_id=project)

        Folder.objects.create(
            name=folder_name,
            project_id=project,
            parent_folder=parent_folder,
        )

        return redirect('file_processing:project_detail', user_slug, project_slug)
    else:
        directories = get_all_folders(project)

        return render(
            request,
            'file_processing/create_folder.html',
            context={
                'user': user,
                'project': project,
                'directories': directories,
            }
        )
