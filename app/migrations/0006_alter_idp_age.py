# Generated by Django 5.0.3 on 2024-05-11 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_idp_household_composition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idp',
            name='age',
            field=models.CharField(max_length=100),
        ),
    ]
