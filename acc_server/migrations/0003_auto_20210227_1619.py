# Generated by Django 3.1.7 on 2021-02-27 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acc_server', '0002_auto_20210227_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsettings',
            name='track',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='acc_server.track'),
        ),
    ]