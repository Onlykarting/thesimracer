# Generated by Django 3.1.8 on 2021-05-21 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0007_merge_20210521_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='grid_type',
        ),
    ]