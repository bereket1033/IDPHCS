# Generated by Django 5.0.3 on 2024-05-11 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_image_image_url_image_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image',
            new_name='image_url',
        ),
    ]
