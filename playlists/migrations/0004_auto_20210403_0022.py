# Generated by Django 3.1.7 on 2021-04-02 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0003_auto_20210329_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbs'),
        ),
    ]
