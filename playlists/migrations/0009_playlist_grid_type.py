# Generated by Django 3.1.8 on 2021-05-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0008_remove_playlist_grid_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='grid_type',
            field=models.CharField(choices=[('Main', 'Main'), ('Reversed', 'Reversed')], default='Main', max_length=255),
            preserve_default=False,
        ),
    ]
