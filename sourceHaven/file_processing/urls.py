from django.urls import path
from . import views

app_name = 'file_processing'
urlpatterns = [
    path('detail-project/<slug:user_slug>/<slug:project_slug>/upload-file/', views.upload_file, name='upload_file'),
    path('create_project/', views.create_project, name='create_project'),
    path('detail-project/<slug:user_slug>/<slug:project_slug>/<path:file_path>.<slug:extension>/', views.file_detail,
         name='file_detail'),
    path('detail-project/<slug:user_slug>/<slug:project_slug>/', views.project_detail,
         name='project_detail'),
    path('detail-project/<slug:user_slug>/<slug:project_slug>/<path:directory_path>/', views.project_detail,
         name='project_detail_with_path'),
    path('', views.project_list, name='projects_list'),
    path('file-processing/', views.file_processing, name='file_processing'),
    path('delete_file/', views.delete_file, name='delete_file'),
    path('create_folder/<slug:user_slug>/<slug:project_slug>/', views.create_folder, name='create_folder')
]
