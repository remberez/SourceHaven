from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from .utils import get_folder_hierarchy, project_directory_path
import os
from django.conf import settings


class ProgrammingLanguages(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FileExtensions(models.Model):
    lang = models.ForeignKey(ProgrammingLanguages, related_name='ext', on_delete=models.CASCADE)
    extension = models.CharField(max_length=5)

    def __str__(self):
        return self.extension


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, default=None)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    languages = models.ManyToManyField(ProgrammingLanguages, related_name='project', null=True, blank=True)

    def __str__(self):
        return f'Проект {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))

        if self._state.adding:
            path = os.path.join(settings.MEDIA_ROOT, 'projects', str(self.owner.id), self.name)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('file_processing:project_detail', args=[self.owner.profile.slug, self.slug])

    def update_project_langs(self):
        new_langs = []
        old_langs = self.languages.all()
        for file in self.file.all():
            extension = file.extension_id
            if extension:
                new_langs.append(extension.lang)

        for_add = set(new_langs) - set(old_langs)
        for_delete = set(old_langs) - set(new_langs)

        if for_add:
            for lang in for_add:
                self.languages.add(lang)

        if for_delete:
            for lang in for_delete:
                self.languages.remove(lang)


class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_folder', null=True,
                                      blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='folder', default=None)

    def __str__(self):
        return f'Папка {self.name}'

    def get_absolute_url(self):
        # ---- old version ----
        # if self.parent_folder:
        #     return self.parent_folder.get_absolute_url() + self.name + '/'
        # else:
        #     return reverse('file_processing:project_detail_with_path',
        #                    args=[self.project_id.owner.profile.slug, self.project_id.slug, self.name])
        # ---- old version ----

        args = [self.project_id.owner.profile.slug,
                self.project_id.slug,
                '/'.join(get_folder_hierarchy(self))]
        return reverse('file_processing:project_detail_with_path', args=args)

    def save(self, *args, **kwargs):
        if self._state.adding:
            path = os.path.join(settings.MEDIA_ROOT, 'projects', str(self.project_id.owner.id), self.project_id.name,
                                "/".join(get_folder_hierarchy(self)))
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

        super().save(*args, **kwargs)


class File(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='file')
    extension = models.CharField(max_length=5)
    extension_id = models.ForeignKey(FileExtensions, on_delete=models.CASCADE, related_name='files', null=True)
    name = models.CharField(max_length=100)
    filling_the_file = models.FileField(upload_to=project_directory_path)
    file_size = models.IntegerField()
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='file', null=True, blank=True)

    def __str__(self):
        return f'Файл {self.name}'

    def get_absolute_url(self):
        # ---- old version ----
        # if self.parent_folder:
        #     profile_slug, project_slug, *path = self.parent_folder.get_absolute_url().split('/')[3:]
        #
        #     return reverse(
        #         'file_processing:file_detail', args=[
        #             profile_slug,
        #             project_slug,
        #             '/'.join(path) + self.name,
        #             self.extension[1:]]
        #     )
        # else:
        #     return reverse('file_processing:file_detail',
        #                    args=[self.project_id.owner.profile.slug, self.project_id.slug, self.name,
        #                          self.extension[1:]])
        # ---- old version ----

        args = [self.project_id.owner.profile.slug,
                self.project_id.slug, '/'.join(get_folder_hierarchy(self)),
                self.extension[1:]]
        return reverse('file_processing:file_detail', args=args)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        project = self.project_id
        project.update_project_langs()

    def delete(self, *args, **kwargs):
        self.filling_the_file.delete()
        super().delete(*args, **kwargs)
        project = self.project_id
        project.update_project_langs()
