# Generated by Django 3.0.14 on 2022-01-11 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_comment_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='intro',
        ),
    ]
