from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

class L3UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'l3users'

    def ready(self):
        post_migrate.connect(set_site_id, sender=self)

def set_site_id(sender, **kwargs):
    from django.conf import settings
    from django.contrib.sites.models import Site

    current_domain = settings.CURRENT_DOMAIN
    try:
        current_site = Site.objects.get(domain=current_domain)
        settings.SITE_ID = current_site.id
    except Site.DoesNotExist:
        # Create the site if it does not exist
        pass