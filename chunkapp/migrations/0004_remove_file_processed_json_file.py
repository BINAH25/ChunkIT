# Generated by Django 3.2.11 on 2022-07-26 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunkapp', '0003_file_processed_json_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='processed_json_file',
        ),
    ]
