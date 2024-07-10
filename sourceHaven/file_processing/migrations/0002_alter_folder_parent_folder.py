# Generated by Django 5.0.6 on 2024-06-26 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_processing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parent_folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_folder', to='file_processing.folder'),
        ),
    ]