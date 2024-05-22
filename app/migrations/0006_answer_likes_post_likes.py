# Generated by Django 4.2 on 2024-05-21 18:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_answer_content_alter_answer_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(related_name='answer_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]