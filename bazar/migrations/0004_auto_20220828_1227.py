# Generated by Django 2.0.7 on 2022-08-28 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bazar', '0003_auto_20220828_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='userid',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='msg',
            new_name='value',
        ),
    ]
