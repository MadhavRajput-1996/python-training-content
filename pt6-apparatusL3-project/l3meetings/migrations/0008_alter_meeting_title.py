# Generated by Django 5.0.6 on 2024-08-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("l3meetings", "0007_remove_actionitem_action_for_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meeting",
            name="title",
            field=models.CharField(max_length=250),
        ),
    ]
