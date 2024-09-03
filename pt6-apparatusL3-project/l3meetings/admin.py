from django.contrib import admin
from .models import *

admin.site.register(Meeting)
admin.site.register(ActionItem)
admin.site.register(Response)
admin.site.register(Agenda)
admin.site.register(DeliveryUnit)
admin.site.register(MeetingAgenda)
admin.site.register(DeliveryUnitDefaultAgenda)
admin.site.register(MeetingNotes)