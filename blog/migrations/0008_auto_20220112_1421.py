# Generated by Django 3.0.14 on 2022-01-12 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20220111_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='message',
            new_name='body',
        ),
    ]
