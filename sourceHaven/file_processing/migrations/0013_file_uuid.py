# Generated by Django 5.0.6 on 2024-07-04 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_processing', '0012_alter_file_filling_the_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
