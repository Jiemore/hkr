# Generated by Django 2.1.3 on 2019-03-02 23:44

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('six0', '0007_userprofile_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
