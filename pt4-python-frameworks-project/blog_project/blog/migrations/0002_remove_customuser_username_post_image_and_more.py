# Generated by Django 5.0.6 on 2024-06-27 10:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="username",
        ),
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
