from django.contrib import admin
from .models import *


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        project_id = obj.project_id
        super().delete_model(request, obj)
        project_id.update_project_langs()


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


class FileExtensions(admin.TabularInline):
    model = FileExtensions


@admin.register(ProgrammingLanguages)
class ProgrammingLanguagesAdmin(admin.ModelAdmin):
    inlines = [
        FileExtensions
    ]
