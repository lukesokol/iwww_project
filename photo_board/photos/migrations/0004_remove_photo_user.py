# Generated by Django 4.0.1 on 2022-01-17 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_alter_photo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='user',
        ),
    ]
