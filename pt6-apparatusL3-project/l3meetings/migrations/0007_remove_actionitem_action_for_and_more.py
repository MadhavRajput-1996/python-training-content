# Generated by Django 5.0.6 on 2024-08-12 06:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("l3meetings", "0006_alter_actionitem_actual_end_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="actionitem",
            name="action_for",
        ),
        migrations.RemoveField(
            model_name="actionitem",
            name="category",
        ),
        migrations.RemoveField(
            model_name="response",
            name="category",
        ),
        migrations.DeleteModel(
            name="ActionFor",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]