# Generated by Django 3.2.8 on 2021-10-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_visits',
            field=models.IntegerField(default=0),
        ),
    ]