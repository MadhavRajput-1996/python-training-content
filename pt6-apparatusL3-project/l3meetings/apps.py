from django.apps import AppConfig


class L3MeetingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "l3meetings"

    def ready(self):
        import l3meetings.signals 
        