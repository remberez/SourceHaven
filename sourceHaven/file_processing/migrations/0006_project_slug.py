# Generated by Django 5.0.6 on 2024-06-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_processing', '0005_project_description_project_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
