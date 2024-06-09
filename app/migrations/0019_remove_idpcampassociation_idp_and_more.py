# Generated by Django 5.0.6 on 2024-06-08 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_sharing_shared_with_alter_sharing_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idpcampassociation',
            name='idp',
        ),
        migrations.AddField(
            model_name='idpcampassociation',
            name='idpemail',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='idpcampassociation',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
