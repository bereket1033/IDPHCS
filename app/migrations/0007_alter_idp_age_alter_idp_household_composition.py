# Generated by Django 5.0.3 on 2024-05-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_idp_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idp',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='idp',
            name='household_composition',
            field=models.IntegerField(),
        ),
    ]
