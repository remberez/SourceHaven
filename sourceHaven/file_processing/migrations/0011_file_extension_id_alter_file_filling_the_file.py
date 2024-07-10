# Generated by Django 5.0.6 on 2024-06-29 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_processing', '0010_alter_file_filling_the_file_alter_project_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='extension_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='file_processing.fileextensions'),
        ),
        migrations.AlterField(
            model_name='file',
            name='filling_the_file',
            field=models.FileField(upload_to='files/%Y/%m/%d/'),
        ),
    ]