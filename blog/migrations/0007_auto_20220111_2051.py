# Generated by Django 3.0.14 on 2022-01-11 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_intro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='message',
        ),
    ]
