# Generated by Django 5.0.3 on 2024-05-10 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_actorprofile_user_delete_authuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.actorprofile'),
            preserve_default=False,
        ),
    ]
