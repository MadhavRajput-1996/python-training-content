from django.contrib import admin
from .models import *

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

admin.site.register(EmailNotificationTemplate)