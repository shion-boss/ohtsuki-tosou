# Generated by Django 3.0.7 on 2020-06-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tosou', '0020_message_user_model_post_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_user_model',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
