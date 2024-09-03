from django.conf import settings
from django.http import request

def register_my_context_processor(self):
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append('invites.context_processors.user_permission_context')

register_my_context_processor(request)