# Generated by Django 2.1.3 on 2019-02-27 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('six0', '0002_auto_20190117_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('pwd', models.CharField(max_length=100)),
                ('session_key', models.CharField(max_length=40)),
            ],
        ),
    ]
