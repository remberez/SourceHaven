# Generated by Django 5.0.6 on 2024-06-26 18:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent_folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_folder', to='file_processing.folder')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
                ('filling_the_file', models.TextField()),
                ('file_size', models.IntegerField()),
                ('parent_folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='file_processing.folder')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_processing.project')),
            ],
        ),
    ]
