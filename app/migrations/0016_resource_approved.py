# Generated by Django 5.0.3 on 2024-05-19 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_resource_status_resource_provided_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
