# Generated by Django 5.0.6 on 2024-08-08 06:38

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("l3meetings", "0004_meeting_assigned_to"),
    ]

    operations = [
        migrations.CreateModel(
            name="MeetingNotes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note_description", ckeditor.fields.RichTextField()),
                (
                    "meeting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="l3meetings.meeting",
                    ),
                ),
            ],
            options={
                "verbose_name": "Meeting Notes",
            },
        ),
    ]
