# Generated by Django 5.0.3 on 2024-05-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_image_image_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='status',
            field=models.CharField(default='active', max_length=100),
        ),
    ]